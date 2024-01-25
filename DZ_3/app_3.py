from flask import render_template, request, Flask
from flask_wtf.csrf import CSRFProtect

from forms_3 import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = b'3c22c2862425a412a0e27ed0951638a83de0840a8f34a788984f9ca75a354af7'
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return 'Hi!'

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
