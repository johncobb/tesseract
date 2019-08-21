import requests, os

path = "/Users/tylermeserve/Documents/Tesseract/tesseract/out/tsv/0"
files1 = [('file', open(os.path.join(path, "result-004.tsv"), 'rb')), ('file', open(os.path.join(path, 'result-006.tsv'), 'rb'))]
files1 = [('file', open(os.path.join(path, file), 'rb')) for file in sorted(os.listdir(path))]
params = {'id': 0, 'configid': 1}

r = requests.post('https://mmljg0chkd.execute-api.us-east-1.amazonaws.com/dev/api/upload', files=files1, params=params)


for file in files1:
    file[1].close()

print(r.status_code)
print(r.text)