import re

import requests
from requests.auth import HTTPBasicAuth


class Repository:
    token: str = (
        f""
    )
    headers = {"Content-Type": "application/json",
               "Authorization": f'Bearer {token}'}

    @classmethod
    def get_repositories(cls):
        url = f""
        get_content = requests.get(url, headers=cls.headers)

    @classmethod
    def get_script_content(cls, repository_name, script_name):
        url = f"{repository_name}/{script_name}"
        print(url)
        get_content = requests.get(url, headers=cls.headers)
        return get_content.text

    # @classmethod
    # def filter_repository_html_str(cls, html_raw_repo_text):
    #     return re.sub(r"<body[^>]*>|</body></html>", "", html_raw_repo_text)


Repository.get_repositories()
