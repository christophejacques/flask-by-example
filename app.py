from flask import Flask
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/')
def hello():
    html_str = """<!DOCTYPE html>
<html>
    <head>
        <META Content-Type="text/html" charset="iso-8859-1">
    </head>
    <body>
        Hello My World !
        Phrase avec des accents
          l'écureuil cogne à la fenêtre !
    </body>
</html>
    """
    return html_str

@app.route('/<name>')
def hello_name(name):
    return "Hello {} !".format(name)


if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    app.run()

