from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('register1.html')

@app.route('/register', methods=['POST'])
def register():
    # Получение данных из формы
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Хеширование пароля
    hashed_password = generate_password_hash(password)

    # Сохранение данных в базе данных
    # В этом месте необходимо использовать Вашу логику для сохранения данных в БД

    return 'Регистрация успешно завершена!'

if __name__ == '__main__':
    app.run()