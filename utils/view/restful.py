from utils.util.json_util import JsonUtil



def result(code:int,msg:str,data:dict,**kwargs)->str:
     return JsonUtil.dumps({
        "code":code,
        "msg":msg,
        "data":data
    })

def success(msg:str=None,data:dict=None,**kwargs) -> str:
    return result(200,msg=msg or "处理成功",data=data,**kwargs)

def login_success(data:dict=None,**kwargs) -> str:
    return success(msg="登录成功",data=data,**kwargs)

def get_success(data:dict=None,**kwargs) -> str:
    return success(msg="获取成功",data=data,**kwargs)

def add_success(data:dict=None,**kwargs) -> str:
    return success(msg="添加成功",data=data,**kwargs)

def change_success(data:dict=None,**kwargs) -> str:
    return success(msg="修改成功",data=data,**kwargs)

def delete_success(data:dict=None,**kwargs) -> str:
    return success(msg="删除成功",data=data,**kwargs)

def upload_success(data:dict=None,**kwargs) -> str:
    return success(msg="上传成功",data=data,**kwargs)

def synchronize_success(data:dict=None,**kwargs) -> str:
    return success(msg="同步成功",data=data,**kwargs)

def copy_success(data:dict=None,**kwargs) -> str:
    return success(msg="复制成功",data=data,**kwargs)

def fail(msg:str=None,data:dict=None,**kwargs) -> str:
    return result(400,msg=msg or "处理失败",data=data,**kwargs)

def not_login(data:dict=None,**kwargs) -> str:
    return result(401,msg="未登录,请重新登录",data=data,**kwargs)

def not_permission(data:dict=None,**kwargs) -> str:
    return result(403,msg="没有权限",data=data,**kwargs)

def not_found(data:dict=None,**kwargs) -> str:
    return result(404,msg="资源不存在",data=data,**kwargs)

def method_not_allowed(data:dict=None,**kwargs) -> str:
    return result(405,msg="请求方法不允许",data=data,**kwargs)

def server_error(data:dict=None,**kwargs) -> str:
    return result(500,msg="服务器内部错误",data=data,**kwargs)
