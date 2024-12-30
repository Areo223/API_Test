from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, Table, Column
from sqlalchemy.orm import relationship

app = Flask(__name__)
HOSTNAME="127.0.0.1"
PORT="3306"
USERNAME="root"
PASSWORD="1234"
DATABASE="api_test"
app.config['SQLALCHEMY_DATABASE_URI']=f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"

db = SQLAlchemy(app)

# # 测试数据库是否正确连接
# with app.app_context():
#     with db.engine.connect() as conn:
#         result = conn.execute(text("select 1"))
#         print(result.fetchone())

# 项目和用户的关联表
project_user = Table('project_user', db.Model.metadata,
                     Column('project_id', db.Integer, db.ForeignKey('project.id')),
                     Column('user_id', db.Integer, db.ForeignKey('user.id')))

# 项目和模块的关联表
project_model = Table('project_model', db.Model.metadata,
                      Column('project_id', db.Integer, db.ForeignKey('project.id')),
                      Column('model_id', db.Integer, db.ForeignKey('model.id')))

# 项目和用例集的关联变
project_caseset = Table('project_caseset', db.Model.metadata,
                        Column('project_id', db.Integer, db.ForeignKey('project.id')),
                        Column('caseset_id', db.Integer, db.ForeignKey('case_set.id')))

# 模块和接口的关联表
model_interface = Table('model_interface', db.Model.metadata,
                        Column('model_id', db.Integer, db.ForeignKey('model.id')),
                        Column('interface_id', db.Integer, db.ForeignKey('interface.id')))

# 用例集和用例的关联表
caseset_case= Table('caseset_case', db.Model.metadata,
                    Column('caseset_id', db.Integer, db.ForeignKey('case_set.id')),
                    Column('case_id', db.Integer, db.ForeignKey('case.id')))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), nullable=False)
    project_url = db.Column(db.String(50), nullable=False)


    model = relationship('Model',secondary=project_model,backref='project')
    user = relationship("User",secondary=project_user,backref="project")
    caseset = relationship("CaseSet",secondary=project_caseset,backref="project")



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50), nullable=False)

    interface = relationship("Interface",secondary=model_interface,backref="model")

class Interface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interface_name = db.Column(db.String(50), nullable=False)
    interface_url = db.Column(db.String(50), nullable=False)
    method = db.Column(db.String(50), nullable=False)
    data = db.Column(db.String(50), nullable=False)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    html = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)


class CaseSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caseset_name = db.Column(db.String(50), nullable=False)

    case=relationship("Case",secondary=caseset_case,backref="CaseSet")

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_name = db.Column(db.String(50), nullable=False)

# 创建数据库
# with app.app_context():
#     db.create_all()
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/project', methods=['POST'])
# 新增项目
def project_add():
    try:
        project = Project(project_name=request.form['project_name'], project_url=request.form['project_name'])
        db.session.add(project)
        db.session.commit()
        return f"项目创建成功:{project.project_name}"
    except KeyError as e:
        return f"项目创建失败,缺少关键参数:{e}",400

if __name__ == '__main__':
    app.run(debug=True)
