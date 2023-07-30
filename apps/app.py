#app.py
#config切り替えにはconfig.pyのconfig辞書が使えればいい。
# from apps.config import config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# #SQLAlchemyをインスタンス化
db=SQLAlchemy()
#ブループリントback_appのviews.pyをインポート
from apps.back_app import views


def create_app(config_key):
  app=Flask(__name__)
  app.register_blueprint(views.back_app,url_prefix="/back_app")

  # app.config.from_object(config[config_key])
  if config_key=="product":
    print("create_app----config_key=",config_key)
    app.config.from_pyfile("../.env.py")
  elif config_key=="local":
    print("create_app----config_key=",config_key)
    app.config.from_pyfile("../dev.env.py")
  else:
    print("create_app----config_key=",config_key)
    app.config.from_pyfile("../dev.env.py")
  #SQLAlchemyとアプリを連携する初期化
  db.init_app(app)
  # #Migrateインスタンス作成 appとdbを入れて連携させる
  Migrate(app,db)
  
  

  CORS(app, resources={"/back_app/*":{"origins":"http://tmp/gunicorn_flask.sock"}})

  return app
if __name__=="__main__":
    app=create_app()