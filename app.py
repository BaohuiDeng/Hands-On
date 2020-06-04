from flask import Flask, render_template, request,session
from flask_mail import Mail, Message
from mongoengine import *
import bcrypt
from flask_pymongo import PyMongo 

from document import User
from login import LoginForm
from forms import RegisterForm
import local_setings




app = Flask(__name__,template_folder='template')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] ='Dengbaohuilea@gmail.com'
app.config['MAIL_PASSWORD'] = local_setings.MAIL_PASSWORD 
app.config['MAIL_DEFAULT_SENDER'] = 'Dengbaohuilea@gmail.com'
app.config['MAIL_MAX_EMAILS'] =  None
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.secret_key = 'development key'

mail = Mail (app)


connect('HandsOnSession', host='localhost', port=27017) #

@app.route('/')
def index():
    form=LoginForm()
    return render_template('login.html',form=form)




@app.route('/login', methods=['POST'])
def login():
        app.config['MONGO_DBNAME'] = 'HandsOnSession'
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/HandsOnSession'
        mongo = PyMongo(app)

        if request.method == 'POST':
            user = mongo.db.user
            login_user = user.find_one({'username' : request.form.get('username')})

            if login_user:
                    if bcrypt.checkpw(request.form.get('password').encode('utf-8'), login_user['password'].encode('utf-8')): 
                        session['username'] = request.form['username']
                        return 'You are logged in as ' + session['username']

            return 'Invalid username/password combination'



@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegisterForm() #
    if request.method =='POST':
        existing_user = User.objects.filter(username=request.form.get("username")).first()
        

        if existing_user is None:
            user = User(  #
            username=request.form.get("username"),
            email=request.form.get("email"),
            password=bcrypt.hashpw(request.form.get("password").encode('utf-8'),bcrypt.gensalt())
            )
            user.save()  
            
            recipient = request.form['email'] #
            msg = Message('Welcome to Hands-on session', recipients=[recipient])
            msg.body = ('Welcome to Flask part 2 Hands-on session')
            msg.html = ("<h2>Welcome! you have registered!</h2><b>\
            </b><br><h4>In this session you will learn more about Flask</h4>"
                )
            mail.send(msg)
            return 'you have successfully registered, check your email!'
        return 'That username already exists!'
    return render_template('signup.html',form=form)






if __name__ =='__main__':
  app.run(debug=True)
