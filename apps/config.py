import os

#.envファイルからdotenvを使い環境変数として読み込む
from pathlib import Path
from dotenv import load_dotenv

#各段階のconfigの基礎となる部分
class BaseConfig:
  
  JSON_AS_ASCII=False
#開発段階のconfig(BaseConfigを継承)
class LocalConfig(BaseConfig):
  #このファイルの親の親ディレクトリを指定(←その中に.envがあるから)
  basedir=Path(__file__).parent.parent
  dotenv_path = os.path.join(basedir, 'dev.env')
  load_dotenv(dotenv_path)
  
  mysql_root_password=os.getenv("MYSQL_ROOT_PASSWORD")
  mysql_user=os.getenv("MYSQL_USER")
  mysql_password=os.getenv("MYSQL_PASSWORD")
  mysql_database=os.getenv("MYSQL_DATABASE")
  mysql_endpoint=os.getenv("MYSQL_ENDPOINT")
  secret_key=os.getenv("SECRET_KEY")
  
  print("--LocalConfig---")
  
  SQLALCHEMY_DATABASE_URI = 'mariadb+pymysql://'+mysql_user+':'+mysql_password+'@'+mysql_endpoint+'/'+mysql_database
  print("SQLALCHEMY_DATABASE_URI=",SQLALCHEMY_DATABASE_URI)
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO = True
  SECRET_KEY=secret_key
#本番用のconfig(BaseConfigを継承)
#テスト用段階だったらCSRF対策を無効にするため「WTF_CSRF_ENABLED = False」にしたりも
class ProdConfig(BaseConfig):
  #このファイルの親の親ディレクトリを指定(←その中に.envがあるから)
  basedir=Path(__file__).parent.parent
  dotenv_path = os.path.join(basedir, '.env')
  load_dotenv(dotenv_path)


  mysql_root_password=os.getenv("MYSQL_ROOT_PASSWORD")
  mysql_user=os.getenv("MYSQL_USER")
  mysql_password=os.getenv("MYSQL_PASSWORD")
  mysql_database=os.getenv("MYSQL_DATABASE")
  mysql_endpoint=os.getenv("MYSQL_ENDPOINT")
  secret_key=os.getenv("SECRET_KEY")
  print("mysql_endpoint=",mysql_endpoint)
  print("-=-=-ProdConfig-=-=-")
  SQLALCHEMY_DATABASE_URI = 'mariadb+pymysql://'+mysql_user+':'+mysql_password+'@'+mysql_endpoint+'/'+mysql_database
  # SQLALCHEMY_DATABASE_URI=f"sqlite:///{basedir/'testing.sqlite'}"
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO = True
  SECRET_KEY=secret_key
#辞書の中身は上のクラスを値にもつ キーが指定されたら、対応する設定値になる
config={"local":LocalConfig,"product":ProdConfig}