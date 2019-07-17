# TSV to Json API

<div id='toc'>

## Table of Contents
  [Table of Contents](#toc)
  [Prerequisites](#pre)
  [Installing Pip](#pip)
  [Virtual Environment](#venv)
  [Installing Requirements](#req)
  [Usage](#use)
  [Endpoints](#end)
  [Examples](#ex)

<div id='pre'>

## Prerequisites

- Install a [python 3.7](https://www.python.org/downloads/)
- Install [pip](#pip)
- Install a [Virtual Environment](#venv)
- Install the [requirements](#req)

<div id='pip'>

## Installing Pip

`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

`python get-pip.py --user`

<div id='venv'>

## Install virtualenv  

`pip install --user virtualenv`

Create a folder in tesseract/web/back to house the virtual environment (env). Also, specify this project is using python3.7

`virtualenv -p python3 env`

Activate environment  

`. env/bin/activate`

<div id='req'>

`pip install -r requirements.txt`

To stop the virtual session  

`deactivate`

<div id='use'>

## Usage

Navigate to tesseract/web/back
Activate the [virtual environment](#venv)
```console
python server.py
```

<div id='end'>

## Endpoints

api/upload

<div id='ex'>

## Examples

### Python Example
Refer to test.py

### Curl
```console
curl http://0.0.0.0:3010/api/upload -F 'file=@path/to/file'
```