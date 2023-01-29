# console youtube video player
 Python program to download and display videos from Youtube on your console
 
# This was thrown together in one night!
Quicly made python script that downloads and plays videos as text on your console. 

### Running
On Windows open the run.bat file.  
Or:  
Install the dependencies: `pip install -r requirements.txt`  
And run `python player.py` from the command line

### Arguments
You can use these optional arguments:  
- `--url [url]` to specify the youtube url
- `--verbose` to display some additional file information
- `--file [path]` to play some local file on the computer

### Issues
- Some file formats are broken
- File permissions issues
- Error handling not great
- Playback can be a bit messy
