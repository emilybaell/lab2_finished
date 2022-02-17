import random
from flask import Flask, jsonify, request
import database_helper

app = Flask(__name__)
app.debug = True


@app.route("/")
def home(): 
    return "Hello, Flask!"

@app.route("/sign_in", methods=['PUT']) 
def sign_in():
    json = request.get_json()
    if("email" in json and "password" in json):
        user=database_helper.find_user(json['email'])
        if(user and (json['password'] == (user[0])[1])):
            letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            token=''.join((random.choice(letters))for x in range(36))
            result=database_helper.give_token((user[0])[0], token)
            return jsonify(token), 200
        else:
            return "{}", 500
    else:
        return "{}",400 

@app.route("/sign_up", methods = ['PUT'])
def sign_up():
    json = request.get_json()
    isuser=database_helper.find_data_byemail(json['email'])

    if(not isuser and "email" in json and "password" in json and "firstname" in json and "familyname" in json and "gender" in json and "city" in json and "country" in json):
        if(len(json['password'])>=8):
            result=database_helper.create_profile(json['email'],json['password'],json['firstname'],json['familyname'],json['gender'],json['city'],json['country'])
            if(result==True):
                return "{}", 201
            else:
                return "{}", 500
        else:
            return "{}", 400
    else:
        return "{}",400

@app.route("/sign_out", methods=['GET'])
def sign_out():
    json = request.headers['token']
    if(json):
        user=database_helper.find_user_bytoken(json)
        if(user):
            result=database_helper.give_token((user[0])[0], 'NULL')
            return "{}", 200
        else:
            return "{}", 500
    else:
        return "{}",400

@app.route("/Change_password", methods=['PUT'])
def Change_password():
    json = request.get_json()
    tok = request.headers['token']

    if(tok and "oldPassword" in json and "newPassword" in json):
        user=database_helper.find_user_bytoken(tok)
        if((user[0])[1]==json['oldPassword'] and len(json['newPassword'])>=8):
            result=database_helper.changepswrd((user[0])[0], json['newPassword'])
            return "{}", 200
        else:
            return "{}", 500
    else:
        return "{}", 400


@app.route("/get_user_data_by_token", methods=['GET'])
def get_user_data_by_token():
    json = request.get_json()
    tok = request.headers['token']

    if(tok):
        user=database_helper.find_data_bytoken(tok)
        if(user):
            return jsonify(user[0]), 200
        else:
            return "{}", 500
    else:
        return "{}", 400

@app.route("/get_user_data_by_email", methods=['GET'])
def get_user_data_by_email():    
    json = request.get_json()
    tok = request.headers['token']

    if(tok and "email" in json):
        hastoken=database_helper.find_data_bytoken(tok)
        user=database_helper.find_data_byemail(json['email'])
        if(user and hastoken):#kolla om token är giltig
            return jsonify(user[0]), 200
        else:
            return "{}", 500
    else:
        return "{}", 400

 
@app.route("/Get_user_messages_by_token", methods=['GET'])
def Get_user_messages_by_token():
    tok = request.headers['token']

    if(tok):
        user=database_helper.find_user_bytoken(tok)
        if(user):
            msgs=database_helper.find_msgs_byemail((user[0])[0])
            return jsonify(msgs), 200
        else:
            return "{}", 500
    else:
        return "{}", 400

@app.route("/get_user_messages_by_email",methods=['GET'])
def get_user_messages_by_email():
    json = request.get_json()
    tok = request.headers['token']

    if(tok and "email" in json):
        user=database_helper.find_data_byemail(json['email'])
        hastoken=database_helper.find_data_bytoken(tok)

        if(user and hastoken): #här med!
            msgs=database_helper.find_msgs_byemail((user[0])[0])
            return jsonify(msgs), 200
        else:
            return "{}", 500
    else:
        return "{}", 400

@app.route("/post_message",methods=['PUT'])
def post_message():
    json = request.get_json()
    tok = request.headers['token']
    
    if(tok and "message" in json and "email" in json):
        user=database_helper.find_user_bytoken(tok)
        isuser=database_helper.find_data_byemail(json['email'])
        if(user and isuser): 
            msgs=database_helper.post_it((user[0])[0],json['email'] ,json['message'])
            return "{}", 201
        else: 
            return "{}", 500
    else:
        return "{}", 400



if __name__=="__main__":
    app.run()