# -*- coding: utf-8 -*- 
import requests
import os
import sys
gitlab_url = os.environ.get("CI_SERVER_URL", "")
project_id = os.environ.get("CI_PROJECT_ID")
mr_iid = os.environ.get("CI_MERGE_REQUEST_IID")
private_token = os.environ.get("REGISTRATION_TOKEN")

yaml_file_path = "amazon_q_review.md"  
try:
    with open(yaml_file_path, "r") as file:
        yaml_content = file.read()
except Exception as e:
    print(f"读取YAML文件失败: {e}")
    sys.exit(1)
headers = {
    "PRIVATE-TOKEN": private_token,
    "Content-Type": "application/json"
}

url = gitlab_url + "/api/v4/projects/" + project_id + "/merge_requests/" + mr_iid + "/notes"
response = requests.post(url, headers=headers, json={"body": yaml_content})

if response.status_code >= 200 and response.status_code < 300:
    print(f"成功添加评论: {response.status_code}")
    print(response.json())
else:
    print(f"添加评论失败: {response.status_code}")
    print(response.text)
    sys.exit(1)