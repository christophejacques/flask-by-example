from variables import app

try:
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
        