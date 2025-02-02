import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# status = "remote"
status = "local"

if status == "remote":
    UPLOAD_FOLDER = '/home/wuj/mysite/static/'
elif status == "local":
    UPLOAD_FOLDER = './static/'
else:
    print("Unknown status: " + status)

app = Flask(__name__)

rp_dict = {" ": "_"}

def process_filename(filename):
    for c in rp_dict.keys():
        filename = filename.replace(c, rp_dict[c])

    return filename

@app.route('/')
def home():

    # file list
    files = [ [file, round(os.path.getsize(UPLOAD_FOLDER + file)/1024/1024, 2)] for file in os.listdir(UPLOAD_FOLDER) if os.path.isfile(UPLOAD_FOLDER + file) and len(file.split('.')) == 2 and file.split('.')[0] ]
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
            filename = process_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect('/')

    return render_template('upload.html')

@app.route('/delete/<filename>')
def delete_file(filename):

    name = UPLOAD_FOLDER + filename
    os.remove(name)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

