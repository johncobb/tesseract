import sys
import os
import getopt
import json
from parser_kia import Kia
from parser_kia_tsv import runner

path = ""
inp = ""
out = ""
tid = ""

def argparsing(opts, args):
    global path, inp, out, tid
    for opt, arg in opts:
        optc = opt.lower()
        if optc in ['--path', '-p']:
            path = arg
        elif optc in ['--input', '-i']:
            inp = arg
        elif optc in ['--output', '-o']:
            out = arg
        elif optc in ['--tid', '-t']:
            tid = arg
            if tid.isdigit():
                tidint = int(tid)
                if not tidint > -1:
                    print("Error: Invalid epoch time!")
                    sys.exit(1)

def saveJson(json_data):
    global path, inp, out, tid
    outdir = os.path.join(path, os.path.join(out, tid))
    outpath = os.path.join(outdir, "job.json")

    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    with open(outpath, 'w+') as outfile:
        json.dump(json_data, outfile, ensure_ascii=True, indent=2)

if __name__ == "__main__":

    if not sys.argv[1]:
        print("Error: No arguments provided!")
        sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:i:o:t:', ['--path', '--input', '--output', '--tid'])
    except getopt.GetoptError as e:
        print("Error: Invalid arguments!")
        sys.exit(1)

    argparsing(opts, args)
    # file = sys.argv[1] 

    # parser_kia = Kia()

    # parser_kia.parse(file)

    json_data = runner(path, inp, tid)
    saveJson(json_data)