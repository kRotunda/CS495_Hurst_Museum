from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', base="base.html")

@app.route("/Archeology")
def archeology():
    return render_template('subHome.html', base="base.html", subject="Archeology")

@app.route("/Biology")
def biology():
    return render_template('subHome.html', base="base.html", subject="Biology")

@app.route("/Geology")
def geology():
    return render_template('subHome.html', base="base.html", subject="Geology")

@app.route("/Paleontology")
def paleontology():
    return render_template('subHome.html', base="base.html", subject="Paleontology")

@app.route("/About_Us")
def aboutUs():
    return render_template('home.html', base="base.html")

if __name__ == '__main__':
    app.run(debug=True)
