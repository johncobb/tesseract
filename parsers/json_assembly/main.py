import csv, json, getopt
import os,sys
import util

# Input path
inpath = "out/tsv/"
# Output path
outpath = "parsers/json_assembly/json/"
# Root directory path
path = "/Users/tylermeserve/Documents/Tesseract/tesseract/"

# Parses the command line arguments
def argParse(opts, args):
    global inpath, outpath, path
    for opt, arg in opts:
        optc = opt.lower()
        if optc in ['--inpath', '-i']:
            inpath = arg
        elif optc in ['--outpath', '-o']:
            outpath = arg
        elif optc in ['--path', '-p']:
            path = arg

if __name__ == "__main__":

    # if not sys.argv[1:]:
    #     print("Error: please provide arugments.")
    #     sys.exit()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:p', ['--inpath', "--outpath", "--path"])
    except getopt.GetoptError:
        print("Error: invalid argument.")
        sys.exit(2)
    
    if not opts and not args:
        print("Error, no parameters provided")
        sys.exit()
    
    # Multi-OS Support
    slash = ""
    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        slash = "/"
    elif sys.platform == "win32":
        slash = "\\"
    
    # List for the information from the tsv file
    vinbal = []
    # The partial or full vin variable to concatenate
    toAppend = ""
    # Used for naming conventions for when saving the .json file
    # IE:
    # result-001.tsv will return result.json
    filename_prefix = ""
    # Used to sort the page
    pagenum_list = []

    # Concatenates the paths for easier usage
    inpath = path + inpath
    outpath = path + outpath
    
    # Gets the page numbers
    for filename in os.listdir(inpath):
        # Sets the filename_prefix variable and file_extension variable
        if not filename_prefix:
            file_extension = "." + filename.split('.')[-1]
            filename_prefix = filename.split('-')[0]

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

    # Sorts the filename_list properly so the json will match the order of the tsv files
    filename_list = []
    for pagenum in pagenum_list:
        filename_list.append(filename_prefix + "-" + pagenum + file_extension)
    
    # Loops through the file name list
    for item in filename_list:
        # Opens the file currently in the loop
        with open(inpath + slash + item, "r") as tsvfile:
            # Reads the tsv file and converts it to a dictionary
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            # Gets the page number from the file name
            pagenum = int(item.split('.')[0].split('-')[-1])

            # Makes the dictionary for easy access of values
            vinbaldict = {
                "vin": "",
                "balance": "",
                "bbox": "",
                "conf": []
            }

            for row in reader:
                conf = row['conf']
                text = row['text']
                # If text is none then continue
                if not text:
                    continue
                # Removes whitespace from text
                if not text.strip():
                    continue
                # Sets up the bbox variable for the coordinates for later usage
                bbox = "{0} {1} {2} {3}".format(row['left'], row['top'], row['width'], row['height'])
                if len(text) == 6:
                    toAppend += text
                    # Makes sure that text doesn't have any period's or comma's
                    if text.find('.') > -1 or text.find(',') > -1:
                        toAppend = ""
                        continue
                    # Appends the vin number, bbox, and word confidence to the dictionary and vinbal list
                    if len(toAppend) == 17:
                        vinbaldict['vin'] = toAppend
                        vinbaldict['bbox'] = bbox
                        vinbaldict['conf'].append(conf)
                        vinbal.append(vinbaldict)
                        vinbaldict = {
                            "vin": "",
                            "balance": "",
                            "bbox": "",
                            "conf": []
                        }
                    else:
                        toAppend = ""
                elif len(text) == 11:
                    toAppend = text
                    # Appends the word confidence to the list
                    vinbaldict['conf'].append(conf)
                elif text.find(',') > -1 or text.find('.') > -1:
                    # Makes sure that text is infact a digit
                    if text.replace(',', "").replace('.', '').isdigit():
                        # Used for value checking later on
                        dig = float(text.replace(',', ''))
                        if not vinbal:
                            continue
                        
                        if not len(vinbal[-1]['conf']) == 2:
                            continue
                        vinbal[-1]['balance'] = text
                        vinbal[-1]['conf'].append(conf)
            # Json data to put in the json file
            data = []
            for vin in vinbal:
                tojson = {}
                # Prints the vin, balance, and bbox
                print("The vin is: {0}\nThe balance is: {1}\nThe bbox is: {2}".format(vin["vin"], vin["balance"], vin["bbox"]))
                # Checks whether or not the vin is valid
                valid = util.ValidateVIN(vin['vin'])
                # Sets up the bbox coordinates
                bboxsplit = vin['bbox'].split(' ')

                tojson['page'] = str(pagenum)
                tojson['vin'] = vin["vin"]
                tojson['balance'] = vin["balance"]

                if valid[0]:
                    print("Vin is valid!\n\n")
                    tojson['valid'] = True
                else:
                    print("Vin isn't valid!\n\n")
                    tojson['valid'] = True
                
                tojson['x1'] = bboxsplit[0]
                tojson['x2'] = bboxsplit[2]
                tojson['y1'] = bboxsplit[1]
                tojson['y2'] = bboxsplit[3]
                x = 1
                for item in vin['conf']:
                    tojson['conf_{0}'.format(str(x))] = item
                    x += 1
                
                # Appends tojson to data
                data.append(tojson)
            
            json_data = json.dumps(data, indent=4)

            if not os.path.isdir(os.getcwd() + slash + 'json'):
                os.mkdir(os.getcwd() + slash + 'json')

            json_dumps_path = outpath
            if not os.path.isfile(json_dumps_path + slash + filename_prefix + '.json'):
                with open(json_dumps_path + slash + '{0}.json'.format(filename_prefix), 'x') as json_file:
                    print('Created file: {0}.json'.format(filename_prefix))

            with open(json_dumps_path +  slash + '{0}.json'.format(filename_prefix), 'w') as json_file:
                json_file.write(json_data)
                print("Successfully saved data to {0}.json".format(filename_prefix))