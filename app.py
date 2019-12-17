from flask import Flask,render_template,flash,redirect,url_for,request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import InputRequired,Email,Length,EqualTo
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user

app = Flask(__name__)

#Config
app.config['SECRET_KEY']='a random string'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
Bootstrap(app)
db = SQLAlchemy(app)

#login initialize
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Tables
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(),unique=True)
    email = db.Column(db.String(),unique=True)
    password = db.Column(db.String())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.create_all()


#Formlar
class LoginForm(FlaskForm):
    username = StringField('username',validators=[InputRequired()])
    password = PasswordField('password',validators=[InputRequired()])
    submit = SubmitField('Login')
class RegisterFrom(FlaskForm):
    username = StringField('username',validators=[InputRequired()])
    email = StringField('email',validators=[InputRequired(),Email()])
    password = PasswordField('password',validators=[InputRequired()])
    confirm_password = PasswordField('confirm_password',validators=[InputRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

#Routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/rooms',methods=['GET','POST'])
def rooms():
    if request.method == 'POST':
        indate = request.form.get('indate')
        outdate = request.form.get('outdate')
        roomtype = str(request.form.get('roomtype'))
        customer = str(request.form.get('customer'))
        search = indate+" "+ outdate + " "+ roomtype + " " + customer
        return search
    if request.method == 'GET':
        return render_template('rooms.html')
    return render_template('rooms.html')
@app.route('/roomdetail')
def roomdetail():
    return render_template('roomdetail.html')
@app.route('/about')
@login_required
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user)
                flash(f'You logged {form.username.data}','success')
        else:
            flash('Invald passwrod or username','error')
        
    return render_template('login.html',form=form)
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterFrom()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,method='sha256')
        new_user = User(username=form.username.data,email=form.email.data,password =hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}','success')
    return render_template('register.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



app.run(debug=True)