from flask import render_template, redirect, url_for, session
from flask_login import login_required
from config import create_app

app = create_app()

@app.route("/", methods=["GET"])
def index():

    return redirect(url_for("authentication.login"))


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():

    return render_template("dashboard.html", role=session["user_role"])

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
