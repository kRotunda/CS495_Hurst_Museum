from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ***************************** Home *****************************

@app.route("/")
def home():
    return render_template('home.html', base="base.html")

# ***************************** Archeology *****************************

@app.route("/Archeology")
def archeology():
    return render_template('overview.html', base="base.html", subject="Archeology")

@app.route("/Archeology_Gallery")
def archeologyGallery():
    return render_template('gallery.html', base="base.html", subject="Archeology")

@app.route("/Archeology_Exhibits")
def archeologyExhibits():
    return render_template('exhibits.html', base="base.html", subject="Archeology")

@app.route("/Archeology_Timeline")
def archeologyTimeline():
    return render_template('timeline.html', base="base.html", subject="Archeology")

# ***************************** Biology *****************************

@app.route("/Biology")
def biology():
    return render_template('overview.html', base="base.html", subject="Biology")

@app.route("/Biology_Gallery")
def biologyGallery():
    return render_template('gallery.html', base="base.html", subject="Biology")

@app.route("/Biology_Exhibits")
def biologyExhibits():
    return render_template('exhibits.html', base="base.html", subject="Biology")

@app.route("/Biology_Timeline")
def biologyTimeline():
    return render_template('timeline.html', base="base.html", subject="Biology")

# ***************************** Geology *****************************

@app.route("/Geology")
def geology():
    return render_template('overview.html', base="base.html", subject="Geology")

@app.route("/Geology_Gallery")
def geologyGallery():
    return render_template('gallery.html', base="base.html", subject="Geology")

@app.route("/Geology_Exhibits")
def geologyExhibits():
    return render_template('exhibits.html', base="base.html", subject="Geology")

@app.route("/Geology_Timeline")
def geologyTimeline():
    return render_template('timeline.html', base="base.html", subject="Geology")

# ***************************** Paleontology *****************************

@app.route("/Paleontology")
def paleontology():
    return render_template('overview.html', base="base.html", subject="Paleontology")

@app.route("/Paleontology_Gallery")
def paleontologyGallery():
    return render_template('gallery.html', base="base.html", subject="Paleontology")

@app.route("/Paleontology_Exhibits")
def paleontologyExhibits():
    return render_template('exhibits.html', base="base.html", subject="Paleontology")

@app.route("/Paleontology_Timeline")
def paleontologyTimeline():
    return render_template('timeline.html', base="base.html", subject="Paleontology")

# ***************************** About Us *****************************

@app.route("/Contact_Us")
def contactUs():
    return render_template('contact.html', base="base.html")

@app.route("/History_Of_Museum")
def historyOfMuseum():
    return render_template('history.html', base="base.html")

@app.route("/Admin_Login")
def adminLogin():
    return render_template('login.html', base="base.html")

if __name__ == '__main__':
    app.run(debug=True)
