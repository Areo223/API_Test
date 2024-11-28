import json

import pytest
import requests

from common.csv_handler import CsvHandler

# headers = {
#     "token":"eyJhbGciOiJIUzI1NiJ9.eyJwaG9uZU51bSI6IjEyMzQ1Njc4OTAyIiwiaWQiOjQsImV4cCI6MTczMjg5OTAxMH0.itYuwb6WdBikanRpjVKJoud5XYy3gWRIm2QoH5pMamg"
# }
# response = requests.get("http://localhost:8080/diary?text=test_text&tag=test_tagContent",headers=headers)
# assert response.status_code == 200
# print(type(response.json()))
# print(response.json())
# data=CsvHandler(r'C:\Users\areo3\PycharmProjects\Demo\cases.csv').read()
# print(type(data[1]['expect']))
# print(data[1]['expect'])
# assert str(response.json()) == data[1]['expect']
# id_list = [item["id"] for item in response.json()["data"]["content"]]
# print(id_list)
# for id in id_list:
#     print(type(id))
#     r=requests.delete(f"http://localhost:8080/diary/{id}",headers=headers)
#     assert r.status_code == 200


#

# data = {
#     "text": "test_text",
#     "tag": [
#         {
#             "tagContent": "test_tagContent1"
#         },
#         {
#             "tagContent": "test_tagContent2"
#         }
#     ]
# }
# response = requests.post('http://localhost:8080/diary',headers=headers, json=data)
# print(response.text)

# data = {
#     "phoneNumber": "12345678902",
#     "password": "12345678"
# }
# response = requests.post("http://localhost:8080/diary/login", json=data)
# response_dict = json.loads(response.text)
# token = response_dict["token"]
# print(token)

# class Demo:
#     @pytest.mark.parametrize("env", yaml.safe_load(open("./env.yml")))
#     def test_yaml(self, env):
#         if "test" in env:
#             print("���ǲ��Ի���")
#             # print(env)
#             print("���Ի�����ip�ǣ�", env["test"])
#         elif "dev" in env:
#             print("���ǿ����ļ�")
#             print("����������ip�ǣ�", env["dev"])
#             # print(env)