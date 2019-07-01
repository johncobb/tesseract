import csv, json, getopt
import os, sys, time
import util

# Input path
in_file = ""
# Output path
outpath = ""
# Root directory path
path = ""
# Config file path
config = ""
# The session id for file naming conventions
sessionid = ""

# Parses the command line arguments
def argParse(opts, args):
    global in_file, outpath, path, sessionid, config
    for opt, arg in opts:
        optc = opt.lower()
        if optc in ['--infile', '-i']:
            in_file = arg
        elif optc in ['--outpath', '-o']:
            outpath = arg
        elif optc in ['--path', '-p']:
            path = arg
        elif optc in ['--config', '-c']:
            config = arg
        elif optc in ['-s', '--sessionid']:
            sessionid = arg

# Checks if the arguments are valid directories/file names
def argChecker():
    global path, in_file, outpath, config, sessionid
    if not path or not in_file or not outpath or not config or not sessionid:
        print("Please pass the path, in_file, outpath, config, and sessionid arguments.")
        sys.exit()

    if not os.path.isfile(os.path.join(path, in_file)):
        print("Please enter a valid file path/filename for the input file.")
        sys.exit()
    
    if not os.path.isfile(config):
        print("Please enter a valid file path for the config file.")
        sys.exit()

    if not os.path.isdir(path + outpath):
        print("Please enter a valid directory path for the output path.")
        sys.exit()

def set_column_object(fields):
    json_col_obj = {
        "cols":
        [
            
        ]
        
    }
    for item in fields:
        json_item_obj = {
                "type": item,
                "val": "",
                "xy": [],
                "conf": "",
                "attr": []
            }
        json_col_obj['cols'].append(json_item_obj)
    return json_col_obj
        

def set_json_object():
    return \
    {
        "job": {
            "config_id": "really_long_conig_file_name",
            "id": 1561780205,
            "pages": [
            ]
        }
    }

def runner():
    global path, in_file, outpath, config

    # Multi-OS Support
    slash = ""
    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        slash = "/"
    elif sys.platform == "win32":
        slash = "\\"
    else:
        print("Unsupported platform... Please use linux, mac os, or windows.")
        sys.exit()
    
    pagenum = in_file.split("-")[1].split(".")[0]    

    try:
        with open(config, "r") as config_file:
            config_obj = json.load(config_file)
    except json.JSONDecodeError as e:
        print("{0}: Line {1} Column {2}".format(e.msg, e.lineno, e.colno))
        sys.exit()
    write_file_name = "result-{0}.json".format(pagenum)
    fields = []
    funcs = []
    for item in config_obj['config']['fields']:
        fields.append(item['type'])
        funcs.append(item['func'])
    if not os.path.isdir(os.path.join(os.path.join(path, outpath), sessionid)):
        os.mkdir(os.path.join(os.path.join(path, outpath), sessionid))
    
    out_file_name = os.path.join(os.path.join(path, outpath), sessionid) + slash + write_file_name
    
    json_obj = set_json_object()
    column_obj = set_column_object(fields)
    # if not os.path.isfile(out_file):
    #     open(out_file, "w")
    
    # with open(out_file, "a+") as write_file:
    infile_name = path + slash + in_file
    vinbal =[]
    row_obj = {
        'page': pagenum,
        'rows':
        [
            
        ]
    }
    with open(infile_name, "r") as tsvfile:
        reader = csv.DictReader(tsvfile, dialect="excel-tab")

        prev_conf = -1
        prev_xy = []
        toAppend = ""
        for row in reader:
            conf = row['conf']
            text = row['text']
            xy = [row['left'], row['top'], row['width'], row['height']]
            if len(text) == 6:
                toAppend += text
                
                if text.find('.') > -1 or text.find(',') > -1:
                    toAppend = ""
                    continue
                if len(toAppend) == 17:
                    i = 0
                    while i < len(column_obj['cols']):
                        if column_obj['cols'][i]['type'].lower() == "vin":
                            column_obj['cols'][i]['val'] = toAppend
                            column_obj['cols'][i]['xy'].append(xy)
                            column_obj['cols'][i]['xy'].append(prev_xy)
                            wconf = (int(conf) + int(prev_conf))/2
                            column_obj['cols'][i]['conf'] = wconf
                            valid = util.ValidateVIN(toAppend)
                            if valid[0]:
                                column_obj['cols'][i]['attr'].append(True)
                            else:
                                column_obj['cols'][i]['attr'].append(False)
                            prev_conf = -1
                            prev_xy = []
                        i += 1
            elif len(text) == 11:
                toAppend = text
                prev_xy = xy
                prev_conf = conf
            elif len(text) == 17:
                i = 0
                while i < len(column_obj['cols']):
                    if column_obj['cols'][i]['type'].lower() == "vin":
                        column_obj['cols'][i]['val'] = text
                        column_obj['cols'][i]['xy'].append(xy)
                        column_obj['cols'][i]['conf'] = conf
                        valid = util.ValidateVIN(toAppend)
                        if valid[0]:
                            column_obj['cols'][i]['attr'].append(True)
                        else:
                            column_obj['cols']['i']['attr'].append(False)
                    i += 1
            elif text.find(',') > -1 or text.find('.') > -1:
                if text.replace(',', "").replace('.', "").isdigit():
                    dig = float(text.replace(',', ""))

                    i = 0
                    while i < len(column_obj['cols']):
                        if column_obj['cols'][i]['type'].lower() == "currency":
                            column_obj['cols'][i]['val'] = dig
                            column_obj['cols'][i]['conf'] = conf
                            column_obj['cols'][i]['xy'].append(xy)
                        i += 1
            i = 0
            while i < len(column_obj['cols']):
                if not str(column_obj['cols'][i]['val']):
                    broken = True
                    break
                i += 1
            if broken:
                broken = False
                continue
            row_obj['rows'].append(column_obj)
            json_obj['job']['pages'].append(row_obj)
            row_obj = {
                'page': pagenum,
                'rows':
                [

                ]
            }
            column_obj = set_column_object(fields)
    with open(out_file_name, 'w+') as out_file:
        json_data = json.dumps(json_obj, indent=4)
        out_file.write(json_data)

if __name__ == "__main__":

    if not sys.argv[1:]:
        print("Error: please provide arugments.")
        sys.exit()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:p:c:s:', ['--infile', "--outpath", "--path", "--config", "--sessionid"])
    except getopt.GetoptError:
        print("Error: invalid argument.")
        sys.exit(2)

    if not opts and not args:
        print("Error, no parameters provided")
        sys.exit()
    
    argParse(opts, args)
    argChecker()
    runner()