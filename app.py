from flask import Flask, render_template, request, url_for, redirect, session
import os, time

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def home():
    html_str = f"""<!DOCTYPE html>
<html>
    <head>
        <META Content-Type="text/html" charset="iso-8859-1">
    </head>
    <body>
        <P style="text-align:right; margin:2px;">User : {session["username"]}
        <a href="/logout">Deconnexion</a></p>
        Hello My World !<BR />
        Phrase avec des accents<BR />
        l'écureuil cogne à la fenêtre !<BR />
    </body>
</html>
    """
    print("home()")
    return html_str

@app.route("/welcome")
def welcome():
    print("welcome()")
    return render_template("welcome.html")

@app.route("/login", methods=["GET","POST"])
def login():
    print("login()", end=" : ")
    error = None    
    if request.method == "POST":
        username = request.form["username"]
        if (username ,request.form["password"]) != ("admin", "admin"):
            error = "Identifiant et/ou mot de passe invalide. Essayer à nouveau !"
            session["tentatives"] = session.get("tentatives", 0)  + 1
            error = "{} ({})".format(error, session["tentatives"])
            time.sleep(session["tentatives"] * 2)
            if session["tentatives"] > 2:
                return redirect(url_for("welcome"))
        else:
            print(f"User : {username}, succesfully connected")
            session["logged_in"] = True
            session["username"] = username
            session["tentatives"] = 0
            return redirect(url_for("home"))
    
    print(f"Error : {error}")
    return render_template("login.html", error=error)

@app.route("/logout", methods=["GET","POST"])
def logout():
    session.pop("logged_in", None)
    print("logout()")
    return redirect(url_for("welcome"))

@app.route("/<name>")
def hello_name(name):
    print(f"hello_name : {name}")
    return "Hello {} !".format(name)


if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    app.run(debug=True)

