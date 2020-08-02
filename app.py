import os, time, datetime
import inspect 

from functools import wraps
from models import app, BlogPost

try:
    from flask import render_template, request, url_for, redirect, session, flash
    
except Exception as e:
    print("Error:", e)
    print()
    print("L'environnement n'est pas à jour\n")
    print("Pour mettre à jour l'environnement,")
    print("tapper : source .setup")
    exit(1)
    
#os.system("cls")

def log(*args, **kwargs):
    if args:
        print(now(), *args, flush=True)
    else:
        print(now(), get_function_name(),flush=True)

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
    posts = BlogPost.query.filter(BlogPost.id == 1)
    
    return render_template("index.html", username=session.get("username",""), posts=posts)

@app.route("/welcome")
def welcome():
    os.system("cls")
    log()
    
    return render_template("welcome.html", username=session.get("username",""))

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
        log(f"Erreur : {error}")
        
    return render_template("login.html", error=error)

@app.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    log()
    username = session.get("username", "")
    session.clear()
    flash("Vous venez juste de vous déconnecter !")
    log(f"User : {username}, successfully disconnected")
    
    return redirect(url_for("welcome"))

@app.route("/<name>")
def hello_name(name):
    log()
    log(f"looking for /{name}")
    
    return "/{} is not accessible !".format(name)

@app.route("/<name1>/<name2>")
def hello_names(name1, name2):
    log()
    log(f"looking for /{name1}/{name2}")
    
    return "/{}/{} is not accessible !".format(name1, name2)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=["GET","POST"])
@login_required
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
    
    
if __name__ == '__main__':
    # app.run() 
    app.run(debug=True) 
