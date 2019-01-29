
## mac os install via brew
###`brew install tesseract`
###########################`brew install imagemagick`
`brew install gs`

# ubuntu linux install via apt
`sudo apt install tesseract-ocr`
`sudo apt install imagemagick`

# running commands
`tesseract -h` # list options
# pdf to tiff
`convert -density 300 pdf/example.pdf -depth 8 -strip -background white -alpha off out/tiff/out.tiff`
# pdf to png
`convert -density 300 pdf/example.pdf -depth 8 -strip -background white -alpha off out/png/out.png`
# pdf to jpeg
`convert -density 300 pdf/example.pdf -depth 8 -strip -background white -alpha off out/jpeg/out.jpeg`

# example commands
`convert -density 300 pdf/chase_kia.pdf -depth 8 -strip -background white -alpha off out/tiff/out.tiff`
# ocr the intermediate image file to text
`tesseract -l eng out/tiff/out.tiff out/txt/out`
# ocr the intermediate image file to hocr (bounding boxes)
`tesseract -l eng out/tiff/out.tiff result hocr`

# cropping image
# convert image_name -crop pixelsX x pixelsY + pixelOffsetX + pixelOffsetY outputfile
convert out.tiff -crop 600x1800+100+200 cropped.jpg

# extract vin
convert out.tiff -crop 400x1800+10+200 column1.jpg
# extract current principal
convert out.tiff -crop 200x1800+1500+200 column2.jpg

## Resouces
### https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
### https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00
