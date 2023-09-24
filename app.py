from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

#show changes without restarting flask
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0 

import routes
