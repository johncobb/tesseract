import requests, os

path = "/Users/tylermeserve/Documents/Tesseract/tesseract/out/tsv"
files1 = [('file', open(os.path.join(path, "result-004.tsv"), 'rb')), ('file', open(os.path.join(path, 'result-006.tsv'), 'rb'))]
print(files1[0])
params = {'id': 0, 'configid': 1}

r = requests.post('http://0.0.0.0:3010/api/upload', files=files1, params=params)

print(r.status_code)
print(r.text)