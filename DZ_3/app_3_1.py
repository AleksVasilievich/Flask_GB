
from flask import Flask

from DZ_3.models_3_1 import db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

@app.route('/')
def index():
    return 'Hi!'

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')

@app.cli.command("add-john")
def add_user():
    user = User(username='john4', email='john4@example.com')
    db.session.add(user)
    db.session.commit()
    print('John add in DB!')

if __name__ == '__main__':
    app.run(debug=True)
