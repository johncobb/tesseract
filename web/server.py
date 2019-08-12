from functools import wraps
import json
from six.moves.urllib.request import urlopen

from flask import Flask, request, jsonify, render_template

from os import environ as env
from dotenv import load_dotenv, find_dotenv

from collections import defaultdict

from flask_cors import CORS
from parser_kia_tsv import parser, post_processing
from parser_kia_json import processing
import werkzeug
from werkzeug import secure_filename
import os

import calendar, time

from flask_restful import reqparse

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

path = os.path.join(os.getcwd(), 'tsv')
if not os.path.isdir(path):
    os.mkdir(path)

APP = Flask(__name__)
CORS(APP)

def build_page_list(inpath):
    ignore_files = ["final.tsv", ".gitignore"]
    pagenum_list = []
    filename_list = []
    filename_prefix = ""
    filename_ext = ""
    
    # Gets the page numbers
    for filename in os.listdir(inpath):
        print(type(filename))
        # Sets the filename_prefix variable and file_extension variable
        if isinstance(filename, str):
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


@APP.route('/api/upload', methods=['POST', 'PUT'])
def uploads():
    parse = reqparse.RequestParser()
    parse.add_argument('configid')
    parse.add_argument('id', required=True, type=int, help='I\'m sorry but the attribute "id" is required and must be an int.')
    
    args = parse.parse_args()
    
    configid = args['configid']
    transid = args['id']
    
    if not configid:
        configid = "latest"
    
    if not configid.isdigit():
        if configid.lower() == "latest":
            configid = 1
    
    if not transid > -1:
        return jsonify(message="Please make sure that transid is above -1.")
    
    job_json = {
        'job': {}
    }
    
    if isinstance(configid, str):
        if configid.isdigit():
            configid = int(configid)
    
    if configid == 1:
        job_json['job']['configid'] = configid
        job_json['job']['id'] = transid
        job_json['job']['pages'] = []
    else:
        return jsonify(message='Please enter a valid config id.')
    
    path = os.path.join(os.getcwd(), 'tsv')
    if not os.path.isdir(path):
        os.mkdir(path)
    
    for item in request.files.getlist('file'):
        filename = secure_filename(item.filename)
        file_path = os.path.join(path, filename)
        # item.save(file_path)
        page_json = {
            "page": int(filename.split('-')[-1].split('.')[0]) + 1,
            'rows': processing(item, pat=path, tsv=True)
        }
        # os.remove(file_path)
        job_json['job']['pages'].append(page_json)
    
    return jsonify(job_json)

@APP.route('/')
def index():
    return render_template('index.html')

@APP.route('/upload', methods=['POST'])
def upload():
    global path
    cfg_id = request.form.get('version')
    if cfg_id.isdigit():
        cfg_id = int(cfg_id)
    else:
        return jsonify(message="Please make sure the version is a number.")
    job_json = {
        "job": {
            "config_id": cfg_id,
            "id": calendar.timegm(time.gmtime()),
            'pages': []
        }
    }
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    
    if not uploaded_files[0].filename:
        return jsonify(message='Please select files to upload!')
    
    for item in uploaded_files:
        file_ext = item.filename.split('.')[-1]
        if file_ext.lower() == 'json':
            page_json = {
                'page': int(item.filename.split('-')[-1].split('.')[0]),
                'rows': parser(item, tsv=True)
            }
        elif file_ext.lower() == 'tsv':
            page_json = {
                'page': int(item.filename.split('-')[-1].split('.')[0]),
                'rows': parser(item, tsv=True)
            }
        # os.remove(os.path.join(path, item))
        job_json['job']['pages'].append(page_json)
    
    response = json.dumps(job_json, indent=4)
    # Load an html page with a link to each uploaded file
    return render_template('upload.html', response=response)


if __name__ == "__main__":
    APP.run(host=env.get("IP", "0.0.0.0"), port=env.get("PORT", 3010), debug=True)