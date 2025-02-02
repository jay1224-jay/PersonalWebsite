import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/'

app = Flask(__name__)

app = Flask(__name__)

@app.route('/')
def home():

    # file list
    files = [ file for file in os.listdir(UPLOAD_FOLDER) ]
    print(files)
    
    return render_template('home.html', files = files, uploadDir = UPLOAD_FOLDER)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect('/')

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

