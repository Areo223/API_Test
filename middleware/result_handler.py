import json
from common.csv_handler import CsvHandler
from common.excel_handler import ExcelHandler


def ResultHandler(code=None, msg=None, data=None):
    default_values = {
        'code': 1,
        'msg': 'success',
        'data': {}
    }
    from_csv = {}
    result_dict = {}

    if code is not None:
        result_dict['code'] = code
        from_csv['code'] = True
    else:
        result_dict['code'] = default_values['code']
        from_csv['code'] = False

    if msg is not None:
        result_dict['msg'] = msg
        from_csv['msg'] = True
    else:
        result_dict['msg'] = default_values['msg']
        from_csv['msg'] = False

    if data is not None:
        try:
            # 先将data转换为字符串类型再进行json.loads操作
            if isinstance(data, dict):
                data = json.dumps(data)
            result_dict['data'] = json.loads(data)
            from_csv['data'] = True
        except json.JSONDecodeError:
            print(f"Invalid JSON format for data: {data}, using default value.")
            result_dict['data'] = default_values['data']
            from_csv['data'] = False
    else:
        result_dict['data'] = default_values['data']
        from_csv['data'] = False

    return result_dict, from_csv


def compare_dicts_with_assert(expected_dict, from_csv_dict, actual_dict):
    for key in expected_dict:
        if from_csv_dict[key]:
            if key in actual_dict:
                if expected_dict[key]!= actual_dict[key]:
                    assert expected_dict[key] == actual_dict[key], f"键 {key} 的值不匹配，预期值为 {expected_dict[key]}，实际值为 {actual_dict[key]}"
            else:
                assert key in actual_dict, f"键 {key} 在实际_dict中不存在，预期值为 {expected_dict[key]}"


if __name__ == "__main__":
    # csv1 = CsvHandler('../cases.csv')
    # data = csv1.read()
    # print(data)

    xlsx = ExcelHandler('../cases.xlsx')
    data = xlsx.read()
    print(data)

    actual_result_dict = {
        'code': 0,
        'msg': 'success',
        'data': {
            'content': ['item1', 'item2'],
            'totalPages': 1,
            'totalElements': 2
        }
    }

    for dictionary in data:
        result = dictionary['expect']
        try:
            result_dict = json.loads(result)
            if isinstance(result_dict, dict):
                # 将result_dict里的data键对应的值转换为字符串类型后再传入ResultHandler
                data_to_pass = json.dumps(result_dict.get('data')) if result_dict.get('data') is not None else None
                expected_dict, from_csv_dict = ResultHandler(code=result_dict.get('code'),
                                                            msg=result_dict.get('msg'),
                                                            data=data_to_pass)
                try:
                    compare_dicts_with_assert(expected_dict, from_csv_dict, actual_dict=actual_result_dict)
                    print("结果匹配")
                except AssertionError as e:
                    print(f"断言失败: {e}")
        except json.JSONDecodeError:
            print(f"Invalid expect format in row: {dictionary}, skipping...")