from flask import Flask, render_template, request, url_for, session, escape, redirect, jsonify
import my_db as db
import latent

app = Flask(__name__)
@app.route('/')
def index():
    if 'user' in session:
        # TODO 2: use stock ids to grab stock news
        return render_template('news_feed.html', name=session['user']['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = db.users[username]
        session['prediction'] = model.predict(session['user']['id'])
        print session['prediction']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/portfolio')
def portfolio():
    # TODO: return JSON: user's portfolio list, suggested top 5
    return render_template('portfolio.html', name=session['user']['username'])

@app.route('/buy', methods=['POST'])
def buy():
    code = request.form['code']
    share = request.form['share']
    model.update_user_by_code(session['user']['id'], code, float(share))
    model.update()
    session['prediction'] = model.predict()
    return 'ok'

@app.route('/sell', methods=['POST'])
def sell():
    code = request.form['code']
    share = request.form['share']
    model.update_user_by_code(session['user']['id'], code, -float(share))
    model.update()
    session['prediction'] = model.predict()
    return 'ok'

@app.route('/news_feed')
def news_feed():
    # remove the username from the session if it's there
    return render_template('news_feed.html')


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    model = latent.LatentFactorModel()
    f = open('./stock_info.txt','r')
    indexes = map(lambda x: x[0:4], f.readline().strip().split('\t'))
    names = f.readline().strip().split('\t')
    prices = f.readline().strip().split('\t')
    percentage_changes = f.readline().strip().split('\t')
    f.close()
    app.run()
