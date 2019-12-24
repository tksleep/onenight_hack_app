import requests
import json
import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/present"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)


@app.route('/', methods=['GET'])
def send_present():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/sendpresent', methods=["POST"])
def check_present():
    isbn = request.form["isbn"]
    req_url = GOOGLE_BOOKS_API_URL + isbn
    response = requests.get(req_url)
    data = json.loads(response.text)
    if data["totalItems"] != 1:
        return render_template("sendpresent.html", result=False)
    else:
        present = Data()
        present.name = request.form["name"]
        present.title = data["items"][0]["volumeInfo"]["title"]
        present.url = "https://www.amazon.co.jp/dp/" + isbn
        db.session.add(present)
        db.session.commit()
        return render_template("sendpresent.html", name=request.form["name"],
                               result=True,
                               title=data["items"][0]["volumeInfo"]["title"],
                               amazon="https://www.amazon.co.jp/dp/"
                               + isbn)


@app.route('/getpresent', methods=["POST"])
def get_present():
    got_present = db.session.query(Data).order_by(db.func.random()).first()
    print(got_present)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
