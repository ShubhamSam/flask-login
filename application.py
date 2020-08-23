from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from form_feilds import *
from modal import *

# configure app
app = Flask(__name__)
app.secret_key = 'shubham'

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/chat_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=["GET", 'POST'])
def index():
    reg_form = RegistrationForm()

    # Update the database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data  # flask wtf syntax

        # Hash Password
        hased_pswd = pbkdf2_sha512.hash(password)

        # check username exists
        # user_object = User.query.filter_by(username=username).first()
        # if user_object:
        #     return 'Someone else has taken this username!'

        # Add user to database
        user = User(username=username, password=hased_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('index.html', form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)
        # if current_user.is_authenticated:
        #     return 'Logged in Successfully!'
        # return 'Not Logged In!'
        return redirect(url_for('chat'))
    else:
        return render_template('login.html', form=login_form)

@app.route('/chat', methods=['GET', 'POST'])
# @login_required
def chat():

    if not current_user.is_authenticated:
            return 'Please login before accessing chat!'

    return 'Chat with me'



@app.route('/logout', methods=['GET'])
def logout():
    logout_user()

    return 'Logged out using flask-login!'


if __name__ == "__main__":
    app.run(debug=True)
