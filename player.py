import os
import sys
import time
import argparse
import youtube_dl
import subprocess
from PIL import Image

FRAMETIMES = {
    "FPS60" : 0.0167,
    "FPS50" : 0.0200,
    "FPS30" : 0.0333,
    "FPS24" : 0.0417,
    "FPS15" : 0.0666,
    "FPS04" : 0.2500,
    "FPS01" : 1.0000
} 

CURRENTDIR = os.getcwd()

VIDEO_FILE_PATH = os.path.join(os.path.normpath(CURRENTDIR + "/temp/temp_video/"), "")
TEMP_FRAME_PATH = os.path.join(os.path.normpath(CURRENTDIR + "/temp/temp_frames/"), "")
TEXT_FRAME_PATH = os.path.join(os.path.normpath(CURRENTDIR + "/temp/text_frames/"), "")

if not os.path.exists(TEMP_FRAME_PATH):
    os.makedirs(TEMP_FRAME_PATH)

if not os.path.exists(TEXT_FRAME_PATH):
    os.makedirs(TEXT_FRAME_PATH)

if not os.path.exists(VIDEO_FILE_PATH):
    os.makedirs(VIDEO_FILE_PATH)


##WEBHOOKURL = "https://discord.com/api/webhooks/833675063160209448/77JJTry-2Lgb3VvD9tatnBq1F9lYRIL6KVu_U5MOCR6Hi64EaLRXqLxvIAeRtXZNIphH"

verbose = False

def mainFunction(url):

    def getFrames():

        for file in os.listdir(TEMP_FRAME_PATH): os.remove(TEMP_FRAME_PATH + file)
        for file in os.listdir(TEXT_FRAME_PATH): os.remove(TEXT_FRAME_PATH + file)
        for file in os.listdir(VIDEO_FILE_PATH): os.remove(VIDEO_FILE_PATH + file)

        os.system("cls")
        print("Downloading video..")
        youtube = youtube_dl.YoutubeDL({'outtmpl': VIDEO_FILE_PATH + '/vid', 'resolution': '480p'})
        youtube.download([url])

        if not verbose:
            verboseString = ">nul 2>&1"
            
        else:
            verboseString = ""

        #os.system("copy " + CURRENTDIR + "\\vid.* " + VIDEO_FILE_PATH + verboseString)

        files = os.listdir(VIDEO_FILE_PATH)

        #os.system("ffmpeg -i " + VIDEO_FILE_PATH + "vid.mkv -c:v libx264 " + VIDEO_FILE_PATH + "temp_vid.mp4 " + verboseString)
        
        os.system("cls")
        #print("Extracting frames..", files[0])
        #print("ffmpeg -i " + VIDEO_FILE_PATH + files[0] + TEMP_FRAME_PATH + "frame%04d.jpg " + verboseString)
        os.system("ffmpeg -i " + VIDEO_FILE_PATH + files[0] + " " + TEMP_FRAME_PATH + "frame%04d.jpg " + verboseString)

    def imageToAscii():
        
        files = os.listdir(TEMP_FRAME_PATH)

        #image_path = imgpath
        img = Image.open(TEMP_FRAME_PATH  + "frame0001.jpg")

        # resize the image
        width, height = img.size
        aspect_ratio = height/width
        new_width = 100
        new_height = aspect_ratio * new_width * 0.55

        os.system("mode con: cols=100 lines=" + str(int(new_height)))

        #os.system("cls")
        for i in range(len(files)):
            
            print("Converting frames to text.. [" + str(i) + "\\" + str(len(files)) + "]", end="\r")

            #image_path = imgpath
            img = Image.open(TEMP_FRAME_PATH  + files[i])

            img = img.resize((new_width, int(new_height)))
            # new size of image
            # print(img.size)

            # convert image to greyscale format
            img = img.convert('L')

            pixels = img.getdata()

            # replace each pixel with a character from array
            chars = [" ", ".",":","!","*","%","$","@","&","#","S","*"]
            
            
            new_pixels = [chars[pixel//26] for pixel in pixels]
            new_pixels = ''.join(new_pixels)

            # split string of chars into multiple strings of length equal to new width and create a list
            new_pixels_count = len(new_pixels)
            ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
            ascii_image = "\n".join(ascii_image)

            #print(TEXT_FRAME_PATH + filename + ".txt")

            # write to a text file.
            with open(TEXT_FRAME_PATH + files[i] + ".txt", "w") as f:
                f.write(ascii_image)

    def printFrames():
        
        videoFile = os.listdir(VIDEO_FILE_PATH)
        framerate = eval(subprocess.getoutput("ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate " + VIDEO_FILE_PATH + videoFile[0]))
        

        files = os.listdir(TEXT_FRAME_PATH)
        print(framerate)
        for filename in files:
            print("\r")
            timeStart = time.time()
            
            with open((TEXT_FRAME_PATH + filename), "r") as f:
                    

                    print("".join(map(str, f.readlines())))
                    #os.system("clear")

            
            #delta = time.time() - timeStart
            time.sleep(1/framerate)

        input("Press enter to quit")

    getFrames()
    imageToAscii()
    printFrames()


parser = argparse.ArgumentParser(description='Console ASCII video player')
parser.add_argument('--url', metavar='URL', type=str,
                    help='Youtube video url')

parser.add_argument('--verbose', type=bool,
                    help='Display convertion and downlaod info')
"""
parser.add_argument('--file', metavar='FILE', type=str,
                    help='Path to a video local file')
"""

args = parser.parse_args()

if args.verbose:
    verbose = True

if args.url:
    mainFunction(args.url)

else:
    url = input("Liitä youtube url: ")
    mainFunction(url)
