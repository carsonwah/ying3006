from flask import Flask, render_template, request, url_for, session, escape, redirect
import my_db as db

app = Flask(__name__)
# TODO 1: predict by uid, return stock ids
# TODO 2: use stock ids to grab stock news
# TODO 3: route to '/user', show profolio, suggested stocks, buy/sell, refresh
@app.route('/')
def index():
    if 'user' in session:
        # return 'Logged in as %s' % escape(session['user']['username'])
        return render_template('news_feed.html', name=session['user']['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = db.users[username]
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == "__main__":
    app.run()
