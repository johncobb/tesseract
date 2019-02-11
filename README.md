
### Mac OS install via brew
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

### Test tesseract, imagemagick, and gs installs by issuing the following commands:
```console
tesseract --version
convert -version # imagemagick version
gs --version # ghostscript version

```

### pdf to tiff
```console
convert -density 300 pdf/example.pdf -depth 8 -strip -background white -alpha off out/tiff/out.tiff
```

### crop two columns of data and append into one combined image
Tip: make sure to pad the filename with leading zeros so that the files enumerate
in the correct order when we go to splice later on. ie: col1-%03d.jpeg
```console

convert out/tiff/out.tiff -crop 400x2550+10+200 out/jpeg/col1-%03d.jpeg
convert out/tiff/out.tiff -crop 200x2550+1500+200 out/jpeg/col2-%03d.jpeg
# below we combine page 4 from col1-4.jpeg and col2-4.jpeg into combined.jpeg
convert out/jpeg/col1-4.jpeg out/jpeg/col2-4.jpeg +append out/jpeg/combined.jpeg
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

### runtessrun script
Prior to running the runtessrun script navigate to the parsers folder and setup the virutal environment.
Follow the instructions in the parsers README.md. Finally, modify the path labeled (TODO: Modify Path) so that the scripts reference the correct path.
```console
. runtessrun
```


### Resources
#### https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
#### https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00
