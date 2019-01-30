
#### Mac OS install via brew
```console
brew install tesseract
brew install imagemagick
brew install gs
```

### Ubuntu/Linux install via apt
```console
sudo apt install tesseract-ocr
sudo apt install imagemagick
```

### Test tesseract install by issuing the following command to list options
```console
tesseract -h # list options
```

### pdf to tiff
```console
convert -density 300 pdf/example.pdf -depth 8 -strip -background white -alpha off out/tiff/out.tiff
```

### crop one column of data
```console
convert out/tiff/out.tiff -crop 400x1800+10+200 out/tiff/column1.tiff
```

### Run tesseract on file
```console
# run tesseract with custom parameters
# oem 1 (nerual nets LSTM only)
# psm 3 (page segmentation mode)  PSM_AUTO
tesseract -l eng --oem 1 --psm 3 out/tiff/column1.tiff out/txt/out
```

### Write hocr file (bounding coordinates)
```console
tesseract -l eng out/tiff/column1.tiff out/hocr/result hocr
```

### Resources
#### https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
#### https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00
