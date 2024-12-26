from flask import Flask, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from routes import authentication
from utils.token_utils import secret_key


app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = secret_key
app.config["JWT_SECRET_KEY"] = secret_key

app.register_blueprint(authentication)

@jwt.unauthorized_loader
def unauthorized_error(callback):

    return render_template("unauthorized.html")

@app.route('/')
def index():

    return redirect(url_for("authentication.register"))

@app.route('/home', methods=['GET'])
@jwt_required()
def home():

    print("inside home")

    user = get_jwt_identity()

    if user:

        return render_template("home.html") 
    
    else:

        return jsonify({"message": "couldnt identify user"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)