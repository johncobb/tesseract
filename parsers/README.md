### Install Virtual Environment
#### RTFM: https://virtualenv.pypa.io/en/stable/installation/
```console
pip install --user virtualenv

# create env with python3
virtualenv -p python3 env
# activate environment
. env/bin/activate
pip install -r requirements.txt

# extract file data
python3 modules/run_test.py out.txt > tmp_file

# stop virtual session
deactivate
```