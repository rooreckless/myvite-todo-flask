#下のimportしたdbはapp.pyで作成した変数でflask_alchemyオブジェクト
# from apps.app import db , login_manager
from apps.app import db
#datetaime型を使う場合importしてきます。
from datetime import datetime
#入力されたパスワードを平文のままにせず、ハッシュ値をデータベースに残すための関数をimport
from werkzeug.security import generate_password_hash,check_password_hash
# from flask_login import UserMixin

class Todo(db.Model):
  #このクラスが扱うテーブル名
  __tablename__ = "todos"
  #カラムを定義 db.Columnオブジェクトをカラム数分用意し1個ずつ変数化
  id = db.Column(db.Integer,primary_key=True, autoincrement=True)
  task=db.Column(db.String(255), nullable=False)
  checked=db.Column(db.Boolean, nullable=False,default=False)
  created_at=db.Column(db.DateTime,default=datetime.now, nullable=False)
  updated_at=db.Column(db.DateTime,default=datetime.now, nullable=False,onupdate=datetime.now)

# class User(db.Model,UserMixin):
# class User(db.Model):
#   __tablename__ = "users"
#   #カラムを定義 db.Columnオブジェクトをカラム数分用意し1個ずつ変数化
#   id = db.Column(db.Integer,primary_key=True)
#   username=db.Column(db.String(255), index=True)
#   email=db.Column(db.String(255), unique=True, index=True)

#   password_hash = db.Column(db.String(255))
  
#   created_at=db.Column(db.DateTime,default=datetime.now)
#   updated_at=db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

#   # パスワードのゲッター
#   # しかしゲッターをつかってのアクセスはできないようにエラーを返します。
#   @property
#   def password(self):
#     raise AttributeError("読み取り不可")
  
#   # セッター password=〇〇でここが起動する
#   # importした関数を使ってハッシュ化したパスワードを、このクラスの属性password_hashにセットします。
#   @password.setter
#   def password(self,password):
#     self.password_hash =generate_password_hash(password)
  
#   #パスワードチェック用メソッド
#   def verify_password(self, password):
#     #引数のpasswordと、Userクラスのインスタンスが持つpassword_hashが一致するかを返します。
#     return check_password_hash(self.password_hash,password)
#   #メールアドレスが重複していないかチェック用
#   def is_duplicate_email(self):
#     #このメソッドを起動したモデルインスタンスが持つemailプロパティでDBを検索し、
#     # #NoneだったらFalseを返す = 重複していないということ
#     return User.query.filter_by(email=self.email).first() is not None

# # @login_manager.user_loader
# # def load_user(user_id):
# #     return User.query.get(user_id)