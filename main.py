from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config["SECRET_KEY"] = "t432gwerg324qgwg24"
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
