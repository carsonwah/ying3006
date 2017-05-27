from flask import Flask, render_template, request, url_for
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('news_feed.html', name="hihi")

@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run()
