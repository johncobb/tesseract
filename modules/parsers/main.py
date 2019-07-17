import sys
import os
import getopt
import json
from parser_kia_tsv import runner

path = ""
inp = ""
out = ""
tid = ""
configid = ""

def argparsing(opts, args):
    global path, inp, out, tid, configid
    for opt, arg in opts:
        optc = opt.lower()
        if optc in ['--input', '-i']:
            if os.path.isdir(arg):
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
        elif optc in ['--configid', '-c']:
            if arg.isdigit():
                if int(arg) > 0:
                    configid = arg
            elif arg.lower() == 'latest':
                configid = 1

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
        opts, args = getopt.getopt(sys.argv[1:], 'p:i:o:t:c:', ['--path', '--input', '--output', '--tid', '--configid'])
    except getopt.GetoptError as e:
        print("Error: Invalid arguments!")
        sys.exit(1)

    argparsing(opts, args)

    json_data = runner(path, inp, tid, configid)

    saveJson(json_data)

    # ripper(out, tid)