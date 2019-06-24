import csv, json
from lxml import etree, html
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import modules.util as util

if __name__ == "__main__":
    out_path = "/Users/tylermeserve/Documents/Tesseract/tesseract/out/"

    slash = ""
    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        slash = "/"
    elif sys.platform == "win32":
        slash = "\\"

    vinbal = []
    toAppend = ""

    with open(out_path + 'tsv/result-009.tsv') as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')

    # hocr_file_path = out_path + "/hocr/result.hocr"
    # hocr_file_name = hocr_file_path.split('/')[-1]
    # doc = html.parse(hocr_file_path)

    # for element in doc.iter('*'):
        for row in reader:
            text = row['text']
            if not text:
                continue
            if not text.strip():
                continue
            bbox = "{0} {1} {2} {3}; wconf {4}".format(row['left'], row['top'], row['width'], row['height'], row['conf'])
            if len(text) == 6:
                toAppend += text
                if text.find('.') > -1 or text.find(',') > -1:
                    toAppend = ""
                    continue
                if len(toAppend) == 17:
                    vinbal.append([toAppend, bbox])
                else:
                    toAppend = ""
            elif len(text) == 11:
                toAppend = text
            elif text.find(',') > -1 or text.find('.') > -1:
                if text.replace(',', "").replace('.', '').isdigit():
                    dig = float(text.replace(',', ''))
                    if not vinbal:
                        continue
                    lastindex = vinbal[-1]
                    if len(lastindex) == 3:# or dig <= 1000:
                        continue
                    vinbal[-1].append(text)
                    print(vinbal[-1])
                    print("passed")
    
    data = []
    for vin in vinbal:
        tojson = {}
        print("The vin is: {0}\nThe balance is: {1}\nThe bbox is: {2}".format(vin[0], vin[2], vin[1]))
        valid = util.ValidateVIN(vin[0])

        bboxsplit = vin[1].split(';')
        bboxsplit[1] = bboxsplit[1].rstrip()
        bboxsplit2 = bboxsplit[0].split(' ')

        tojson['vin'] = vin[0]
        tojson['balance'] = vin[2]

        if valid[0]:
            print("Vin is valid!\n\n")
            tojson['valid'] = True
        else:
            print("Vin isn't valid!\n\n")
            tojson['valid'] = True
        
        tojson['x1'] = bboxsplit2[0]
        tojson['x2'] = bboxsplit2[2]
        tojson['y1'] = bboxsplit2[1]
        tojson['y2'] = bboxsplit2[3]
        tojson['x_wconf'] = bboxsplit[1].split(' ')[1]
        
        data.append(tojson)
    
    json_data = json.dumps(data, indent=4)

    if not os.path.isdir(os.getcwd() + slash + 'json'):
        os.mkdir(os.getcwd() + slash + 'json')

    json_dumps_path = os.getcwd() + slash + 'json'
    print(vinbal[0])
    if not os.path.isfile(json_dumps_path + slash + hocr_file_name.split('.')[0] + '.json'):
        with open(json_dumps_path + slash + '{0}.json'.format(hocr_file_name.split('.')[0]), 'x') as json_file:
            print('Created file: {0}.json'.format(hocr_file_name.split('.')[0]))

    with open(json_dumps_path +  slash + '{0}.json'.format(hocr_file_name.split('.')[0]), 'w') as json_file:
        json_file.write(json_data)
        print("Successfully saved data to {0}.json".format(hocr_file_name.split('.')[0]))