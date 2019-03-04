# Tesseract Project Extended Information  

### GhostScript:

Using `gs` (GhostScript) instead of `convert` (ImageMagick) when changing between file types (i.e. pdf and tiff) results in a much faster process (2~ seconds vs 30~ with 30 pages). The GhostScript command will result in a file size many times smaller then using ImageMagick but quality is also slightly affected for the worse. Depending on the original quality of the source and the size of characters etc. GhostScript can stil be a valuable alternative becuase of its speed.

##### Example using GhostScript:  
`gs -dBATCH -sDEVICE=tiffg4 -r300x300 -dNOPAUSE -sOutputFile=out/tiff/out.tiff \ pdf/example.pdf`  

##### Example using ImageMagick:  
`convert -density 300 pdf/example.pdf -depth 8 -strip -background white -alpha off out/tiff/out.tiff` 

<br>

### Adding Input Parameters:  

The base project includes a few supported parameters (like a changing to a **tsv** output format). Adding more options is simple, bash stores arguments and they can be recovered and used in several ways. So to add a new option add it as an option in the **if** block at the beginning of the file and in the **if** block surrounding the code to be run with the new option.

##### Example:  
The console command `. runtessrun -tsv` is run thruough this **if** statement

	if [ "$1" == "-tsv" ]; # $1 is where the first set of characters (space-delimited) after 
	# the file (runntessrun) are stored. 
	# If a new option like "foo" is created look for [ "$1" == "-foo" ] as well.

	then  

       parameter="tsv" # "parameter" is a string that now contains the input parameter *tsv*
     
       echo "Option tsv selected" 
         
	else # catches instances where there are no parameters declared at start and uses defualt option
 
        parameter=""
    
        echo "Default txt selected"
    
	fi
	
Parameter is later checked before running certain blocks of code

Example:

	if [ "$parameter" == "tsv" ]; then
			# do stuff for tsv
	elif [ "$parameter" == "foo" ]; 
	then
			# do stuff for foo
	else
	      # do default stuff      
	fi
