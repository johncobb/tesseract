import csv, json, getopt
import os,sys, time
from parsers.util import ValidateVIN
import re
import werkzeug
import io

# date regex:
# ^((((0[13578])|([13578])|(1[02]))[\/](([1-9])|([0-2][0-9])|(3[01])))|(((0[469])|([469])|(11))[\/](([1-9])|([0-2][0-9])|(30)))|((2|02)[\/](([1-9])|([0-2][0-9]))))[\/]\d{4}$|^\d{4}$

# Input path
inpath = "out/tsv/"
# Root directory path
path = "/Users/tylermeserve/Documents/Tesseract/tesseract"

ignore_files = ["final.tsv", ".gitignore"]

# Used to sort the page
pagenum_list = []
# used to store names of files
filename_list = []

filename_prefix = "result"
filename_ext = ".tsv"

cfg_id = "12345678"
job_id = 1561780205

# local storage
ocr_type = "text"
ocr_val = ""

def task1(ocr_val):
    global ocr_type
    illegal_chars = ['I', 'O', 'Q']
    for item in ocr_val:
        if item.upper() in illegal_chars:
            return False
    if len(ocr_val) == 11:
        ocr_type = "text"
        return True
    return False

def task2(ocr_val):
    global ocr_type
    if len(ocr_val) == 6 and ocr_val.isdigit():
        ocr_type = "text"
        return True
    return False

def task3(ocr_val):
    global ocr_type
    # ^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}$
    if re.match(r'^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}', ocr_val):
        ocr_type = 'number'
        return True
    return False
    
def task4(ocr_val):
    global ocr_type
    if re.match(r"^((((0[13578])|([13578])|(1[02]))[\/](([1-9])|([0-2][0-9])|(3[01])))|(((0[469])|([469])|(11))[\/](([1-9])|([0-2][0-9])|(30)))|((2|02)[\/](([1-9])|([0-2][0-9]))))[\/]\d{4}$|^\d{4}$", ocr_val):
        ocr_type = 'date'
        return True
    return False

def dummy_task(ocr_val):
    return False

# reference to index of function being called
fnc_index = 0

# fmap stores references to task functions and their results
fmap = {}

def build_sample_output():

    ocr_type = "text"
    ocr_val = "5XXGT4L30GG032037"
    ocr_bbox =[[100,200,100,300], [100,200,100,300]]
    ocr_conf = 90
    ocr_attr = [True]

    ocr_cols = []
    ocr_rows = []
    ocr_pages = []

    ocr_json = {
        "type": ocr_type,
        "val": ocr_val,
        "bbox": ocr_bbox,
        "conf": ocr_conf
    }
    # append the ocr json to column
    ocr_cols.append(ocr_json)

    rows_json = {
        "cols": ocr_cols
    }

    # append the ocr column data to row
    ocr_rows.append(rows_json)

    pages_json = {
        "rows": ocr_rows
    }

    job_json =   {
        "job": {
            "config_id": cfg_id,
            "id": job_id,
            "pages": [
                pages_json
            ]
        }
    }

    print(json.dumps(job_json, indent=2))


def build_page_list():
    global filename_list, inpath
    
    # Gets the page numbers
    for filename in os.listdir(inpath):
        # Sets the filename_prefix variable and file_extension variable
        if not os.path.isfile(os.path.join(inpath, filename)):
            continue
        if filename in ignore_files:
            print("ignore file: ", filename)
            continue

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

def post_processing(json_data, values):
    global job_id, cfg_id
    prev_val = ""
    new_json = {
        "job": {
            "config_id": cfg_id,
            "id": job_id
        }
    }
    ocr_cols = []
    ocr_rows = []
    ocr_pages = []

    if 'vin' in values and 'date' in values and 'balance' in values:

        index_header = 0
        index_footer = 1
        index_date = 2
        index_balance = 3
    elif 'vin' in values and 'date' in values:
        index_header = 0
        index_footer = 1
        index_date = 2
    elif 'vin' in values and 'balance' in values:
        index_header = 0
        index_footer = 1
        index_balance = 2
    elif 'date' in values and 'balance' in values:
        index_date = 0
        index_balance = 1
    elif 'vin' in values:
        index_header = 0
        index_footer = 1
    elif 'date' in values:
        index_date = 0
    elif 'balance' in values:
        index_balance = 0

    for page in json_data['job']['pages']:

        for row in page['rows']:
            conf = []
            # if len(row['cols']) > 2 and len(row['cols']) < 5:
            if len(row['cols']) == 4:
                
                bal_attr = row['cols'][index_balance]['attr']

                
                if 'vin' in values:
                    conf.append(row['cols'][index_header]['conf'])
                    conf.append(row['cols'][index_footer]['conf'])

                    vin = row['cols'][index_header]['val'] + row['cols'][index_footer]['val']
                    vin_header_bbox = row['cols'][index_header]['bbox']
                    vin_footer_bbox = row['cols'][index_footer]['bbox']
                    
                    valid = ValidateVIN(vin)
                    vin_attr = valid[0]

                    ocr_col = {
                        'type': 'text',
                        'val': vin,
                        'bbox': [vin_header_bbox, vin_footer_bbox],
                        'conf': conf,
                        'attr': vin_attr
                    }

                    ocr_cols.append(ocr_col)
                    ocr_col = {}
                
                if 'date' in values:

                    date = row['cols'][index_date]['val']
                    date_bbox = row['cols'][index_date]['bbox']
                    date_conf = row['cols'][index_date]['conf']
                    date_attr = row['cols'][index_date]['attr']
                    ocr_col2 = {
                        'type': 'date',
                        'val': date,
                        'bbox': [date_bbox],
                        'conf': [date_conf],
                        'attr': date_attr
                    }

                    ocr_cols.append(ocr_col2)
                    ocr_col2 = {}

                if 'balance' in values:
                    bal_conf = row['cols'][index_balance]['conf']
                    balance = row['cols'][index_balance]['val']
                    bal_bbox = row['cols'][index_balance]['bbox']

                    ocr_col3 = {
                        'type': 'number',
                        'val': balance,
                        'bbox': [bal_bbox],
                        'conf': [bal_conf],
                        'attr': bal_attr
                    }

                    ocr_cols.append(ocr_col3)

                if not ocr_cols:
                    continue

                row_json = {
                    'cols': ocr_cols
                }
                ocr_rows.append(row_json)
                ocr_cols = []
        page_json = {
            'page': page['page'],
            'rows': ocr_rows
        }
        ocr_pages.append(page_json)
        ocr_rows = []
        

    new_json['job']['pages'] = ocr_pages
    return new_json

def parser(item, values, pat=None, tsv=False):
    global inpath, path, fnc_index, job_id, pagenum_list, filename_list
     # parse the page number
     
    if path:
        inpath = pat
    
    if 'vin' in values:
        fmap[0] = [task1, 0]
        fmap[1] = [task2, 0]
        fmap[2] = [dummy_task, 0]
        fmap[3] = [dummy_task, 0]
        fmap[4] = 0
    if 'balance' in values:
        fmap[2] = [task3, 0]
        fmap[3] = [dummy_task, 0]
    if 'date' in values:
        fmap[3] = [task4, 0]

    ocr_rows = []
    ocr_cols = []
    ocr_val = ""
    # *** the following two functions are broken out for readability ***
    # Opens the file currently in the loop
    if tsv:
        item.seek(0)
        tsvfile = io.StringIO(item.read().decode())
    else:
        tsvfile = open(os.path.join(inpath, item))
    # Reads the tsv file and converts it to a dictionary
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    # loop through each row in the file
    for row in reader:
        # read ocr text value
        ocr_val = row["text"]

        # validate if not move to next
        if not ocr_val:
            continue
        # trim and validate if not move to next
        if not ocr_val.strip():
            continue
        # append coordiantes (bounding box)
        ocr_bbox = [int(row['left']), int(row['top']), int(row['width']), int(row['height'])]
        # set confidence
        ocr_conf = int(row['conf'])

        # call the current function and store the result
        # if isinstance(fmap[fnc_index], int):
        #     fnc_index = 0
        #     continue
        # print(ocr_val, ' is ocr_val')
        # print(fnc_index, ' is fnc_index')
        try:
            fmap[fnc_index][1] = fmap[fnc_index][0](ocr_val)
        except TypeError:
            print(fnc_index)
            print(ocr_val)
        # json template for local storage
        ocr_json = {
            "type": ocr_type,
            "val": ocr_val,
            "bbox": ocr_bbox,
            "conf": ocr_conf,
            "attr": False
        }
        if fnc_index == 2 and not fmap[fnc_index][1]:
            print(ocr_val, ' is ocr_val')
        # if function was successful append the ocr json to column
        if fmap[fnc_index][1]:        
            ocr_json['attr'] = True
            # if ocr_val.find('=') > -1:
            #     print(ocr_val)
            ocr_cols.append(ocr_json)                
            fnc_index += 1
        else:
            if fmap[0][1] and fmap[1][1] and fnc_index == 2 and len(ocr_val) > 5 and len(ocr_val) < 12:
                if ocr_val.find('/') > -1 or ocr_val.find('-') > -1 or ocr_val.count('.') == 2:
                    ocr_json['attr'] = False
                    ocr_json['type'] = 'date'
                    fmap[fnc_index][1] = True
                    ocr_cols.append(ocr_json)
                    fnc_index += 1
            if fmap[2][1] and fnc_index == 3:
                found_ds = ocr_val.find('$')
                found_pe = ocr_val.find('.')
                found_co = ocr_val.find(',')
                
                if found_ds > -1 and (found_co > -1 or found_pe > -1):
                    ocr_json['type'] = 'number'
                    ocr_json['attr'] = False
                    fmap[fnc_index][1] = True
                    ocr_cols.append(ocr_json)
                    fnc_index += 1
                elif found_co > -1 or found_pe > -1:
                    ocr_json['type'] = 'number'
                    ocr_json['attr'] = False
                    fmap[fnc_index][1] = True
                    ocr_cols.append(ocr_json)
                    fnc_index += 1

        # check to see if all functions have completed
        if (fmap[0][1] and fmap[1][1] and fmap[2][1] and fmap[3][1]):
            # we found all the parts so add columns to row
            rows_json = {
                "cols": ocr_cols
            }

            # append the ocr column data to row
            ocr_rows.append(rows_json)
            fnc_index = 0

            if 'vin' in values:
                fmap[0][1] = 0
                fmap[1][1] = 0
            
            if 'date' in values:
                fmap[2][1] = 0
            
            if 'balance' in values:
                fmap[3][1] = 0

            ocr_cols = []

    return ocr_rows

def runner(patharg, inp, tid, configid):
    global inpath, path, fnc_index, job_id, pagenum_list, filename_list, cfg_id
    path = patharg
    inpath = inp
    job_id = tid
    cfg_id = configid
    # Concatenates the paths for easier usage
    inpath = os.path.join(path, inpath)
    
    print("inpath: ", inpath)

    build_page_list()

    # local dictionaries to build up json
    ocr_cols = []
    ocr_rows = []
    ocr_pages = []
    values = ['date', 'balance', 'vin']
    # filename_list = ['result-004.tsv', 'result-006.tsv']

    # for each file in the directory
    for item in filename_list:
        pagenum = int(item.split('.')[0].split('-')[-1])
        rows = parser(item, values)
        pages_json = {
            "page": pagenum + 1,
            "rows": rows
        }
        ocr_pages.append(pages_json)

    job_json =   {
        "job": {
            "config_id": cfg_id,
            "id": job_id,
            "pages": ocr_pages
        }
    }
    
    job_json = post_processing(job_json, values)
    print("processing completed successfully")
    return job_json