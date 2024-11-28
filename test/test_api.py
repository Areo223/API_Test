import json

import pytest
import requests
from Tools.scripts.make_ctype import method

from common.csv_handler import CsvHandler
from common.excel_handler import ExcelHandler
from middleware.result_handler import compare_dicts_with_assert, ResultHandler


# def test_api():
#     pass
@pytest.fixture(scope="session")
def session():
    return requests.Session()

@pytest.fixture(scope="session")
def login_session(session):
    data={
    "phoneNumber":"12345678902",
    "password":"12345678"
    }
    response = session.post("http://localhost:8080/diary/login", json=data).text
    response_dict = json.loads(response)
    token = response_dict["token"]
    session.headers.update({"token": token})
    return session
#
# @pytest.fixture
# def new_diary_session(login_session):
#     data={
#     "text": "test_text",
#     "tag": [
#             {
#                 "tagContent": "test_tagContent1"
#             },
#             {
#                 "tagContent": "test_tagContent2"
#             }
#         ]
#     }
#     response = login_session.post('http://localhost:8080/diary',json=data)
#     assert response.status_code == 200
#     return login_session
#
# @pytest.fixture
# def list_diaries_session(new_diary_session):
#
#     return new_diary_session
#
# # @pytest.fixture(scope="session")
# # def no_login_session(session):
# #     return session
#
# # 测试登录接口
# def test_login(login_session):
#    pass
#
# # 测试新建日记接口
# def test_new_dairy(new_diary_session):
#     pass
#
# # 测试删除日记接口
# def test_delete_dairy(login_session,new_diary_session):
#     response = new_diary_session.get("http://localhost:8080/diary?text=test_text&tag=test_tagContent")
#     assert response.status_code == 200
#     print(response.json())
#     id_list = [item["id"] for item in response.json()["data"]["content"]]
#     print(id_list)
#     for id in id_list:
#         print(type(id))
#         r = login_session.delete(f"http://localhost:8080/diary/{id}")
#         assert r.status_code == 200
#
# # 测试查找日记接口
# def test_list_dairy(login_session,new_diary_session):
#     response = login_session.get("http://localhost:8080/diary?tag=tag")
#     assert response.status_code == 200

@pytest.fixture
def base_url():
    return "http://localhost:8080/diary"

@pytest.mark.parametrize('data',CsvHandler(r'C:\Users\areo3\PycharmProjects\Demo\cases.csv').read())
def test_csv_handler(data, login_session, base_url):
    print("csv")
    print(data)
    the_url = base_url+data['url']
    response = login_session.request(method=data['method'],url=the_url,params=data['parametrize'],json=data['json'])
    print("csv")
    print(response)
    try:
        result_dict = json.loads(data['expect'])
        if isinstance(result_dict, dict):
            # 将result_dict里的data键对应的值转换为字符串类型后再传入ResultHandler
            data_to_pass = json.dumps(result_dict.get('data')) if result_dict.get('data') is not None else None
            expected_dict, from_csv_dict = ResultHandler(code=result_dict.get('code'),
                                                         msg=result_dict.get('msg'),
                                                         data=data_to_pass)
            try:
                compare_dicts_with_assert(expected_dict, from_csv_dict, actual_dict=response.json())
                print("结果匹配")
            except AssertionError as e:
                print(f"断言失败: {e}")
                assert False
    except json.JSONDecodeError:
        print(f"Invalid expect format in row: {data}, skipping...")

@pytest.mark.parametrize('data',ExcelHandler(r'C:\Users\areo3\PycharmProjects\Demo\cases.xlsx').read())
def test_excel_handler(data, login_session, base_url):
    print("excel")
    print(data)
    the_url = base_url+(data['url'] if data['url'] is not None else "")
    response = login_session.request(method=data['method'],url=the_url,params=data['parametrize'])
    print("excel")
    print(response)
    try:
        result_dict = json.loads(data['expect'])
        if isinstance(result_dict, dict):
            # 将result_dict里的data键对应的值转换为字符串类型后再传入ResultHandler
            data_to_pass = json.dumps(result_dict.get('data')) if result_dict.get('data') is not None else None
            expected_dict, from_csv_dict = ResultHandler(code=result_dict.get('code'),
                                                        msg=result_dict.get('msg'),
                                                        data=data_to_pass)
            try:
                compare_dicts_with_assert(expected_dict, from_csv_dict, actual_dict=response.json())
                print("结果匹配")
            except AssertionError as e:
                print(f"断言失败: {e}")
                assert False
    except json.JSONDecodeError:
        print(f"Invalid expect format in row: {data}, skipping...")