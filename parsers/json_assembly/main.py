import csv, json, getopt
import os,sys, time
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

    if not sys.argv[1:]:
        print("Error: please provide arugments.")
        sys.exit()
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
    data = []
    # Sorts the filename_list properly so the json will match the order of the tsv files
    filename_list = []
    for pagenum in pagenum_list:
        filename_list.append(filename_prefix + "-" + pagenum + file_extension)
    
    bbox_object = {
        "x1": "",
        "x2": "",
        "y1": "",
        "y2": ""
    }
    # Loops through the file name list
    for item in filename_list:
        pagenum = int(item.split('.')[0].split('-')[-1])
        # Opens the file currently in the loop
        with open(inpath + slash + item, "r") as tsvfile:
            # Reads the tsv file and converts it to a dictionary
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            # Gets the page number from the file name
            
            # Makes the dictionary for easy access of values
            vinbaldict = {
                "vin": "",
                "balance": "",
                "conf": []
            }
            bbox_count = 1
            for row in reader:
                if bbox_count > 3:
                    bbox_count = 1
                conf = row['conf']
                text = row['text']
                # If text is none then continue
                if not text:
                    continue
                # Removes whitespace from text
                if not text.strip():
                    continue
                # Sets up the bbox variable for the coordinates for later usage
                bbox_object['x1'] = row['left']
                bbox_object['x2'] = row['width']
                bbox_object['y1'] = row['top']
                bbox_object['y2'] = row['height']
                if len(text) == 6:
                    toAppend += text
                    # Makes sure that text doesn't have any period's or comma's
                    if text.find('.') > -1 or text.find(',') > -1:
                        toAppend = ""
                        continue
                    # Appends the vin number, bbox, and word confidence to the dictionary and vinbal list
                    if len(toAppend) == 17:
                        vinbaldict['vin'] = toAppend
                        vinbaldict['b{0}'.format(bbox_count)] = bbox_object
                        vinbaldict['conf'].append(conf)
                        vinbal.append(vinbaldict)
                        vinbaldict = {
                            "vin": "",
                            "balance": "",
                            "conf": []
                        }
                        bbox_count += 1
                        bbox_object = {
                            "x1": "",
                            "x2": "",
                            "y1": "",
                            "y2": ""
                        }
                        bbox_count += 1
                    else:
                        toAppend = ""
                elif len(text) == 11:
                    toAppend = text
                    # Appends the word confidence to the list
                    vinbaldict['conf'].append(conf)
                    vinbaldict['b{0}'.format(bbox_count)] = bbox_object
                    bbox_object = {
                        "x1": "",
                        "x2": "",
                        "y1": "",
                        "y2": ""
                    }
                    bbox_count += 1
                elif text.find(',') > -1 or text.find('.') > -1:
                    # Makes sure that text is infact a digit
                    if text.replace(',', "").replace('.', '').isdigit():
                        # Used for value checking later on
                        dig = float(text.replace(',', ''))
                        if not vinbal:
                            continue
                        
                        if not len(vinbal[-1]['conf']) == 2:
                            continue
                        vinbal[-1]['b{0}'.format(bbox_count)] = bbox_object
                        vinbal[-1]['balance'] = text
                        vinbal[-1]['conf'].append(conf)
                        bbox_object = {
                            "x1": "",
                            "x2": "",
                            "y1": "",
                            "y2": ""
                        }
                        bbox_count += 1
            
            for vin in vinbal:
                tojson = {}
                # Prints the vin, balance, and bbox
                # print("The vin is: {0}\nThe balance is: {1}\nThe bbox is: {2}".format(vin["vin"], vin["balance"], vin["bbox"]))
                # Checks whether or not the vin is valid
                valid = util.ValidateVIN(vin['vin'])
                # Sets up the bbox coordinates
                # print(str(pagenum))
                tojson['page'] = str(pagenum)
                tojson['vin'] = vin["vin"]
                tojson['balance'] = vin["balance"]
                i = 1
                numberused = 0
                while True:
                    try:
                        tojson['b{0}'.format(i)] = vin['b{0}'.format(i)]
                        i += 1
                    except KeyError:
                        break
                
                if valid[0]:
                    # print("Vin is valid!\n\n")
                    tojson['valid'] = True
                else:
                    # print("Vin isn't valid!\n\n")
                    tojson['valid'] = True
                x = 1
                for item in vin['conf']:
                    tojson['conf_{0}'.format(str(x))] = item
                    x += 1
                
                # Appends tojson to data
                data.append(tojson)
            if not data:
                continue
            
    json_data = json.dumps(data, indent=4)

    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    json_dumps_path = outpath
    if not os.path.isfile(json_dumps_path + slash + filename_prefix + '.json'):
        with open(json_dumps_path + slash + '{0}.json'.format(filename_prefix), 'x') as json_file:
            print('Created file: {0}.json'.format(filename_prefix))

    with open(json_dumps_path +  slash + '{0}.json'.format(filename_prefix), 'w') as json_file:
        json_file.write(json_data)
        print("Successfully saved data to {0}.json".format(filename_prefix))