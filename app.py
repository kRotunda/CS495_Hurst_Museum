from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import or_
import flask
import os
import smtplib

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
    admin = db.Column(db.Integer)

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
    news_collection = News.query.order_by(News.id.desc()).limit(4).all()
    return render_template('home.html', base="base.html",news_collection = news_collection)

# ***************************** Search *****************************

@app.route("/search", methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['input']
        artifacts = Artifacts.query.join(User).filter((Artifacts.name.ilike(f'%{search_query}%') |
                                                        Artifacts.description.ilike(f'%{search_query}%') |
                                                        Artifacts.subject.ilike(f'%{search_query}%')) &
                                                        (User.admin == 1))
        colections = Colection.query.filter(or_(Colection.name.ilike(f'%{search_query}%'),
                                                Colection.shortDescription.ilike(f'%{search_query}%'),
                                                Colection.description.ilike(f'%{search_query}%'),
                                                Colection.subject.ilike(f'%{search_query}%')))
        news = News.query.filter(or_(News.name.ilike(f'%{search_query}%'),
                                     News.shortDescription.ilike(f'%{search_query}%'),
                                     News.description.ilike(f'%{search_query}%'),
                                     News.subject.ilike(f'%{search_query}%')))
        
        if len(artifacts) > 15:
            artifacts = artifacts[0:15]
        if len(colections) > 15:
            colections = colections[0:15]
        if len(news) > 15:
            news = news[0:15]
        
        return render_template('search.html', base="base.html", artifacts=artifacts, colections=colections, news=news, search_query=search_query)

    return render_template('search.html', base="base.html")

# ***************************** Student *****************************

@app.route("/StudentGallery", methods = ['GET', 'POST'])
def studentGallery():
    artifactArray = []
    # admin_user = User.query.filter_by(username=current_user.username, admin=0).first()
    # if admin_user:
    allArtifacts = Artifacts.query.join(User).filter(User.admin==0).all()
    # else:
    #     allArtifacts = []
        
    if len(allArtifacts) == 0:
        return render_template('studentGallery.html', base="base.html")
    for i in range(0, len(allArtifacts), 15):
        artifactArray.append(allArtifacts[i:i+15])
    if request.method == 'POST':
        currentPage = request.form['currentPage']
        return render_template('studentGallery.html', base="base.html", allArtifacts = artifactArray[int(currentPage)-1], nextPage = len(artifactArray), currentPage = currentPage)
    return render_template('studentGallery.html', base="base.html", allArtifacts = artifactArray[0], nextPage = len(artifactArray))

# ***************************** Archaeology *****************************

@app.route("/Archaeology")
def archaeology():
    return render_template('overview.html', base="base.html", subject="Archaeology")

@app.route("/Archaeology_Gallery", methods = ['GET', 'POST'])
def archaeologyGallery():
    artifactArray = []
    allArtifacts = Artifacts.query.join(User).filter(Artifacts.subject=="archaeology", User.admin==1).all()
    if len(allArtifacts) == 0:
        return render_template('gallery.html', base="base.html", subject="Archaeology")
    for i in range(0, len(allArtifacts), 15):
        artifactArray.append(allArtifacts[i:i+15])
    if request.method == 'POST':
        currentPage = request.form['currentPage']
        return render_template('gallery.html', base="base.html", subject="Archaeology", allArtifacts = artifactArray[int(currentPage)-1], nextPage = len(artifactArray), currentPage = currentPage)
    return render_template('gallery.html', base="base.html", subject="Archaeology", allArtifacts = artifactArray[0], nextPage = len(artifactArray))

@app.route("/Archaeology_Exhibits", methods = ['GET', 'POST'])
def archaeologyExhibits():
    exhibitsArray = []
    allExhibits = Colection.query.filter_by(subject="archaeology").all()
    if len(allExhibits) == 0:
        return render_template('exhibits.html', base="base.html", subject="Archaeology")
    for i in range(0, len(allExhibits), 15):
        exhibitsArray.append(allExhibits[i:i+15])
    if request.method == 'POST':
        currentPage = request.form['currentPage']
        return render_template('exhibits.html', base="base.html", subject="Archaeology", allExhibits = exhibitsArray[int(currentPage)-1], nextPage = len(exhibitsArray), currentPage = currentPage)
    return render_template('exhibits.html', base="base.html", subject="Archaeology", allExhibits = exhibitsArray[0], nextPage = len(exhibitsArray))

@app.route("/Archaeology_Timeline")
def archaeologyTimeline():
    return render_template('timeline.html', base="base.html", subject="Archaeology")

@app.route("/Archaeology_News", methods = ['GET', 'POST'])
def archaeologyNews():
    newsArray = []
    allNews = News.query.filter_by(subject="archaeology").all()
    if len(allNews) == 0:
        return render_template('news.html', base="base.html", subject="Archaeology")
    for i in range(0, len(allNews), 15):
        newsArray.append(allNews[i:i+15])
    if request.method == 'POST':
        currentPage = request.form['currentPage']
        return render_template('news.html', base="base.html", subject="Archaeology", allNews = newsArray[int(currentPage)-1], nextPage = len(newsArray), currentPage = currentPage)
    return render_template('news.html', base="base.html", subject="Archaeology", allNews = newsArray[0], nextPage = len(newsArray))

@app.route("/archaeologyDisplay/<id>")
def archaeologyDisplayReroute(id):
    return flask.redirect('/ArchaeologyDisplay/'+id)

@app.route("/ArchaeologyDisplay/<id>")
def archaeologyDisplay(id):
    artifact = Artifacts.query.filter_by(id=id).first()
    artifactFiles = Files.query.filter_by(artifactId=id).all()
    return render_template('display.html', base="base.html", subject="Archaeology", artifact = artifact, artifactFiles = artifactFiles, admin=current_user.admin, userId = current_user.id)

@app.route("/archaeologyDisplayExhibit/<id>")
def archaeologyDisplayExhibitReroute(id):
    return flask.redirect('/ArchaeologyDisplayExhibit/'+id)

@app.route("/ArchaeologyDisplayExhibit/<id>")
def archaeologyDisplayExhibit(id):
    exhibit = Colection.query.filter_by(id=id).first()
    artifacts = ColectionArtifacts.query.filter_by(colectionId=id).all()

    artifactList = []
    for artifactId in artifacts:
        artifact = Artifacts.query.filter_by(id=artifactId.artifactId).first()
        artifactList.append(artifact)

    return render_template('display.html', base="base.html", subject="Archaeology", exhibit = exhibit, artifactList = artifactList, admin=current_user.admin, userId = current_user.id)

@app.route("/archaeologyDisplayNews/<id>")
def archaeologyDisplayNewsReroute(id):
    return flask.redirect('/ArchaeologyDisplayNews/'+id)

@app.route("/ArchaeologyDisplayNews/<id>")
def archaeologyDisplayNews(id):
    news = News.query.filter_by(id=id).first()
    newsFiles = NewsFiles.query.filter_by(newsId=id).all()
    return render_template('display.html', base="base.html", subject="Archaeology", news = news, newsFiles = newsFiles, admin=current_user.admin, userId = current_user.id)

@app.route("/updateArchaeology/<id>", methods = ['GET', 'POST'])
@login_required
def updateArchaeology(id):
    artifact = Artifacts.query.filter_by(id=id).first()
    if request.method == 'POST':
        artifact.name = request.form['artifactName']
        artifact.description = request.form['description']
        artifact.timePeriod = request.form['year']
        db.session.commit()
        return flask.redirect('/ArchaeologyDisplay/'+id)
    return render_template('updatePost.html', base="base.html", subject="Archaeology", artifact = artifact)

@app.route("/deleteArchaeology/<id>")
@login_required
def deleteArchaeology(id):
    artifact = Artifacts.query.filter_by(id=id).first()
    collection = ColectionArtifacts.query.filter_by(artifactId=id).all()
    artifactFiles = Files.query.filter_by(artifactId=id).all()

    for artifactCollection in collection:
        db.session.delete(artifactCollection)
    for file in artifactFiles:
        try:
            os.remove('static/artifact_img/' + file.fileName)
            print("File deleted successfully.")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print("Error occurred:", e)
        db.session.delete(file)
    try:
        os.remove('static/artifact_img/' + artifact.coverImageName)
        print("File deleted successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Error occurred:", e)
    db.session.delete(artifact)
    db.session.commit()
    return flask.redirect('/Archaeology_Gallery')

@app.route("/updateExibitArchaeology/<id>", methods = ['GET', 'POST'])
@login_required
def updateExibitArchaeology(id):
    exhibit = Colection.query.filter_by(id=id).first()
    if request.method == 'POST':
        exhibit.name = request.form['name']
        exhibit.shortDescription = request.form['shortDescription']
        exhibit.description = request.form['description']
        db.session.commit()
        return flask.redirect('/ArchaeologyDisplayExhibit/'+id)
    return render_template('updatePost.html', base="base.html", subject="Archaeology", exhibit = exhibit)

@app.route("/deleteExibitArchaeology/<id>")
@login_required
def deleteExibitArchaeology(id):
    colection = Colection.query.filter_by(id=id).first()
    colectionArtifacts = ColectionArtifacts.query.filter_by(colectionId=id).all()

    for artifacts in colectionArtifacts:
        db.session.delete(artifacts)
    try:
        os.remove('static/artifact_img/' + colection.coverImageName)
        print("File deleted successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Error occurred:", e)
    db.session.delete(colection)
    db.session.commit()
    return flask.redirect('/Archaeology_Exhibits')

@app.route("/updateNewsArchaeology/<id>", methods = ['GET', 'POST'])
@login_required
def updateNewsArchaeology(id):
    news = News.query.filter_by(id=id).first()
    if request.method == 'POST':
        news.name = request.form['name']
        news.shortDescription = request.form['shortDescription']
        news.description = request.form['description']
        db.session.commit()
        return flask.redirect('/ArchaeologyDisplayNews/'+id)
    return render_template('updatePost.html', base="base.html", subject="Archaeology", news = news)

@app.route("/deleteNewsArchaeology/<id>")
@login_required
def deleteNewsArchaeology(id):
    news = News.query.filter_by(id=id).first()
    newsFiles = NewsFiles.query.filter_by(newsId=id).all()

    for file in newsFiles:
        try:
            os.remove('static/artifact_img/' + file.fileName)
            print("File deleted successfully.")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print("Error occurred:", e)
        db.session.delete(file)
    try:
        os.remove('static/artifact_img/' + news.coverImageName)
        print("File deleted successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("Error occurred:", e)
    db.session.delete(news)
    db.session.commit()
    return flask.redirect('/Archaeology_News')

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
    return render_template('timeline.html', base="base.html", subject="Archaeology")

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
    return render_template('timeline.html', base="base.html", subject="Archaeology")

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
    return render_template('timeline.html', base="base.html", subject="Archaeology")

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
    return render_template('upload.html', base="base.html", admin = current_user.admin)

@app.route("/Create_Admin", methods = ['GET', 'POST'])
@login_required
def createAdmin():
    if request.method == 'POST':
        admin = request.form.get('adminAccount', 0)
        if admin == 'on':
            admin = 1
        else:
            admin = 0
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        newUser = User(username = username, password = password, firstname = firstname, lastname = lastname, email = email, admin = admin)
        db.session.add(newUser)
        db.session.commit()
        return flask.redirect('/Upload')
    return render_template('upload.html', base="base.html", createAdmin = 1, admin = current_user.admin)

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
        image.save(os.path.join(basedir, app.config["IMAGE_UPLOADS"], filename))

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

        if len(allArtifacts) == 0:
            return render_template('upload.html', base="base.html", createExibit = 1, error=1)
        
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

@app.route('/forgotPassword', methods = ['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        email = user.email
        password = user.password
        username = user.username
        name = user.firstname

        subject = "Forgot Password!"
        text = "Dear " + name + ",\n\n" + "Your Username is: " + username +",\n\n" + "Your Password is: " + password + "\n\nThank you for using CT Hurst Virtual Museum!"
        message = 'Subject: {}\n\n{}'.format(subject, text)

        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()

        server.login("SafeRideGunnison@outlook.com", "Safe81230")
        server.sendmail("SafeRideGunnison@outlook.com", email, message)
        server.quit()
        return flask.redirect('/Admin_Login')
    return render_template('forgot.html', base="base.html")

if __name__ == '__main__':
    app.run(debug=True)
