from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import flask
import os

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretCey'
login_manager = LoginManager(app)
login_manager.init_app(app)
db = SQLAlchemy(app)
app.config["IMAGE_UPLOADS"] = "static\\artifact_img"
app.config["NEWS_UPLOADS"] = "static\\news_img"
app.config["EXIBIT_UPLOADS"] = "static\\exibit_img"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Artifacts(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   description = db.Column(db.String(1000), nullable=False)
   timePeriod = db.Column(db.String(250), nullable=True)
   subject = db.Column(db.String(50), nullable=False)
   coverImageName = db.Column(db.String(25), nullable=False)
   coverImageType = db.Column(db.String(25), nullable=False)
   uploadedBy = db.Column(db.Integer, db.ForeignKey(User.id))

class Colection(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   type = db.Column(db.String(50), nullable=False)
   name = db.Column(db.String(100), nullable=False)
   shortDescription = db.Column(db.String(150), nullable=False)
   description = db.Column(db.String(1000), nullable=False)
   subject = db.Column(db.String(50), nullable=False)
   coverImageName = db.Column(db.String(25), nullable=False)
   coverImageType = db.Column(db.String(25), nullable=False)

class News(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   shortDescription = db.Column(db.String(150), nullable=False)
   description = db.Column(db.String(1000), nullable=False)
   subject = db.Column(db.String(50), nullable=False)
   coverImageName = db.Column(db.String(25), nullable=False)
   coverImageType = db.Column(db.String(25), nullable=False)

class NewsFiles(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   fileName = db.Column(db.String(25), nullable=False)
   fileType = db.Column(db.String(25), nullable=False)
   newsId = db.Column(db.Integer, db.ForeignKey(News.id))

class ColectionArtifacts(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   colectionId = db.Column(db.Integer, db.ForeignKey(Colection.id))
   artifactId = db.Column(db.Integer, db.ForeignKey(Artifacts.id))

class Files(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   fileName = db.Column(db.String(25), nullable=False)
   fileType = db.Column(db.String(25), nullable=False)
   artifactId = db.Column(db.Integer, db.ForeignKey(Artifacts.id))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

# ***************************** Home *****************************

@app.route("/")
def home():
    news_collection = News.query.all()
    
    return render_template('home.html', base="base.html",news_collection = news_collection)

# ***************************** Archeology *****************************

@app.route("/Archeology")
def archeology():
    return render_template('overview.html', base="base.html", subject="Archeology")

@app.route("/Archeology_Gallery", methods = ['GET', 'POST'])
def archeologyGallery():
    artifactArray = []
    allArtifacts = Artifacts.query.filter_by(subject="archeology").all()
    for i in range(0, len(allArtifacts), 15):
        artifactArray.append(allArtifacts[i:i+15])
    if request.method == 'POST':
        currentPage = request.form['currentPage']
        return render_template('gallery.html', base="base.html", subject="Archeology", allArtifacts = artifactArray[int(currentPage)-1], nextPage = len(artifactArray), currentPage = currentPage)
    return render_template('gallery.html', base="base.html", subject="Archeology", allArtifacts = artifactArray[0], nextPage = len(artifactArray))

@app.route("/Archeology_Exhibits", methods = ['GET', 'POST'])
def archeologyExhibits():
    exhibitsArray = []
    allExhibits = Colection.query.filter_by(subject="archeology").all()
    for i in range(0, len(allExhibits), 15):
        exhibitsArray.append(allExhibits[i:i+15])
    if request.method == 'POST':
        currentPage = request.form['currentPage']
        return render_template('exhibits.html', base="base.html", subject="Archeology", allExhibits = exhibitsArray[int(currentPage)-1], nextPage = len(exhibitsArray), currentPage = currentPage)
    return render_template('exhibits.html', base="base.html", subject="Archeology", allExhibits = exhibitsArray, nextPage = len(exhibitsArray))

@app.route("/Archeology_Timeline")
def archeologyTimeline():
    return render_template('timeline.html', base="base.html", subject="Archeology")

@app.route("/Archeology_News", methods = ['GET', 'POST'])
def archeologyNews():
    newsArray = []
    allNews = News.query.filter_by(subject="archeology").all()
    for i in range(0, len(allNews), 15):
        newsArray.append(allNews[i:i+15])
    if request.method == 'POST':
        currentPage = request.form['currentPage']
        return render_template('news.html', base="base.html", subject="Archeology", allNews = newsArray[int(currentPage)-1], nextPage = len(newsArray), currentPage = currentPage)
    return render_template('news.html', base="base.html", subject="Archeology", allNews = newsArray, nextPage = len(newsArray))

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

@app.route("/Biology_News")
def biologyNews():
    return render_template('timeline.html', base="base.html", subject="Archeology")

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

@app.route("/Geology_News")
def geologyNews():
    return render_template('timeline.html', base="base.html", subject="Archeology")

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

@app.route("/Paleontology_News")
def paleontologyNews():
    return render_template('timeline.html', base="base.html", subject="Archeology")

# ***************************** About Us *****************************

@app.route("/Contact_Us")
def contactUs():
    return render_template('contact.html', base="base.html")

@app.route("/History_Of_Museum")
def history():
    return render_template('history.html', base="base.html")

@app.route("/Admin_Login", methods = ['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user != None:
            if request.form['password'] != user.password:
                return render_template('login.html', base="base.html", error=1)
            else:
                login_user(user)
                return flask.redirect('/')
        return render_template('login.html', base="base.html", error=1)
    return render_template('login.html', base="base.html")

# ***************************** Admin Options *****************************

@app.route("/Upload")
@login_required
def upload():
    return render_template('upload.html', base="base.html")

@app.route("/Create_Admin", methods = ['GET', 'POST'])
@login_required
def createAdmin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        newUser = User(username = username, password = password, firstname = firstname, lastname = lastname, email = email)
        db.session.add(newUser)
        db.session.commit()
        return render_template('upload.html', base="base.html")
    return render_template('upload.html', base="base.html", createAdmin = 1)

@app.route("/Create_Artifact", methods = ['GET', 'POST'])
@login_required
def createArtifact():
    if request.method == 'POST':
        subject = request.form['subject']
        artifactName = request.form['artifactName']
        description = request.form['description']
        year = request.form['year']

        image = request.files['coverImg']
        filename = secure_filename(image.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir, app.config["EXIBIT_UPLOADS"], filename))

        if year == "":
            newArtifact = Artifacts(name = artifactName, description = description, subject = subject, coverImageName = filename, coverImageType = filename.split('.')[-1], uploadedBy = current_user.id)
        else:
            newArtifact = Artifacts(name = artifactName, description = description, timePeriod = year, subject = subject, coverImageName = filename, coverImageType = filename.split('.')[-1], uploadedBy = current_user.id)

        db.session.add(newArtifact)
        db.session.commit()

        numFiles = request.form['numOfFiles']

        for x in range(0,int(numFiles)):   
            image = request.files['file'+str(x)]

            filename = secure_filename(image.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            image.save(os.path.join(basedir, app.config["IMAGE_UPLOADS"], filename))

            newImg = Files(fileName = filename, fileType = filename.split('.')[-1], artifactId = newArtifact.id)
            db.session.add(newImg)
            db.session.commit()
    

        return render_template('upload.html', base="base.html")
    return render_template('upload.html', base="base.html", createArtifact = 1)

@app.route("/Create_Exibit", methods = ['GET', 'POST'])
@login_required
def createExibit():
    if request.method == 'POST':
        subject = request.form['subject']
        name = request.form['exibitName']
        shortDescription = request.form['shortDescription']
        description = request.form['description']

        image = request.files['coverImg']
        filename = secure_filename(image.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir, app.config["EXIBIT_UPLOADS"], filename))

        newExibit = Colection(type = "Exibit", name = name, shortDescription = shortDescription, description = description, subject = subject, coverImageName = filename, coverImageType = filename.split('.')[-1])
        allArtifacts = Artifacts.query.filter_by(subject=subject).all()

        if allArtifacts == None:
            return render_template('upload.html', base="base.html", createExibit = 1, error="no artifacts")
        
        db.session.add(newExibit)
        db.session.commit()

        return render_template('upload.html', base="base.html", createExibit = 1, artifacts=allArtifacts, exibitId = newExibit.id)
    return render_template('upload.html', base="base.html", createExibit = 1)

@app.route("/Exibit_Add", methods = ['GET', 'POST'])
@login_required
def exibitAdd():
    artifacts = []
    artifacts = request.form.getlist('artifactSelect')
    exibitId = request.form['exibitId']

    for i in range(0, len(artifacts)):
        addExibit = ColectionArtifacts(colectionId = exibitId, artifactId = artifacts[i])
        db.session.add(addExibit)
        db.session.commit()

    return render_template('upload.html', base="base.html")

@app.route("/Create_News", methods = ['GET', 'POST'])
@login_required
def createNews():
    if request.method == 'POST':
        subject = request.form['subject']
        name = request.form['newsName']
        shortDescription = request.form['shortDescription']
        description = request.form['description']

        image = request.files['coverImg']
        filename = secure_filename(image.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir, app.config["NEWS_UPLOADS"], filename))

        newNews = News(name = name, shortDescription = shortDescription, description = description, subject = subject, coverImageName = filename, coverImageType = filename.split('.')[-1])

        db.session.add(newNews)
        db.session.commit()

        numFiles = request.form['numOfFiles']

        if int(numFiles) > 0:
            for x in range(0,int(numFiles)):   
                image = request.files['file'+str(x)]

                filename = secure_filename(image.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                image.save(os.path.join(basedir, app.config["NEWS_UPLOADS"], filename))

                newNewsFile = NewsFiles(fileName = filename, fileType = filename.split('.')[-1], newsId = newNews.id)
                db.session.add(newNewsFile)
                db.session.commit()

        return render_template('upload.html', base="base.html")
    return render_template('upload.html', base="base.html", createNews = 1)

# @app.route("/Create_Timeline", methods = ['GET', 'POST'])
# @login_required
# def createTimeline():
#     if request.method == 'POST':
#         subject = request.form['subject']
#         name = request.form['exibitName']
#         description = request.form['description']
#         startYear = request.form['timeStart']
#         endYear = request.form['timeEnd']
        
#         image = request.files['coverImg']
#         filename = secure_filename(image.filename)
        
#         newExibit = Colection(type = "Timeline", name = name, timeStart = startYear, timeEnd = endYear, description = description, subject = subject, coverImageName = filename, coverImageType = type(image))
#         allArtifacts = Artifacts.query.filter_by(subject=subject).all()
        
#         if allArtifacts == None:
#             return render_template('upload.html', base="base.html", createTimeline = 1, error="no artifacts")

#         # db.session.add(newTimeline)
#         # db.session.commit()

#         return render_template('upload.html', base="base.html", createTimeline = 1, artifacts=allArtifacts)
#     return render_template('upload.html', base="base.html", createTimeline = 1)

@app.route('/Logout')
@login_required
def logout():
    logout_user()
    return flask.redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
