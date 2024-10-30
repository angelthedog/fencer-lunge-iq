import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

_apiServerUrl = 'https://service.deepmotion.com'
_sessionCredentials = (os.getenv("DEEPMOTION_CLIENT_ID"), os.getenv("DEEPMOTION_CLIENT_SECRET"))

def get_session():
    authUrl = _apiServerUrl + '/session/auth'
    session = requests.Session()
    session.auth = _sessionCredentials
    request = session.get(authUrl)
    if request.status_code == 200:
        print('Succeed to authenticate ')
        return session
    else:
        raise Exception("Failed to authenticate with DeepMotion API")

def get_response(session, urlPath):
    respUrl = _apiServerUrl + urlPath
    resp = session.get(respUrl)
    if resp.status_code == 200:
        return resp
    else:
        print('Failed to contact server ' + resp.status_code + '\n')

def upload_video(session, video_path):
    with open(video_path, 'rb') as f:
        vFile = f.read()
    
    headerContent = {'Content-length': str(len(vFile)), 'Content-type': 'application/octet-stream'}
    vName = os.path.basename(video_path)
    uploadUrl = f"{_apiServerUrl}/upload?name={vName}&resumable=0"
    
    resp = session.get(uploadUrl)
    if resp.status_code == 200:
        jsonResp = json.loads(resp.text)
        gcsUrl = jsonResp['url']
        uploadResp = session.put(gcsUrl, headers=headerContent, data=vFile)
        if uploadResp.status_code == 200:
            return gcsUrl
    raise Exception("Failed to upload video to DeepMotion")

def start_new_job(session, gcs_url):
    processUrl = f"{_apiServerUrl}/process"
    processCfgJson = {
        "url": gcs_url,
        "processor": "video2anim",
        "params": [
            "config=configDefault",
            "formats=bvh"
        ]
    }
    processResp = session.post(processUrl, json=processCfgJson)
    if processResp.status_code == 200:
        return json.loads(processResp.text)['rid']
    raise Exception("Failed to start new job with DeepMotion")

def check_job_status(session, rid) -> Dict[str, Any]:
    statusUrl = f"{_apiServerUrl}/status/{rid}"
    resp = session.get(statusUrl)
    if resp.status_code == 200:
        response = json.loads(resp.text)
        if response['count'] > 0:
            return response['status'][0]
        else:
            return {'status': 'UNKNOWN'}
    raise Exception("Failed to check job status")

def download_bvh(session, file_path):
    downloadUrl = f"{_apiServerUrl}/download/{file_path}"
    print("downloadUrl", downloadUrl)
    downloadResp = session.get(downloadUrl)
    print("status_code: ", downloadResp.status_code)
    if downloadResp.status_code == 200:
        downloadRespJson = json.loads(downloadResp.text)
        if downloadRespJson['count'] > 0:
            bvh_url = downloadRespJson['links'][0]['urls'][0]['files'][0]['bvh']
            bvh_content = session.get(bvh_url).content
            return bvh_content
    raise Exception("Failed to download BVH file")

def download_job_by_rid(session, rid, download_dir=None):
    """
    Downloads a job by its rid. Saves the job files in the specified directory.
    
    Parameters:
    - session: requests.Session, an authenticated session.
    - rid: str, required, the job ID to download.
    - download_dir: str, optional, directory to save the downloaded files.
                    If not provided, files are saved in the current working directory.
    """
    if download_dir is None:
        download_dir = os.getcwd()
    else:
        os.makedirs(download_dir, exist_ok=True)

    # Set up the download path for the rid
    dPath = os.path.join(download_dir, rid + '.')

  # Make the API request to get the download URLs
    downloadResp = get_response(session, '/download/' + rid)
    if downloadResp is None or downloadResp.status_code != 200:
        print(f"Failed to retrieve download URLs for rid {rid}.")
        return

    downloadRespJson = json.loads(downloadResp.text)

    # Check for valid response and file count
    if downloadRespJson.get('count', 0) > 0:
        for fileUrl in downloadRespJson['links'][0]['urls']:
            for file in fileUrl['files']:
                if 'bvh' in file and 'male-young.bvh' in file['bvh']:
                    male_young_bvh_url = file['bvh']
                    
                    # Define the save path
                    file_path = os.path.join(download_dir, f"{rid}_male-young.bvh")
                    
                    # Download the bvh file
                    downloadResp = session.get(male_young_bvh_url)
                    if downloadResp.status_code == 200:
                        with open(file_path, 'wb') as f:
                            f.write(downloadResp.content)
                        print(f'\nFile saved to {file_path}')
                    else:
                        print(f"Failed to download male-young.bvh file for rid {rid}.")
                    return  # Exit after downloading the target file
        print(f"male-young.bvh not found in the response for rid {rid}.")
    else:
        print(f"No files found for rid {rid}.")


# Ensure session is initialized before making any requests
if __name__ == '__main__':
    session = get_session();
    if session is not None:
        download_job_by_rid(session, 'mECjCqM93zE3pddpUDUot7')
    else:
        print("Failed to authenticate session; exiting.")