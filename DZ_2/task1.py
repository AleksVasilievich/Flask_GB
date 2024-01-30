from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/welcome')
def welcome():
    username = request.cookies.get('username')
    return render_template('index1.html', username=username)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('username', '', expires=0)
    return resp

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['name']
    email = request.form['email']
    resp = make_response(redirect(url_for('welcome')))
    resp.set_cookie('username', username)
    return resp

if __name__ == '__main__':
    app.run(debug=True)