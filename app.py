import os
from flask import Flask
from dotenv import load_dotenv
from controllers.home import home_controller
from controllers.production import production_controller

load_dotenv()

app = Flask(__name__)
app.register_blueprint(home_controller)
app.register_blueprint(production_controller)

if __name__ == "__main__":
    debug = os.environ.get("DEBUG", "False") == "True"
    port = os.environ.get("PORT", 5000)
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(debug=debug, port=port, host=host)
