from flask import Flask, render_template, request, url_for, session, escape, redirect, jsonify
import my_db as db
import latent

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import io

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
        prediction = model.predict(session['user']['id'])
        session['prediction_indexes'] = list(prediction.columns.values)
        print session['prediction_indexes']
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/portfolio', methods=['GET'])
def portfolio():
    # TODO: return JSON: user's portfolio list, suggested top 5
    user_portfolio = get_user_portfolio(session['user']['id'])
    print user_portfolio
    return render_template('portfolio.html', name=session['user']['username'], portfolios=user_portfolio)

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
    return render_template('news_feed.html', news=db.news['0017'])

def get_user_portfolio(userid):
    user_row = model.R[userid]
    user_portfolio_index = []
    for i in xrange(len(user_row)):
        if user_row[i] != 0:
            user_portfolio_index += [i]
    user_portfolio = {}
    for index in user_portfolio_index:
        stock_code = codes[index]
        stock_name = names[index]
        stock_price = prices[index]
        stock_percentage_change = percentage_changes[index]
        user_portfolio[stock_code] = {'name':stock_name,'price':stock_price,'percentage_change':stock_percentage_change}
    return user_portfolio

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    model = latent.LatentFactorModel()
    f = io.open('./stock_info.txt','r', encoding='utf8')
    codes = map(lambda x: x[0:4], f.readline().strip().split('\t'))
    names = f.readline().strip().split('\t')
    prices = f.readline().strip().split('\t')
    percentage_changes = f.readline().strip().split('\t')
    f.close()
    app.run()
