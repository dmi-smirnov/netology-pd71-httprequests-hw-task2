import requests
import os

class YaUploader:
    api_url = 'https://cloud-api.yandex.net'
    
    def __init__(self, token: str):
        self.token = token

    def get_upload_link(self, cloud_file_path):
        upload_route = '/v1/disk/resources/upload'

        url = self.api_url + upload_route
        headers = {'Authorization': self.token}
        params = {'path': cloud_file_path, 'overwrite': True}
        resp = requests.get(url, headers=headers, params=params)

        req_status_code = resp.status_code
        if req_status_code != 200:
            print(f'Error: HTTP request status code is {req_status_code}.')
            return
        
        return resp.json()['href']

    def upload(self, file_path: str):
        file_name = os.path.basename(file_path)
        upload_link = self.get_upload_link('/' + file_name)
        headers = {'Authorization': self.token}
        resp = requests.put(upload_link, headers=headers,
            data=open(file_path, 'rb'))
        
        req_status_code = resp.status_code
        if req_status_code != 201:
            print(f'Error: HTTP request status code is {req_status_code}.')
            return
        
        print('File uploaded.')    

if __name__ == '__main__':
    path_to_file = __file__
    token = input()
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)