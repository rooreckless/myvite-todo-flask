#back_app/apps/config.py
import os
from pathlib import Path
# basedir=Path(__file__).parent.parent

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__).parent.parent, '.env')
load_dotenv(dotenv_path)


mysql_root_password=os.getenv("MYSQL_ROOT_PASSWORD")
mysql_user=os.getenv("MYSQL_USER")
mysql_password=os.getenv("MYSQL_PASSWORD")
mysql_database=os.getenv("MYSQL_DATABASE")
mysql_endpoint=os.getenv("MYSQL_ENDPOINT")
secret_key=os.getenv("SECRET_KEY")


#各段階のconfigの基礎となる部分
class BaseConfig:
  SECRET_KEY=secret_key
  JSON_AS_ASCII=False
#開発段階のconfig(BaseConfigを継承)
class LocalConfig(BaseConfig):
  print("mysql_user=",mysql_user)
  print("mysql_password",mysql_password)
  print("mysql_database=",mysql_database)
  print("mysql_endpoint=",mysql_endpoint)
  SQLALCHEMY_DATABASE_URI = 'mariadb+pymysql://'+mysql_user+':'+mysql_password+'@'+mysql_endpoint+'/'+mysql_database
  
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO = True
  
#本番用のconfig(BaseConfigを継承)
#テスト用段階だったらCSRF対策を無効にするため「WTF_CSRF_ENABLED = False」にしたりも
class ProdConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = 'mariadb+pymysql://'+mysql_user+':'+mysql_password+'@'+mysql_endpoint+'/'+mysql_database
  # SQLALCHEMY_DATABASE_URI=f"sqlite:///{basedir/'testing.sqlite'}"
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO = True
#辞書の中身は上のクラスを値にもつ キーが指定されたら、対応する設定値になる
# config={"testing":TestingConfig,"local":LocalConfig}
config={"local":LocalConfig,"product":ProdConfig}