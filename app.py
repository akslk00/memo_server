from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.memo import MemoReigsterResource, MemoResource

from resources.user import FrindResource, UserLoginResource, UserReigsterResource

app = Flask(__name__)

api = Api(app)

app.config.from_object(Config)

jwt = JWTManager(app)


# 경로와 리소스 연결
api.add_resource(UserReigsterResource,'/user/register')

api.add_resource(UserLoginResource,'/user/login')

api.add_resource(MemoReigsterResource,'/memo')

api.add_resource(MemoResource,'/memo/<int:Memo_id>')

api.add_resource(FrindResource,'/user/<int:user_id>')

if __name__ == '__main__' :
    app.run()