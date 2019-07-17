import os, requests, json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

from os import environ as env
from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Initialize the Flask application
app = Flask(__name__)

path = os.path.join(os.getcwd(), 'tsv')
if not os.path.isdir(path):
    os.mkdir(path)
    
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'tsv/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')

def build_page_list(inpath):
    filename_list = []
    pagenum_list = []
    filename_prefix = ""
    filename_ext = ""
    ignore_files = ["final.tsv", ".gitignore"]
    # Gets the page numbers
    for filename in os.listdir(inpath):
        # Sets the filename_prefix variable and file_extension variable
        if not os.path.isfile(os.path.join(inpath, filename)):
            continue
        if filename in ignore_files:
            print("ignore file: ", filename)
            continue
        
        if not filename_prefix:
            filename_prefix = filename.split('-')[0]
        if not filename_ext:
            filename_ext = "." + filename.split('.')[-1]
        
        # Gets the page number from the file name
        page_num = filename.split('-')[-1].split('.')[0]       
        # Makes sure page_num isn't empty
        if not page_num:
            continue

        if page_num.isdigit():
            # Adds page number to the list
            pagenum_list.append(page_num)

    # Sorts the page number list
    pagenum_list.sort()
    # after sorting the pages build the list of files
    for pagenum in pagenum_list:
        filename_list.append(filename_prefix + "-" + pagenum + filename_ext)
        
    return filename_list

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    global path
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    
    for file in uploaded_files:
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to the upload
        # folder we setup
        file.save(os.path.join(path, filename))
        # Save the filename into a list, we'll use it later
        filenames.append(filename)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        
    filenames = build_page_list(path)
    request_list = []
    for item in filenames:
        request_list.append(('file', open(os.path.join(path, item), 'rb')))
    
    r = requests.post('http://0.0.0.0:3010/api/upload', files=request_list)
    
    response = json.dumps(r.json(), sort_keys=False, indent=4)
    
    # Load an html page with a link to each uploaded file
    return render_template('upload.html', filenames=filenames, response=response)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(
        host=env.get("IP", "0.0.0.0"),
        port=env.get("PORT", 5000),
        debug=True
    )