from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import flask

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretCey'
login_manager = LoginManager(app)
login_manager.init_app(app)
db = SQLAlchemy(app)
app.config["IMAGE_UPLOADS"] = "static\\assingment_img"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)

class Archeology(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   description = db.Column(db.String(1000), nullable=False)
   year = db.Column(db.String(250), nullable=True)
   uploadedBy = db.Column(db.Integer, db.ForeignKey(User.id))

class ArcheologyColection(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   type = db.Column(db.String(50), nullable=False)
   name = db.Column(db.String(100), nullable=False)
   timeStart = db.Column(db.Integer, nullable=True)
   timeEnd = db.Column(db.Integer, nullable=True)
   description = db.Column(db.String(1000), nullable=False)

class ArcheologyColectionArtifacts(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   colectionId = db.Column(db.Integer, db.ForeignKey(ArcheologyColection.id))
   artifactId = db.Column(db.Integer, db.ForeignKey(Archeology.id))

class ArcheologyFiles(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   fileName = db.Column(db.String(25), nullable=False)
   fileType = db.Column(db.String(25), nullable=False)
   artifactId = db.Column(db.Integer, db.ForeignKey(Archeology.id))

class Biology(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   description = db.Column(db.String(1000), nullable=False)
   year = db.Column(db.String(250), nullable=True)
   uploadedBy = db.Column(db.Integer, db.ForeignKey(User.id))

class BiologyColection(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   type = db.Column(db.String(50), nullable=False)
   name = db.Column(db.String(100), nullable=False)
   timeStart = db.Column(db.Integer, nullable=True)
   timeEnd = db.Column(db.Integer, nullable=True)
   description = db.Column(db.String(1000), nullable=False)

class BiologyColectionArtifacts(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   colectionId = db.Column(db.Integer, db.ForeignKey(BiologyColection.id))
   artifactId = db.Column(db.Integer, db.ForeignKey(Biology.id))

class BiologyFiles(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   fileName = db.Column(db.String(25), nullable=False)
   fileType = db.Column(db.String(25), nullable=False)
   artifactId = db.Column(db.Integer, db.ForeignKey(Biology.id))

class Geology(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   description = db.Column(db.String(1000), nullable=False)
   year = db.Column(db.String(250), nullable=True)
   uploadedBy = db.Column(db.Integer, db.ForeignKey(User.id))

class GeologyColection(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   type = db.Column(db.String(50), nullable=False)
   name = db.Column(db.String(100), nullable=False)
   timeStart = db.Column(db.Integer, nullable=True)
   timeEnd = db.Column(db.Integer, nullable=True)
   description = db.Column(db.String(1000), nullable=False)

class GeologyColectionArtifacts(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   colectionId = db.Column(db.Integer, db.ForeignKey(GeologyColection.id))
   artifactId = db.Column(db.Integer, db.ForeignKey(Geology.id))

class GeologyFiles(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   fileName = db.Column(db.String(25), nullable=False)
   fileType = db.Column(db.String(25), nullable=False)
   artifactId = db.Column(db.Integer, db.ForeignKey(Geology.id))

class Paleontology(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   description = db.Column(db.String(1000), nullable=False)
   year = db.Column(db.String(250), nullable=True)
   uploadedBy = db.Column(db.Integer, db.ForeignKey(User.id))

class PaleontologyColection(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   type = db.Column(db.String(50), nullable=False)
   name = db.Column(db.String(100), nullable=False)
   timeStart = db.Column(db.Integer, nullable=True)
   timeEnd = db.Column(db.Integer, nullable=True)
   description = db.Column(db.String(1000), nullable=False)

class PaleontologyColectionArtifacts(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   colectionId = db.Column(db.Integer, db.ForeignKey(PaleontologyColection.id))
   artifactId = db.Column(db.Integer, db.ForeignKey(Paleontology.id))

class PaleontologyFiles(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   fileName = db.Column(db.String(25), nullable=False)
   fileType = db.Column(db.String(25), nullable=False)
   artifactId = db.Column(db.Integer, db.ForeignKey(Paleontology.id))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

# ***************************** Home *****************************

@app.route("/")
def home():
    if (User.query.filter_by(username="admin") == None):
        admin = User(username = "admin", password = "123")
        db.session.add(admin)
        db.session.commit()
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
def history():
<<<<<<< HEAD
    return render_template('3dmodel.html', base="base.html")
=======
    return render_template('history.html', base="base.html")
>>>>>>> d4d3cc6a565fe8f4dd1f0600eeee973bfc30808d

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
        newUser = User(username = username, password = password, firstname = firstname, lastname = lastname)
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

        if subject == "archeology":
            newArtifact = Archeology(name = artifactName, description = description, year = year, uploadedBy = current_user.id)
        if subject == "biology":
            newArtifact = Biology(name = artifactName, description = description, year = year, uploadedBy = current_user.id)
        if subject == "geology":
            newArtifact = Geology(name = artifactName, description = description, year = year, uploadedBy = current_user.id)
        if subject == "paleontology":
            newArtifact = Paleontology(name = artifactName, description = description, year = year, uploadedBy = current_user.id)


        # for x in range(0,10):   
        #     image = request.files['file'+str(x)]
        #     if image:
        #         filename = secure_filename(image.filename)
        #         print(filename)
        
        
        # newImg = Image(ImageName = '-1', AssignmentId = newAssinmnet.id)
        
        # db.session.add(newImg)
        # db.session.commit()

        # db.session.add(newArtifact)
        # db.session.commit()


        return render_template('upload.html', base="base.html")
    return render_template('upload.html', base="base.html", createArtifact = 1)

@app.route("/Create_Exibit", methods = ['GET', 'POST'])
@login_required
def createExibit():
    if request.method == 'POST':
        subject = request.form['subject']
        name = request.form['exibitName']
        description = request.form['description']
        
        
        if subject == "archeology":
            newExibit = ArcheologyColection(type = "Exibit", name = name, description = description)
        if subject == "biology":
            newExibit = BiologyColection(type = "Exibit", name = name, description = description)
        if subject == "geology":
            newExibit = GeologyColection(type = "Exibit", name = name, description = description)
        if subject == "paleontology":
            newExibit = PaleontologyColection(type = "Exibit", name = name, description = description)

        
        # db.session.add(newExibit)
        # db.session.commit()
        return render_template('upload.html', base="base.html")
    return render_template('upload.html', base="base.html", createExibit = 1)

@app.route("/Create_Timeline", methods = ['GET', 'POST'])
@login_required
def createTimeline():
    if request.method == 'POST':
        subject = request.form['subject']
        name = request.form['exibitName']
        description = request.form['description']
        startYear = request.form['timeStart']
        endYear = request.form['timeEnd']
        
        
        if subject == "archeology":
            newTimeline = ArcheologyColection(type = "Timeline", name = name, timeStart = startYear, timeEnd = endYear, description = description)
        if subject == "biology":
            newTimeline = BiologyColection(type = "Timeline", name = name, timeStart = startYear, timeEnd = endYear, description = description)
        if subject == "geology":
            newTimeline = GeologyColection(type = "Timeline", name = name, timeStart = startYear, timeEnd = endYear, description = description)
        if subject == "paleontology":
            newTimeline = PaleontologyColection(type = "Timeline", name = name, timeStart = startYear, timeEnd = endYear, description = description)

        
        # db.session.add(newTimeline)
        # db.session.commit()
        return render_template('upload.html', base="base.html")
    return render_template('upload.html', base="base.html", createTimeline = 1)

@app.route('/Logout')
@login_required
def logout():
    logout_user()
    return flask.redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
