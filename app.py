from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', base="base.html")

@app.route("/Archeology")
def home():
    return render_template('home.html', base="base.html")

@app.route("/Biology")
def home():
    return render_template('home.html', base="base.html")

@app.route("/Geology")
def home():
    return render_template('home.html', base="base.html")

@app.route("/Paleontology")
def home():
    return render_template('home.html', base="base.html")

@app.route("/About_Us")
def home():
    return render_template('home.html', base="base.html")

if __name__ == '__main__':
    app.run(debug=True)
