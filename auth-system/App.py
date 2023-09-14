from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import re



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db.sqlite3'
app.config['SECRET_KEY'] = "authentication Mission"
db = SQLAlchemy(app)



# ---------------------------------------------------------------------------------------------------- #

class Users(db.Model):
    user_id = db.Column("UserID", db.Integer, primary_key = True)
    user_name = db.Column("UserName", db.String(20), nullable = False)
    password = db.Column("Password", db.String(20), nullable = False)

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

# ---------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------------------------------- #

@app.route("/register", methods = ["POST"])
def Register():
    if request.method == "POST":
        info = request.json
        user_name = str(info["user_name"])
        password = str(info["password"])

        if len(user_name) > 20 or len(password) > 20:
            return ("Username or password are too long.")
        
        regex = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        comp = re.compile(regex)
        proper = re.search(comp, password)
        if proper:
            if re.match("^[A-Za-z0-9_-]*$", user_name):
                new_user = Users(user_name, password)
                db.session.add(new_user)
                db.session.commit()
                return (f"Successfully registered under the details:\nUsername: '{user_name}',\nPassword: '{password}'.")
            else: return ("Username must include only numbers and characters.")
        else: return ("Password invalid.\nMinimum 8 characters, at least one letter and one number")


@app.route("/login", methods = ["GET"])
def Login():
    if request.method == "GET":
        info = request.json
        user_name = info["user_name"]
        password = info["password"]

        user_names = Users.query.filter_by(user_name = user_name).all()
        passwords = Users.query.filter_by(password = password).all()

        if user_names:
            if passwords:
                return (f"Welcome {user_name}!")
            else: return ("Wrong username or password.")
        else: return ("Wrong username or password.")


@app.route("/user_delete", methods = ["DELETE"])
def user_delete():
    if request.method == "DELETE":
        user_id = request.json["user_id"]

        filtered_user = Users.query.get(user_id)
        if filtered_user:
            db.session.delete(filtered_user)
            db.session.commit()
            return (f"'{filtered_user.user_name}' was deleted successfully.")
        else: return ("There is not such a user.")

# ---------------------------------------------------------------------------------------------------- #
        


if __name__ == '__main__':
    with app.app_context():
     	db.create_all()
app.run(debug = True)