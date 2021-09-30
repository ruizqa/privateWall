from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user
from flask_app.models import message
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
#import datetime to change date format


@app.route("/")
def form():
    return render_template("create.html")

@app.route('/register', methods=["POST"])
def create_user():
    if not request.form:
        flash("Please register", "register")
        return redirect("/")
    if not user.User.validate_user(request.form):
        # we redirect to the template with the form.
            return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    
    data = {
        "first_name": request.form["fname"],
        "last_name" : request.form["lname"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    
    # We pass the data dictionary into the save method from the User class.
    id= user.User.save(data)

    # Don't forget to redirect after saving to the database.
    session['user_id'] = id
    return redirect('/wall')            

@app.route('/login', methods=["POST"])
def login_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    if not request.form:
        flash("Please login", "login")
        return redirect("/")

    if not user.User.validate_login(request.form):
        # we redirect to the template with the form.
            return redirect('/')

    data = {
        "email" : request.form["email"],
        "password" : request.form["pw"]
    }

    user_e= user.User.login(data)
    print(user_e)
    if not user_e:
        return redirect('/')
    elif not bcrypt.check_password_hash(user_e.password, data['password']):
        flash("The password is incorrect", "login")
        return redirect('/')
    session['user_id'] = user_e.id
    # Don't forget to redirect after saving to the database.
    return redirect('/wall')  


@app.route("/wall")
def read():
    if not 'user_id' in session:
        flash("Please login to access the site","login")
        return redirect("/")
    users = user.User.get_all_users({'id': session['user_id']})
    user_e= user.User.get_user_info({'id':session['user_id']})
    user_e.get_user_messages()

    return render_template("wall.html", user=user_e, users=users)

@app.route("/delete/<int:m>")
def delete(m):
    if not 'user_id' in session:
        flash("Please login to access the site","login")
        return redirect("/")
    message.Message.delete({'id': m})
    return redirect("/wall")

@app.route("/send", methods=["POST"])
def send():
    if not 'user_id' in session:
        flash("Please login to access the site","login")
        return redirect("/")
    message.Message.send(request.form)
    return redirect("/wall")


@app.route("/logout")
def clearsession():
    session.clear()
    return redirect('/')