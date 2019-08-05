import csv, json, getopt
import os,sys, time
import util
import re

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
    if len(ocr_val) == 11:
        ocr_type = "text"
        return True

def task2(ocr_val):
    global ocr_type
    if len(ocr_val) == 6 and ocr_val.isdigit():
        ocr_type = "text"
        return True

def task3(ocr_val):
    global ocr_type
    regex = r"^"
    if re.match(r"^((((0[13578])|([13578])|(1[02]))[\/](([1-9])|([0-2][0-9])|(3[01])))|(((0[469])|([469])|(11))[\/](([1-9])|([0-2][0-9])|(30)))|((2|02)[\/](([1-9])|([0-2][0-9]))))[\/]\d{4}$|^\d{4}$", ocr_val) \
        or re.match(r"^(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/(?:[0-9]{2})?[0-9]{2}$", ocr_val) \
            or re.match(r'^(?:(?:(?:0?[13578]|1[02])(\/|-|\.)31)\1|(?:(?:0?[1,3-9]|1[0-2])(\/|-|\.)(?:29|30)\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:0?2(\/|-|\.)29\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:(?:0?[1-9])|(?:1[0-2]))(\/|-|\.)(?:0?[1-9]|1\d|2[0-8])\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$', ocr_val):
        ocr_type = 'date'
        return True
    else:
        return False
    
def task4(ocr_val):
    global ocr_type
    # ^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}$
    if re.match(r'^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}', ocr_val):
        ocr_type = 'number'
        return True
    else:
        return False
    
# reference to index of function being called
fnc_index = 0

# fmap stores references to task functions and their results
fmap = {0: [task1, 0],
    1: [task2, 0],
    2: [task3, 0],
    3: [task4, 0],
    4: 0}
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

def post_processing(json_data):
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

    index_header = 0
    index_footer = 1
    index_balance = 2
    index_date = 3

    for page in json_data['job']['pages']:

        for row in page['rows']:
            conf = []
            if len(row['cols']) > 2 and len(row['cols']) < 5:

                vin = row['cols'][index_header]['val'] + row['cols'][index_footer]['val']
                vin_header_bbox = row['cols'][index_header]['bbox']
                vin_footer_bbox = row['cols'][index_footer]['bbox']
                

                valid = util.ValidateVIN(vin)
                balance = row['cols'][index_balance]['val']
                bal_bbox = row['cols'][index_balance]['bbox']

                conf.append(row['cols'][index_header]['conf'])
                conf.append(row['cols'][index_footer]['conf'])
                bal_conf = row['cols'][index_balance]['conf']

                vin_attr = valid[0]
                bal_attr = row['cols'][index_balance]['attr']

                ocr_col = {
                    'type': 'text',
                    'val': vin,
                    'bbox': [vin_header_bbox, vin_footer_bbox],
                    'conf': conf,
                    'attr': vin_attr
                }

                ocr_col2 = {
                    'type': 'number',
                    'val': balance,
                    'bbox': [bal_bbox],
                    'conf': [bal_conf],
                    'attr': bal_attr
                }


                ocr_cols.append(ocr_col)
                ocr_cols.append(ocr_col2)
                if len(row['cols']) == 4:
                    date = row['cols'][index_date]['val']
                    date_bbox = row['cols'][index_date]['bbox']
                    date_conf = row['cols'][index_date]['conf']
                    date_attr = row['cols'][index_date]['attr']
                    
                    ocr_col3 = {
                        'type': 'date',
                        'val': date,
                        'bbox': [date_bbox],
                        'conf': [date_conf],
                        'attr': date_attr
                    }
                    ocr_cols.append(ocr_col3)
                ocr_col = {}
                ocr_col2 = {}

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

def parser(item, tsv=False):
    global inpath, path, fnc_index, job_id, pagenum_list, filename_list
     # parse the page number
    
    ocr_rows = []
    ocr_cols = []
    ocr_val = ""
    # *** the following two functions are broken out for readability ***
    if tsv:
        tsvfile = item
    else:
        # Opens the file currently in the loop
        tsvfile = open(os.path.join(inpath, item))
    # Reads the tsv file and converts it to a dictionary
    
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
        fmap[fnc_index][1] = fmap[fnc_index][0](ocr_val)

        # json template for local storage
        ocr_json = {
            "type": ocr_type,
            "val": ocr_val,
            "bbox": ocr_bbox,
            "conf": ocr_conf,
            "attr": False
        }

        # if function was successful append the ocr json to column
        if fmap[fnc_index][1]:
            ocr_json['attr'] = True
            ocr_cols.append(ocr_json)
            fnc_index += 1

        # print(json.dumps(ocr_cols, indent=2))

        # check to see if all functions have completed
        if (fmap[0][1] and fmap[1][1] and fmap[2][1] and fmap[3][1]):
            # we found all the parts so add columns to row
            rows_json = {
                "cols": ocr_cols
            }

            # append the ocr column data to row
            ocr_rows.append(rows_json)
            fnc_index = 0
            fmap[0][1] = 0
            fmap[1][1] = 0
            fmap[2][1] = 0
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

    # filename_list = ['result-004.tsv', 'result-006.tsv']

    # for each file in the directory
    for item in filename_list:
        pagenum = int(item.split('.')[0].split('-')[-1])
        rows = parser(item)
        pages_json = {
            "page": pagenum + 1,
            "rows": rows
        }
        ocr_pages.append(pages_json)

    job_json = {
        "job": {
            "config_id": cfg_id,
            "id": job_id,
            "pages": ocr_pages
        }
    }
    # print(json.dumps(job_json, indent=2))
    # sys.exit()
    
    job_json = post_processing(job_json)
    print("processing completed successfully")
    return job_json