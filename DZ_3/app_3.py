from hashlib import sha256

from flask import render_template, request, Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect

from DZ_3.templates.models_3 import db, User
from forms_3 import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = b'3c22c2862425a412a0e27ed0951638a83de0840a8f34a788984f9ca75a354af7'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/mydatabase.db'
db.init_app(app)

@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('ok')

@app.route('/')
def index():
    return 'Hi!'

@app.route('/forms/', methods=['GET', 'POST'])
def forms():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=sha256(form.password.data.encode(enkoding='utf-8')).hexdigest())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template(template_name_or_list='user.html', form=form)

@app.route('/main/')
def main():
    return 'Основная страница!'

@app.route('/data/')
def data():
    return 'Your data!'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
    # Обработка данных из формы
        pass
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
