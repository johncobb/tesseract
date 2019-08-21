import requests, os
import sys

path = "/Users/tylermeserve/Documents/Tesseract/tesseract/out/tsv/0"
files1 = [('file', open(os.path.join(path, "result-004.tsv"), 'rb')), ('file', open(os.path.join(path, 'result-006.tsv'), 'rb'))]
files1 = [('file', open(os.path.join(path, file), 'rb')) for file in sorted(os.listdir(path))]
params = {'id': 0, 'configid': 1}
IP = ''

if not os.path.isfile(os.path.join(os.getcwd(), 'server_secrets.txt')):
    print('Go to server_secrets.txt and replace "(your api domain) with your api domain.')
    with open(os.path.join(os.getcwd(), 'server_secrets.txt'), 'w+') as f:
        f.write('IP=(your api domain)')
        pass

with open(os.path.join(os.getcwd(), 'server_secrets.txt'), 'r') as f:
    for line in f.readlines():
        if line.startswith('IP='):
            IP = line.replace('IP=', '')
            
if not IP:
    print('Go to server_secrets.txt and replace "(your api domain) with your api domain."')
    sys.exit()
r = requests.post('{0}/api/upload'.format(IP), files=files1, params=params)


for file in files1:
    file[1].close()

print(r.status_code)
print(r.text)