import os
import json
import sqlite3
from db import save_details, show_table
from flask import Flask, redirect, url_for, render_template, request, session, current_app
from flask_dance.contrib.google import make_google_blueprint, google

def get_creds():
    fp = open("./creds.json", "r")
    creds = json.load(fp)
    client_id = creds["web"]["client_id"]
    client_secret = creds["web"]["client_secret"]
    return client_id, client_secret

app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
client_id, client_secret = get_creds()
path = os.getcwd()
uploadDirPath = os.path.join(path, 'data')

def allowedFile(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() == "json"

google_bp = make_google_blueprint(
    client_id = client_id,
    client_secret = client_secret,
    scope=["profile", "email"]
)
app.register_blueprint(google_bp, url_prefix="/login")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        File = request.files['file']
        if allowedFile(File.filename):
            File.save(os.path.join(uploadDirPath, File.filename))
            fp = open(os.path.join(uploadDirPath, File.filename), "r")
            data = json.load(fp)
            for row in data:
                save_details(tuple(row.values()))
            return "File upload Success"
        else:
            return "File upload Failed"

def _empty_session():
    if 'google' in current_app.blueprints and hasattr(current_app.blueprints['google'], 'token'):
        del current_app.blueprints['google'].token
    session.clear()

@app.route("/logout")
def logout():
    if google.authorized:
        try:
            google.get('https://accounts.google.com/o/oauth2/revoke',
                params = { 'token': current_app.blueprints['google'].token['access_token']}
            )
        except:
            pass
    _empty_session()
    return redirect(url_for('index'))

@app.route("/getData")
def show_data():
    data = show_table()
    return render_template("data.html", data = data)

@app.route("/google_login")
def google_login():
    return redirect(url_for("google.login"))

@app.route("/")
def index():
    if not google.authorized:
        return render_template("login.html")
    else:
        return render_template("index.html")

app.run(debug = True)