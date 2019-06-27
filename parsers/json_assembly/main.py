import csv, json, getopt
from lxml import etree, html
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import modules.util as util

inpath = "/Users/tylermeserve/Documents/Tesseract/tesseract/out/tsv/"
outpath = "./json"

def argParse(opts, args):
    global inpath, outpath
    for opt, arg in opts:
        optc = opt.lower()
        if optc in ['--inpath', '-ip']:
            inpath = arg
        elif optc in ['--outpath', '-op']:
            outpath = arg

if __name__ == "__main__":

    if not sys.argv[1:]:
        print("Error: please provide arugments.")
        sys.exit()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ip:op', ['--inpath', "--outpath"])
    except getopt.GetoptError:
        print("Error: invalid argument.")
        sys.exit(2)
    
    if not opts and not args:
        print("Error, no parameters provided")
        sys.exit()

    slash = ""
    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        slash = "/"
    elif sys.platform == "win32":
        slash = "\\"

    vinbal = []
    toAppend = ""
    filename_prefix = ""
    pagenum_list = []
    for filename in os.listdir(inpath):
        if not filename_prefix:
            file_extension = "." + filename.split('.')[-1]
            filename_prefix = filename.split('-')[0]

        page_num = filename.split('-')[-1].split('.')[0]

        if not page_num:
            continue
        
        if page_num.isdigit():
            pagenum = int(page_num)
            pagenum_list.append(page_num)

    pagenum_list.sort()

    filename_list = []
    for pagenum in pagenum_list:
        filename_list.append(filename_prefix + "-" + pagenum + file_extension)
    
    for item in filename_list:
        
        with open(inpath + item, "r") as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            pagenum = int(item.split('.')[0].split('-')[-1])
            tsv_file_name = item.split(".")[0].split('-')[0]
        # hocr_file_path = path + "/hocr/result.hocr"
        # hocr_file_name = hocr_file_path.split('/')[-1]
        # doc = html.parse(hocr_file_path)
            vinbaldict = {
                "vin": "",
                "balance": "",
                "bbox": "",
                "conf": []
            }
        # for element in doc.iter('*'):
            for row in reader:
                conf = row['conf']
                text = row['text']
                if not text:
                    continue
                if not text.strip():
                    continue
                bbox = "{0} {1} {2} {3}".format(row['left'], row['top'], row['width'], row['height'])
                if len(text) == 6:
                    toAppend += text
                    if text.find('.') > -1 or text.find(',') > -1:
                        toAppend = ""
                        continue
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
                    vinbaldict['conf'].append(conf)
                elif text.find(',') > -1 or text.find('.') > -1:
                    if text.replace(',', "").replace('.', '').isdigit():
                        dig = float(text.replace(',', ''))
                        if not vinbal:
                            continue
                        
                        if not len(vinbal[-1]['conf']) == 2:
                            continue
                        vinbal[-1]['balance'] = text
                        vinbal[-1]['conf'].append(conf)
    
            data = []
            for vin in vinbal:
                tojson = {}
                print("The vin is: {0}\nThe balance is: {1}\nThe bbox is: {2}".format(vin["vin"], vin["balance"], vin["bbox"]))
                valid = util.ValidateVIN(vin['vin'])
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
                
                data.append(tojson)
            
            json_data = json.dumps(data, indent=4)

            if not os.path.isdir(os.getcwd() + slash + 'json'):
                os.mkdir(os.getcwd() + slash + 'json')

            json_dumps_path = outpath
            if not os.path.isfile(json_dumps_path + slash + tsv_file_name.split('.')[0] + '.json'):
                with open(json_dumps_path + slash + '{0}.json'.format(tsv_file_name.split('.')[0]), 'x') as json_file:
                    print('Created file: {0}.json'.format(tsv_file_name.split('.')[0]))

            with open(json_dumps_path +  slash + '{0}.json'.format(tsv_file_name.split('.')[0]), 'w') as json_file:
                json_file.write(json_data)
                print("Successfully saved data to {0}.json".format(tsv_file_name.split('.')[0]))