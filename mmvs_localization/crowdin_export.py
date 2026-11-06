# pip install crowdin-api-client

from typing import Optional, Dict, Any
from pathlib import Path
from crowdin_api import CrowdinClient
import httpx
import time
from . import bpl
from . import config
from .project_config import ProjectConfig


class crowdin_downloader():
    def __init__(self, project_config: ProjectConfig, api_token: str):
        self.client: Optional[CrowdinClient] = None
        self.project_id = project_config.project_id
        self.api_token = api_token

    def connect(self) -> None:
        self.client = CrowdinClient(token=self.api_token)

    def build_project(self) -> Optional[Dict[str, Any]]:
        # Build
        if self.client:
            request_data: Dict[str, Any] = {}
            bundle = self.client.translations.build_project_translation(  # type: ignore
                request_data=request_data,
                projectId=self.project_id
            )  
            return bundle
        return None

    def try_get_download_url(self, bundle: Dict[str, Any]) -> Optional[str]:
        if self.client is None:
            return None

        build_id = bundle['data']['id']
        response = self.client.translations.download_project_translations(
            buildId=build_id,
            projectId=self.project_id
        )

        if not isinstance(response, dict):
            print("Unexpected response type:", type(response).__name__)
            return None

        # Check if the response contains a URL
        if 'data' not in response:
            print("No data found in response.")
            print(response)  # type: ignore
            return None

        if 'url' not in response['data']:
            print("No URL found in response.")
            print(response)  # type: ignore
            return None
        
        if isinstance(response['data'], dict):
            if isinstance(response['data']['url'], str):
                return response['data']['url']

    def download_project(self, bundle: Dict[str, Any], file_path: Path) -> Optional[Path]:

        if self.client is None:
            return None

        maximum_attempts: int = config.crowdin_download_max_attempts
        delay_between_attempts: int = config.crowdin_delay_between_attempts_seconds
        current_attempt: int = 0
        
        download_url: Optional[str] = None
        while current_attempt < maximum_attempts and download_url is None:
            current_attempt += 1
            try_get_download_url = self.try_get_download_url(bundle)
            if try_get_download_url:
                download_url = try_get_download_url
            else:
                print(f"Attempt {current_attempt} to get download URL failed.")
                if delay_between_attempts > 0:
                    for i in range(delay_between_attempts):
                        print(f"Retrying in {delay_between_attempts - i} seconds...", end='\r', flush=True)
                        time.sleep(1)
                continue

        if download_url is None:
            print("Failed to get download URL after multiple attempts.")
            return None
    
        # Specify where to save the file
        folder = file_path.parent
        folder.mkdir(parents=True, exist_ok=True)

        # Download and save the file
        print(f"Downloading translations from Crowdin...")
        counter = bpl.utils.CounterTimer()
        with httpx.Client() as client:
            file_response = client.get(download_url)
            with open(file_path, "wb") as file:
                file.write(file_response.content)
        print(f"File downloaded in {counter.get_str_time()} to:")
        print(f"  {file_path}")

        return file_path

def start_export(project_config: ProjectConfig, api_token: str, file_path: Path) -> bool:
    print("Start exporting...")
    my_crowdin = crowdin_downloader(project_config, api_token)
    my_crowdin.connect()
    bundle = my_crowdin.build_project()
    if bundle:
        result = my_crowdin.download_project(bundle, file_path)
        if result:
            print("Export successful.")
            return True
        else:
            print("Export failed.")
            return False
    else:
        print("Failed to build project.")
        return False