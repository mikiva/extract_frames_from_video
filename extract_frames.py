import cv2
from PIL import Image, ImageStat
import numpy as np
from time import time
import sys




def getFrames():
    start = time()
    cap = cv2.VideoCapture(film)
    #cap = cv2.VideoCapture('nemo.mp4')
    number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print "Frames: %d" % number_of_frames
    offset_x = 0
    offset_width = 1
    size = (number_of_frames, 10)
    new_img = Image.new("RGB", size)
    while True:
        success, frame = cap.read()
        if frame is None:
            break

        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        median = ImageStat.Stat(img).median

        new_img.paste(Image.new("RGB", (1,10), tuple(median)), (offset_x,0))

        offset_x += offset_width
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
        
    end = time()
    print "Time elapsed: %d  " % (end - start)
    new_img = new_img.resize((3000, 1000), Image.ANTIALIAS)
    new_img.save("image2.png")
    cap.release()

















def count_frames():
    cap = cv2.VideoCapture(film)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print length
    cap.release()


try:
    film = sys.argv[1]
    getFrames()
except:
    print "Add file"
#count_frames()
#buildImage()
