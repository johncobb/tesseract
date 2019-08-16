from parsers.lenders.chase.parser_kia import Kia

import sys, os
import getopt
import json
import re
import io

inp = ''
out = ''
kia = Kia()

def argparsing(opts, args):
    global inp, out
    for opt, arg in opts:
        optc = opt.lower()
        if optc in ['--input', '-i']:
            if os.path.isdir(arg):
                inp = arg
        elif optc in ['--output', '-o']:
            out = arg
            if not os.path.isdir(out):
                os.mkdir(out)

def date_regex(ocr_val):
    if re.match(r'^(?:(?:(?:0?[13578]|1[02])(\/|-|\.)31)\1|(?:(?:0?[1,3-9]|1[0-2])(\/|-|\.)(?:29|30)\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:0?2(\/|-|\.)29\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:(?:0?[1-9])|(?:1[0-2]))(\/|-|\.)(?:0?[1-9]|1\d|2[0-8])\4(?:(?:1[6-9]|[2-9]\d)?\d{2})', ocr_val):
        return True
    return False

def check_leap_year(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def check_month(month):
    return month > 0 and month <= 12

def check_day(day, month, leap_year):
    monthlist = {
        '31': [1, 3, 5, 7, 8, 10, 12],
        '30': [4, 6, 9, 11],
        '28': [2],
    }
    
    if not check_month(month):
        return (False, 'Invalid month')
    
    if month in monthlist['31']:
        return (True, 'Passed') if day >= 1 and day <= 31 else (False, 'Failed')
    elif month in monthlist['30']:
        return (True, 'Passed') if day >= 1 and day <= 30 else (False, 'Failed')
    elif month in monthlist['28'] and not leap_year:
        return (True, 'Passed') if day >= 1 and day <= 28 else (False, 'Failed')
    elif month in monthlist['28'] and leap_year:
        return (True, 'Passed') if day >= 1 and day <= 29 else (False, 'Failed')

def processsing(item, pat=None, is_json=False):
    global inp, out, kia
    
    if is_json:
        item.seek(0)
        json_file = io.StringIO(item.read().decode())
        json_data = json.load(json_file)
    else:
        try:
            json_data = json.load(open(os.path.join(inp, 'job.json'), 'r'))
        except json.JSONDecodeError as e:
            print('Error: Couldn\'t load the JSON File')
            sys.exit(1)
    job_data = json_data['job']
    post_processing_json = {
        'job': {
            'config_id': job_data['config_id'],
            'id': job_data['id'],
            'pages': []
        }
    }
    
    for page in json_data['job']['pages']:
        rows_json = {
            'page': page['page'],
            'rows': []
        }
        for row in page['rows']:
            if not row:
                rows_json['rows'].append(row)
                continue
            cols_json = {
                'cols': []
            }
            for col in row['cols']:
                val = col['val']
                col_json = col.copy()
                if col['attr']:
                    cols_json['cols'].append(col_json)
                    continue
                if col['type'] == 'text':
                    result = kia.fixVIN(val)
                    if result[0]:
                        val = result[2]
                        col_json['val'] = val
                        col_json['attr'] = True
                    else:
                        col_json['attr'] = False
                    cols_json['cols'].append(col_json)
                elif col['type'] == 'date':
                    if val.find('=') > -1:
                        val = val.replace('=', '')
                    first2 = val[0: 2]
                    year = val[-4:]
                    index = -1
                    if (year.find('/') > -1 or year.find('.') > -1 or year.find('-') > -1):
                        for item in year:
                            if item == '/' or item == '.' or item == '-':
                                index = year.index(item) + 1
                                break
                            else:
                                index = 0
                                
                    if not len(year[index:]) >= 1 and not len(year[index:]) <= 4:
                        print('Error: Invalid Year')
                        sys.exit(1)
                        
                    is_leap_year = check_leap_year(int(year[index:]))
                    date_check = check_day(int(val[3:5]), int(val[0:2]), is_leap_year)
                    
                    if date_check[0]:
                            # if len(year[index:]) >= 1 and len(year[index:]) <= 4:
                        col_json['val'] = val
                        col_json['attr'] = True
                    else:
                        col_json['val'] = val
                        col_json['attr'] = False
                        
                    cols_json['cols'].append(col_json)
            rows_json['rows'].append(cols_json)
        post_processing_json['job']['pages'].append(rows_json)
    
    return post_processing_json

def runner():
    global inp, out
    
    if not sys.argv[1]:
        print("Error: No arguments provided!")
        sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:', ['--input', '--output'])
    except getopt.GetoptError as e:
        print("Error: Invalid arguments!")
        sys.exit(1)
        
    argparsing(opts, args)
    
    json_data = processsing(inp)
    
    with open(os.path.join(out, 'final.json'), 'w+') as json_file:
        json.dump(json_data, json_file, indent=2)
        
    print('Sucessfully parsed the JSON file.')
    
if __name__ == '__main__':
    runner()