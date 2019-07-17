import requests, os

path = "/Users/tylermeserve/Documents/Tesseract/tesseract/out/tsv"
files1 = [('file', open(os.path.join(path, "result-005.tsv"), 'rb')), ('file', open(os.path.join(path, 'result-006.tsv'), 'rb'))]

r = requests.post('http://0.0.0.0:3010/api/upload', files=files1)

print(r.status_code)
print(r.text)