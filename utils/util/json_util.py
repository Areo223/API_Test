import json
from datetime import datetime
from json import JSONEncoder


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        """
        覆盖默认的序列化方法，处理 datetime 类型的对象。

        参数:
            obj: 要序列化的对象。

        返回:
            str 或 object: 如果对象是 datetime 类型，返回其 ISO 格式的字符串；否则，调用父类的 default 方法。
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class JsonUtil:
    def __init__(self):
        pass

    # 定义一个类方法，用于将对象转换为 JSON 格式并写入到文件指针
    @classmethod
    def dump(cls, obj, fp, *args, **kwargs)->None:
        # 设置 ensure_ascii 参数为 False，确保非 ASCII 字符能正确显示
        kwargs.setdefault('ensure_ascii', False)
        # 将对象转换为 JSON 格式并写入到文件指针
        return json.dump(obj, fp,*args,**kwargs)

    @classmethod
    def dumps(cls, obj, *args, **kwargs)->str:
        # 设置 ensure_ascii 参数为 False，确保非 ASCII 字符能正确显示
        kwargs.setdefault('ensure_ascii', False)
        # 将对象转换为 JSON 格式并返回
        return json.dumps(obj,default=encode_object,cls=CustomEncoder,*args,**kwargs)

    @classmethod
    def load(cls, fp, *args, **kwargs)->object:
        # 从文件指针中读取 JSON 格式的数据并转换为对象，返回转换后的对象
        return json.load(fp,*args,**kwargs)

    @classmethod
    def loads(cls, s:str, *args, **kwargs)->object:
        # 从字符串中读取 JSON 格式的数据并转换为对象，返回转换后的对象
        return json.loads(s,*args,**kwargs)

    @classmethod
    def field_to_json(cls,dict_data:dict,*args) -> dict:
        """
        把字典中已存在的key的值转为json字符串

        参数:
            dict_data: 字典数据
            *args: 要转换为 JSON 的键名

        返回:
            dict: 转换后的字典数据
        """
        for key in args:
            if key in dict_data:
                dict_data[key] = cls.dumps(dict_data[key])
        return dict_data


def encode_object(obj):
    """ json.dumps转化时，先把属于bytes类型的解码，若解码失败返回str类型，和其他对象属性统一转化成str"""
    if isinstance(obj, bytes):
        try:
            return bytes.decode(obj)
        except UnicodeDecodeError:
            return str(obj)
    else:
        return str(obj)