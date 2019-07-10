import csv, json, getopt
import os,sys, time
import util

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
    if len(ocr_val) == 6:
        ocr_type = "text"
        return True

def task2(ocr_val):
    if len(ocr_val) == 11:
        ocr_type = "text"
        return True

def task3(ocr_val):
    if ocr_val.find(',') > -1 or ocr_val.find('.') > -1:
        # Makes sure that text is infact a digit
        if ocr_val.replace(',', "").replace('.', '').isdigit():
            # Used for value checking later on
            ocr_val = float(ocr_val.replace(',', ''))
            ocr_type = "number"
            return True


# reference to index of function being called
fnc_index = 0

# fmap stores references to task functions and their results
fmap = {0: [task1, 0],
    1: [task2, 0],
    2: [task3, 0],
    3:0}


def build_sample_output():

    ocr_type = "text"
    ocr_val = "5XXGT4L30GG032037"
    ocr_xy =[[100,200,100,300], [100,200,100,300]]
    ocr_conf = 90
    ocr_attr = [True]

    ocr_cols = []
    ocr_rows = []
    ocr_pages = []

    ocr_json = {
        "type": ocr_type,
        "val": ocr_val,
        "xy": ocr_xy,
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
    # Gets the page numbers
    for filename in os.listdir(inpath):
        # Sets the filename_prefix variable and file_extension variable

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



def runner(patharg, inp, tid):
    global inpath, path, fnc_index, job_id, pagenum_list
    path = patharg
    inpath = inp
    job_id = tid

    # Concatenates the paths for easier usage
    inpath = os.path.join(path, inpath)

    print("inpath: ", inpath)

    build_page_list()

    # local dictionaries to build up json
    ocr_cols = []
    ocr_rows = []
    ocr_pages = []

    # redeclare filename_list to limit to just two files
    # TODO: remove before flight)
    filename_list = [f for f in os.listdir(inpath) if os.path.isfile(os.path.join(inpath, f))]
    # for each file in the directory
    for item in filename_list:
        if item in ignore_files:
            continue
        # parse the page number
        pagenum = int(item.split('.')[0].split('-')[-1])

        # *** the following two functions are broken out for readability ***
        # Opens the file currently in the loop
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

            # local coordinate storage for bbox
            ocr_xy = []

            # append coordiantes (bounding box)
            ocr_xy.append([int(row['left']), int(row['width']), int(row['top']), int(row['height'])])
            # set confidence
            ocr_conf = int(row['conf'])



            # call the current function and store the result
            fmap[fnc_index][1] = fmap[fnc_index][0](ocr_val)

            # json template for local storage
            ocr_json = {
                "type": ocr_type,
                "val": ocr_val,
                "xy": ocr_xy,
                "conf": ocr_conf
            }


            # if function was successful append the ocr json to column
            if fmap[fnc_index][1]:
                ocr_cols.append(ocr_json)
                fnc_index += 1

            # print(json.dumps(ocr_cols, indent=2))

            # check to see if all functions have completed
            if (fmap[0][1] and fmap[1][1] and fmap[2][1]):
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
                ocr_cols = []
        
        pages_json = {
            "rows": ocr_rows
        }
        ocr_pages.append(pages_json)

        # print(json.dumps(ocr_cols, indent=2))
    
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
    # sys.exit()

    print("processing completed successfully")
    return job_json