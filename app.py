import requests
import json
from flask import Flask, request, render_template


app = Flask(__name__)
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:"


@app.route('/', methods=['GET'])
def send_present():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/present', methods=["POST"])
def check_present():
    isbn = request.form["isbn"]
    req_url = GOOGLE_BOOKS_API_URL
    response = requests.get(req_url)
    data = json.loads(response.text)
    if data["totalItems"] != 1:
        return render_template("present.html", result=0)
    return render_template("present.html", result=1,
                           title=data["items"]["title"],
                           amazon="https://www.amazon.co.jp/dp/487311778X"
                           + isbn)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
