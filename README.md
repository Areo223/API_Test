# 技术栈:Flask


# 仍待完善点:

1.常量配置表(重建config文件)

2.目前url指定有限制(放弃使用pytest,使用Flask重写搭建web框架能更灵活的管理api)

3.更详细的日志和分级,垃圾信息的筛除(编写了logger类,再利用钩子详细记录日志,并保存到本地)

4.解决目前自动化脚本依赖本地allure程序的问题(~~解决,pull后要先运行一遍setup.py会自动安装相关版本依赖~~,解决,不使用allure就不会有问题了,自己写一个日志生成)

5.怎么更好的测试删除操作(删除最好先创建),接口关联

  -如果将创建直接写在fixture中,但是会硬编码造成局限性

  -如果在写入测试用例时先写创建,再写删除,但是又怎么处理标识符id的传输(解决方法:给予用户灵活的设置空间,类似postman那样,同时可以进行公用的设置,减少重复性操作)

6.逐步形成工具化的web测试框架,搭建后台测试平台

7.使用数据库进行项目,模板,接口,用例,测试数据,测试报告管理

8.相关数据加密,定时测试,报告收发....
