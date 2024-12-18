from flask import Flask, render_template, redirect, url_for
from flask_jwt_extended import JWTManager
from routes import authentication

app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = "temporarysecretkey"
app.register_blueprint(authentication)

@app.route('/')
def index():

    return redirect(url_for("authentication.register"))

@app.route('/home', methods=['GET'])
def home():

    return render_template("home.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)