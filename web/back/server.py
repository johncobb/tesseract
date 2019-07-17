from functools import wraps
import json
from six.moves.urllib.request import urlopen

from flask import Flask, request, jsonify

from os import environ as env
from dotenv import load_dotenv, find_dotenv

from collections import defaultdict

from flask_cors import CORS
from parser_kia_tsv import parser, post_processing
import werkzeug
from werkzeug import secure_filename
import os

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

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


@APP.route('/api/upload', methods=['POST', 'PUT'])
def upload():
    job_json = {
        "job": {
            "config_id": "12345678",
            "id": 1561780205,
            'pages': []
        }
    }
    path = os.path.join(os.getcwd(), 'tsv')
    if not os.path.isdir(path):
        os.mkdir(path)
    
    for item in request.files.getlist('file'):
        filename = secure_filename(item.filename)
        file_path = os.path.join(path, filename)
        item.save(file_path)
        page_json = {
            "page": int(filename.split('-')[-1].split('.')[0]) + 1,
            'rows': parser(filename, path)
        }
        
        job_json['job']['pages'].append(page_json)
    
    return jsonify(job_json)

if __name__ == "__main__":
    APP.run(host=env.get("IP", "0.0.0.0"), port=env.get("PORT", 3010))