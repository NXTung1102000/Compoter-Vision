import os
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = 'son310'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOW_EXTENSION = set(['png','jpg','jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOW_EXTENSION

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/",methods = ['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No image selected for uploading')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        flash('Image successfully uploaded and display below')
        result = 'france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg'
        return render_template('index.html',filename=filename, result = result)
    else:
        flash('Allowed image type are: png , jpg , jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static',filename = 'uploads/' + filename), code = 301)

@app.route('/display_result/<filename>')
def display_result_image(filename):
    return redirect(url_for('static',filename = 'results/' + filename), code = 301)

if __name__== '__main':
    app.run()