from flask import Flask,request,jsonify
from model import User
from util import *

app = Flask(__name__)
user = User()

user.create_user("TaroYamada","PasSwd4TY","たろー","僕は元気です")

@app.route('/signup',methods=["POST"])
def signup():
    data = request.json
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        return jsonify({"message":"Account creation failed","cause":"Required user_id and password"}),400
    if len(user_id) < 6 or 20 < len(user_id) or not user_id.isalnum():
        return jsonify({"message":"Account creation failed","cause":"Input length is incorrect"}),400
    if len(password) < 8 or 20 < len(password):
        return jsonify({"message":"Account creation failed","cause":"Input length is incorrect"}),400

    try:
        user.create_user(user_id,password)
        return jsonify({
            "message": "Account successfully created",
            "user": {
                "user_id": user_id,
                "nickname": user_id
            }
        }),200
    except ValueError:
        return jsonify({
            "message": "Account creation failed",
            "cause": "Already same user_id is used"
        }),400
    
@app.route('/users/<user_id>',methods=["GET"])
def get_user(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not authenticate(auth_header,user):
        return jsonify({ "message":"Authentication failed" }),401
    
    user = user.get_user(user_id)
    if not user:
        return jsonify({ "message":"No user found" }),404
    
    res = {
        "message": "User details by user_id",
        "user": {
            "user_id": user_id,
            "nickname": user["nickname"] or user_id,
            "comment": user.get("comment","")
        }
    }
    return jsonify(res),200

@app.route("/users/<user_id>",methods=["PATCH"])
def update_user(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not authenticate(auth_header,user):
        return jsonify({ "message":"Authentication failed" }),401
    
    data = request.json
    nickname = data.get("nickname")
    comment = data.get("comment")

    if nickname == "" or comment == "":
        nickname = user_id  if nickname == "" else nickname
        comment = "" if comment == "" else comment
    if not(nickname or comment):
        return jsonify({
            "message": "User updation failed",
            "cause": "Required nickname or comment"
        }),400
    
    user = user.update_user(user_id,nickname,comment)
    if not user:
        return jsonify({ "message":"No user found" }),404
    return jsonify({
        "message": "User successfully updated",
        "user": user
    }),200

@app.route("/close",methods=["POST"])
def delete_account():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not authenticate(auth_header,user):
        return jsonify({ "message":"Authentication failed" }),401
    user_id,_ = encode_auth(auth_header)
    user.delete_user(user_id)
    return jsonify({  "message": "Account and user successfully removed" }),200


if __name__ == "__main__":
    app.run(debug=True)


    

