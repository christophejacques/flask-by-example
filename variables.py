print("loading Flask : ", flush=True, end="")

import os
from flask import Flask

app = Flask(__name__)
print("ok")

try:
    app.config.from_object(os.environ['APP_SETTINGS'])

except KeyError as ke:
    print(f"ko\nVariable d'environnement {ke} non définie")    
    print()
    print("Pour mettre à jour l'environnement,")
    print("tapper : source .env")
    exit(1)

except Exception as e:
    print("Erreur :", e)
    exit(1)

if False:
    for k in app.config:
        if k in ("ENV", "DEBUG", "TESTING", "SECRET_KEY", "DEVELOPMENT", 
                 "SQLALCHEMY_DATABASE_URI", "SQLALCHEMY_TRACK_MODIFICATIONS"):
            pass
            print(f"- {k:30} =", app.config[k])
