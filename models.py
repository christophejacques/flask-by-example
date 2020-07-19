# Chargement de Flask
print("loading Flask : ", flush=True, end="")

import os
from flask import Flask

app = Flask(__name__)
print("ok")

try:
    # Chargement de la configuration
    print(f"Loading config", flush=True, end=" : ")
    app.config.from_object(os.environ['APP_SETTINGS'])
    print("ok")
    
except KeyError as ke:
    print(f"ko\nVariable d'environnement {ke} non définie")    
    print()
    print("Pour mettre à jour l'environnement,")
    print("tapper : source .env")
    exit(1)

except Exception as e:
    print("ko\nErreur :", e)
    exit(1)

if False:
    for k in app.config:
        if k in ("ENV", "DEBUG", "TESTING", "SECRET_KEY", "DEVELOPMENT", 
                 "SQLALCHEMY_DATABASE_URI", "SQLALCHEMY_TRACK_MODIFICATIONS"):
            pass
            print(f"- {k:30} =", app.config[k])

try:
    # Chargement de SQLAlchemy
    print("loading SQLAlchemy : ", flush=True, end="")
    # Test la présence de la variable d'environnement
    assert app.config["SQLALCHEMY_DATABASE_URI"] != ""
    
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    
except KeyError as ke:
    print("ko")
    print(f"Variable d'environnement {ke} non définie")    
    exit(1)
    
except Exception as e:
    print("ko")
    print("Erreur : d'initialisation de la base de données ! ")
    print(e)
    print("Veuillez vérifier que l'environnement virtuel est bien paramétré !")
    exit(1)


class BlogUser(db.Model):
    
    __tablename__ = "users"

    id       = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String,  nullable    = False)
    key      = db.Column(db.String,  nullable    = False)
    password = db.Column(db.String,  nullable    = False)

    def __init__(self, username, cle, password):
        self.username = username
        self.key      = cle
        self.password = password
        
    def __repr__(self):
        return f"Id : {self.id:2}\nUsername : {self.username}" \
               f"\nCle : {self.key}" \
               f"\nPassword : {self.password}" 


class BlogPost(db.Model):
    
    __tablename__ = "posts"
    
    id          = db.Column(db.Integer, primary_key = True)
    title       = db.Column(db.String , nullable    = False)
    description = db.Column(db.String , nullable    = False)
    
    def __init__(self, title, description):
        self.title = title
        self.description = description
        
    def __repr__(self):
        return f"Title : {self.title}\nDescription : {self.description}"


print("ok")
        