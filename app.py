from flask import Flask, render_template, request, url_for, redirect, session, flash
from functools import wraps
import os, time, datetime
import inspect

os.system("cls")
app = Flask(__name__)
try:
    app.config.from_object(os.environ['APP_SETTINGS'])
except:
    print("Erreur : Variable d'environnement *APP_SETTINGS* inconnue ! ")
    print()
    print("Pour mettre à jour l'environnement,")
    print("tapper : source .env")
    exit(1)

def log(*args, **kwargs):
    if args:
        print(now(), *args)
    else:
        print(now(), get_function_name())

def get_function_name(params=False):
    f_frame = inspect.currentframe()
    f = inspect.getouterframes(f_frame)[2]
    f_detail = f.frame.f_code
    if params:
        parametres = f_detail.co_varnames[:f_detail.co_argcount]
    else:
        parametres = "()"
    return "function {}{}".format( f_detail.co_name, parametres)
        
def now():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Vous devez d'abord vous connecter.")
            return redirect(url_for("login"))
        
    return wrap

@app.route("/")
@login_required
def home():
    log()
    return render_template("index.html", username=session.get("username",""))

@app.route("/welcome")
def welcome():
    log()
    return render_template("welcome.html")

@app.route("/login", methods=["GET","POST"])
def login():
    log()
    error = None    
    if request.method == "POST":
        username = request.form["username"]
        if (username ,request.form["password"]) != ("admin", "admin"):
            error = "Identifiant et/ou mot de passe invalide. "
            session["tentatives"] = session.get("tentatives", 0)  + 1
            time.sleep(session["tentatives"] * 2)

        else:
            log(f"User : {username}, succesfully connected")
            flash("Vous venez juste de vous connecter !")
            session["logged_in"] = True
            session["username"] = username
            session["tentatives"] = 0
            
            return redirect(url_for("home"))
            
    elif session.get("tentatives",0) > 2:
        error = "Trop de tentatives invalides. Connexion désactivée"
        
    if error:
        log(f"Error : {error}")
        
    return render_template("login.html", error=error)

@app.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    log()
    username = session.get("username", "")
    session.pop("logged_in", None)
    session.pop("username", None)
    session.pop("tentatives", None)
    flash("Vous venez juste de vous déconnecter !")
    log(f"User : {username}, successfully disconnected")
    
    return redirect(url_for("welcome"))

@app.route("/<name>")
def hello_name(name):
    log()
    log(" : {name}")
    return "Hello {} !".format(name)


if __name__ == '__main__':
    print("Run with", os.environ['APP_SETTINGS'])
    print()
    app.run(debug=True)

