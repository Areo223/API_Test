from sqlalchemy import Table, Column

from Flask.exts import db

# 项目和用户的关联表
project_user = Table('project_user', db.Model.metadata,
                     Column('project_id', db.Integer, db.ForeignKey('project.id')),
                     Column('user_id', db.Integer, db.ForeignKey('user.id')))

# 项目和模块的关联表
project_module = Table('project_module', db.Model.metadata,
                       Column('project_id', db.Integer, db.ForeignKey('project.id')),
                       Column('module_id', db.Integer, db.ForeignKey('module.id')))
# 项目和用例集的关联变
project_caseset = Table('project_caseset', db.Model.metadata,
                        Column('project_id', db.Integer, db.ForeignKey('project.id')),
                        Column('caseset_id', db.Integer, db.ForeignKey('case_set.id')))

# 模块和接口的关联表
module_api = Table('module_api', db.Model.metadata,
                   Column('module_id', db.Integer, db.ForeignKey('module.id')),
                   Column('api_id', db.Integer, db.ForeignKey('api.id')))

# 用例集和用例的关联表
caseset_case= Table('caseset_case', db.Model.metadata,
                    Column('caseset_id', db.Integer, db.ForeignKey('case_set.id')),
                    Column('case_id', db.Integer, db.ForeignKey('case.id')))
