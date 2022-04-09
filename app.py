
from flask import Flask, redirect, render_template, request, url_for, abort, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from io import BytesIO
import sqlalchemy

app = Flask(__name__)

app.secret_key = 'sssssrfgvv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Alibaba2022@localhost/prototype'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
usmail = "siva@gmail.com"


class Image(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    mime = db.Column(db.String, nullable=False)
    uname = db.Column(db.String, nullable=False)
    umail = db.Column(db.String, nullable=False)


class info(db.Model):
    __tablename__ = 'usinfo'
    id = db.Column(db.Integer, primary_key=True)
    umail = db.Column(db.Text, nullable=False)
    uspass = db.Column(db.Text, nullable=False)


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        uname = request.form.get("user_name")
        umail = request.form.get("user_email")
        file = request.files['file']

        img = Image(
            name=secure_filename(file.filename),
            mime=file.mimetype,
            data=file.read(),
            uname=uname,
            umail=umail
        )
        db.session.add(img)
        db.session.commit()
        userImg = Image.query.filter_by(umail=umail).first()

        return render_template("base.html", uname=uname, imga=userImg)

    return render_template("index.html")


@app.route('/download/<int:image_id>')
def download(image_id):
    img = Image.query.get_or_404(image_id)
    return send_file(
        BytesIO(img.data),
        mimetype=img.mime,
        attachment_filename=img.name
    )


@app.route("/success", methods=["POST", "GET"])
def success():
    passinp = request.form.get("xy")
    tolerance = request.form.get("tol")
    user = info(
        umail=usmail,
        uspass=passinp
    )
    db.session.add(user)
    db.session.commit()
    return render_template("success.html", msg="Account created")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        dummy = request.form.get("ur_email")
        usmail = dummy
        userImg = Image.query.filter_by(umail=dummy).first()
        return render_template("a.html", imga=userImg)
    return render_template("login.html")


@app.route("/dash", methods=["POST", "GET"])
def authenticate():
    ct = 0
    reqUser = info.query.filter_by(umail=usmail).first()
    passdata = (reqUser.uspass)
    coordinates = passdata.split()
    print(coordinates)
    loginuser = request.form.get("passxy")
    logco = (loginuser.split())
    for i in range(len(coordinates)):
        if int(logco[i]) >= int(coordinates[i])-20 and int(logco[i]) <= int(coordinates[i])+20:
            ct = ct+1
    if ct == 6:
        return render_template("success.html", msg="You are successfully logged in ")
    return render_template("success.html", msg="Sorry, you're unathenticated")


if __name__ == "__main__":
    app.run(debug=True)
