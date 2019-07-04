import csv, json, getopt
import os,sys, time
import util

# Input path
inpath = "out/tsv/"
# Output path
outpath = "out/json/"
# Root directory path
path = "/Users/johncobb/dev/tesseract"

ignore_files = ["final.tsv", ".gitignore"]

# Used to sort the page
pagenum_list = []
# used to store names of files
filename_list = []

filename_prefix = "result"
filename_ext = ".tsv"

cfg_id = "12345678"
job_id = 1561780205

pages_json = {}

def build_sample_output():

    ocr_type = "vin"
    ocr_val = "5XXGT4L30GG032037"
    ocr_xy =[[100,200,100,300], [100,200,100,300]]
    ocr_conf = []
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

        # if not filename_prefix:
        #     file_extension = "." + filename.split('.')[-1]
        #     filename_prefix = filename.split('-')[0]



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


# python3 modules/parsers/parser_kia_tsv.py --inpath out/tsv --outpath out/json/ --path /Users/johncobb/dev/tesseract

# Parses the command line arguments
# def argParse(opts, args):
#     global inpath, outpath, path
#     for opt, arg in opts:
#         optc = opt.lower()
#         if optc in ['--inpath', '-i']:
#             inpath = arg
#         elif optc in ['--outpath', '-o']:
#             outpath = arg
#         elif optc in ['--path', '-p']:
#             path = arg

if __name__ == "__main__":

    # build_sample_output()
    # sys.exit()
    # if not sys.argv[1:]:
    #     print("Error: please provide arugments.")
    #     sys.exit()
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], 'i:o:p', ['--inpath', "--outpath", "--path"])
    # except getopt.GetoptError:
    #     print("Error: invalid argument.")
    #     sys.exit(2)
    
    # if not opts and not args:
    #     print("Error, no parameters provided")
    #     sys.exit()
    
    # # Multi-OS Support
    # slash = ""
    # if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
    #     slash = "/"
    # elif sys.platform == "win32":
    #     slash = "\\"
    
    limit_pages = 5

    # buffer to store combined ocr data
    ocr_buffer = ""

    # Concatenates the paths for easier usage
    inpath = os.path.join(path, inpath)
    outpath = os.path.join(path, outpath)

    print("inpath: ", inpath)
    print("outpath: ", outpath)
    

    build_page_list()

    ocr_cols = []
    ocr_rows = []
    ocr_pages = []

    vin_head_found = False
    vin_tail_found = False
    balance_found = False

    # redeclare filename_list to limit to just two files
    # TODO: remove before flight
    filename_list = ['result-005.tsv', 'result-006.tsv']

    # for each file in the directory
    for item in filename_list:
        # print("item: ", item)


        # parse the page number
        pagenum = int(item.split('.')[0].split('-')[-1])

        # if pagenum == limit_pages:
        #     print("page_limit: ", pagenum)
        #     print("exiting system.")
        #     break

        # Opens the file currently in the loop
        tsvfile = open(os.path.join(inpath, item))
        # Reads the tsv file and converts it to a dictionary
        reader = csv.DictReader(tsvfile, dialect='excel-tab')

        ocr_valid_field = False
        for row in reader:
            
            # local storage
            ocr_type = "text"
            ocr_val = ""
            ocr_xy = []
            ocr_conf = ""

            # store the ocr'd text value
            ocr_val = row["text"]

            # validate if not move to next
            if not ocr_val:
                continue
            # trim and validate if not move to next
            if not ocr_val.strip():
                continue


            # append coordiantes (bounding box)
            ocr_xy.append([int(row['left']), int(row['width']), int(row['top']), int(row['height'])])
            # set confidence
            ocr_conf = int(row['conf'])

            if len(ocr_val) == 6:
                ocr_type = "text"
                ocr_valid_field = True
                vin_tail_found = True
            elif len(ocr_val) == 11:
                ocr_type = "text"
                ocr_valid_field = True
                vin_head_found = True
            elif ocr_val.find(',') > -1 or ocr_val.find('.') > -1:
                # Makes sure that text is infact a digit
                if ocr_val.replace(',', "").replace('.', '').isdigit():
                    # Used for value checking later on
                    ocr_val = float(ocr_val.replace(',', ''))
                    ocr_type = "number"
                    ocr_valid_field = True
                    balance_found = True


            # if len(ocr_val) == 6:
            #     ocr_type = "text"
            #     ocr_buffer += ocr_val

            #     if len(ocr_buffer) == 17:
            #         # update the ocr_val so that we can place into json
            #         ocr_val = ocr_buffer
            #         vin_tail_found = True
            #     else:
            #         ocr_buffer = ""

            # elif len(ocr_val) == 11:
            #     ocr_type = "text"
            #     ocr_buffer = ocr_val
            #     vin_head_found = True

            # elif ocr_val.find(',') > -1 or ocr_val.find('.') > -1:
            #     # Makes sure that text is infact a digit
            #     if ocr_val.replace(',', "").replace('.', '').isdigit():
            #         # Used for value checking later on
            #         dig = float(ocr_val.replace(',', ''))
            #         ocr_type = "currency"
            #         ocr_val = dig
            #         balance_found = True

            # json template for local storage
            ocr_json = {
                "type": ocr_type,
                "val": ocr_val,
                "xy": ocr_xy,
                "conf": ocr_conf
            }
            # print(json.dumps(ocr_json, indent=2))


            # append the ocr json to column
            if ocr_valid_field:
                ocr_cols.append(ocr_json)
                # reset flag
                ocr_valid_field = False
            # print(json.dumps(ocr_cols, indent=2))

            if vin_head_found and vin_tail_found and balance_found:
                # we found all the parts so add columns to row
                rows_json = {
                    "cols": ocr_cols
                }

                # append the ocr column data to row
                ocr_rows.append(rows_json)
                vin_head_found = False
                vin_tail_found = False


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

    # print(json.dumps(job_json, indent=2))
    # sys.exit()

    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    with open(os.path.join(outpath, 'job.json'), 'w') as outfile:
        json.dump(job_json, outfile, ensure_ascii=True, indent=2)
    
    print("processing completed successfully")