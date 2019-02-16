## Installing a Virtual Environment
#### Reference : https://virtualenv.pypa.io/en/stable/installation/

#### Prerequisites:

Installing PiP
`
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --user
`

### Install virtualenv  

`pip install --user virtualenv`

Create a folder in tesseract/parsers to house the virtual environment (env). Also, specify this project is using python3  

`virtualenv -p python3 env`


`
Activate environment  

`. env/bin/activate` 

`pip install -r requirements.txt`

Extract file data  

`python3 modules/run_test.py out.txt > tmp_file`

To stop the virtual session  

`deactivate`
