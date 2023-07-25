#apps/crud/views.py
import pdb
from apps.app import db
from apps.back_app.models import Todo
import json
from flask import Flask,Blueprint,render_template,redirect,jsonify,url_for,request
# from apps.crud.forms import UserForm
# #app.pyで作成のflask-SQLAlchemyインスタンスであるdbとモデルのクラスをインポート
# from apps.app import db
# from apps.crud.models import User
# #ログイン必須化のためにflask_loginからlogin_requiredをインポート
# from flask_login import login_required
#ブループリントを作成
# url_prefixを追加したBlueprintオブジェクトを作成
# back_app = Blueprint("back_app",__name__,url_prefix="/back_app",template_folder='templates',static_folder='static')
back_app = Blueprint("back_app",__name__,url_prefix="/back_app")
@back_app.route("/alltask",endpoint="alltask")
#todo全件表示用ルート
def alltask():
  #dbより全件select
  todos=db.session.query(Todo).all()
  todos_list=todos_list_to_dict(todos)
  #辞書をjsonifyにいれる
  return jsonify({"flask-- @back_app.route(/alltask)":"is finished","todos_list":todos_list})
#todoオブジェクトを要素とするリストをリスト・辞書に変形
def todos_list_to_dict(todos):
  print("---todos_list_to_dict--todos=",todos)
  todos_list = []
  for todo in todos:
    todo_dict = {}
    for column in Todo.__table__.columns:
      key = column.name
      value = getattr(todo, key)
      todo_dict[key] = value
    todos_list.append(todo_dict)
  return todos_list
#todo1件表示用ルート・editボタン押下時
@back_app.route("/showtask/<taskid>",endpoint="showtask")
def showtask(taskid):
  #dbより1件select
  todo=db.session.query(Todo).filter(Todo.id==taskid).first()

  todos_list=todos_list_to_dict([todo])
  return jsonify({"flask-- @back_app.route(/showtask/"+taskid+")":"is finished","todos_list":todos_list})
#todo削除用ルート
@back_app.route("/deletetask/<taskid>",methods=["DELETE"],endpoint="deletetask")
def deletetask(taskid):
  #dbより1件select
  todo=db.session.query(Todo).filter(Todo.id==taskid).first()
  #deleteしてcommitします。
  db.session.delete(todo)
  db.session.commit()
  db.session.close()
  print("---DELETED_task"+taskid+"---")
  return jsonify({"flask-- @back_app.route(/delete/"+taskid+")":"is finished"})
#todo新規作成用ルート
@back_app.route("/createtask",methods=["POST"],endpoint="createtask")
def createtask():
  #渡されたjsonデータから値を取りだす
  newtaskstr = request.json["newtaskstr"]
  if newtaskstr.encode("utf-8") == b'':
    #入力欄が空文字
    print("newtaskstr is blankdata",newtaskstr)
    return jsonify({"flask-- @back_app.route(/createtask":" str is blank"})
  else:
    #INSERTするUserクラスインスタンス
    newtodo=Todo(task=newtaskstr)
    #INSERT文
    db.session.add(newtodo)
    # COMMITしないと反映されません
    db.session.commit()
    #DB書き込み後は適当なjsonを返す
    return jsonify({"flask-- @back_app.route(/createtask":"is finished"})
#todoタスク記入内容更新用ルート
@back_app.route("/updatetask",methods=["POST"],endpoint="updatetask")
def updatetask():
  #渡されたjsonデータから値を取りだす
  newtaskstr = request.json["newtaskstr"]
  editingTodo=request.json["editingTodo"]
  if newtaskstr.encode("utf-8") == b'':
    #入力欄が空文字
    print("newtaskstr is blankdata",newtaskstr)
  elif newtaskstr==editingTodo["task"]:
    #入力欄が変更されていない
    print("newtaskstr == editintTodo['task']")
  else:
    #入力されていて、かつ前の入力内容と差がある場合は変更します。
    #dbより1件selectします。editingTodoはただの辞書であり、Todoオブジェクトじゃないです。
    todo=db.session.query(Todo).filter(Todo.id==editingTodo["id"]).first()
    todo.task=newtaskstr
    db.session.commit()
    db.session.close()
    #DB書き込み後は適当なjsonを返す
  return jsonify({"flask-- @back_app.route(/updatetask":"is finished"})
#todoチェック内容更新用ルート
@back_app.route("/changechecktask",methods=["POST"],endpoint="changechecktask")
def changechecktask():
  #渡されたjsonデータから値を取りだす
  editingTodo=request.json["editingTodo"]
  
  #dbより1件selectします。editingTodoはただの辞書であり、Todoオブジェクトじゃないです。
  todo=db.session.query(Todo).filter(Todo.id==editingTodo["id"]).first()
  print("changechecktask--todo.check=",todo.checked," editingTodo['checked']=",editingTodo['checked'])
  todo.checked=editingTodo["checked"]
  db.session.commit()
  db.session.close()
  #DB書き込み後は適当なjsonを返す
  return jsonify({"flask-- @back_app.route(/changechecktask":"is finished"})
