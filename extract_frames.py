import cv2
from PIL import Image, ImageStat
from time import time
import sys
from glob import glob


directory = 'green'

def get_part(width):
    new_img = Image.new("RGB", (width, 10))
    return new_img

def generate_image(number_of_frames, pieces, width):
    start = time()
    cap = cv2.VideoCapture(film)
    

    total_processed = 0


    print "Frames: %d" % number_of_frames

    for piece in range(pieces):
        global directory
        part_start = time()
        current = 0
        #print "Piece: %d" % piece,
        #print "Width: %d" % width, "Frames processed: %d/%d" % (total_processed, number_of_frames),
        offset_x = 0
        offset_width = 1
        size = (width, 10)
        new_img = Image.new("RGB", size)
        while True:
            success, frame = cap.read()
            if frame is None or (current >= width):
                break

            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            median = ImageStat.Stat(img).median

            new_img.paste(Image.new("RGB", (1,10), tuple(median)), (offset_x,0))

            offset_x += offset_width
            current += 1
            total_processed += 1


        print "Piece: %d," % int(piece+1),
        print "Width: %d," % width, "Frames processed: %d/%d," % (total_processed, number_of_frames),
        part = time()
        print "Part time elapsed: %ds" % (part - part_start)
        #new_img = new_img.resize((3000, 1000), Image.ANTIALIAS)
        new_img.save("%s/%05d.png" % (directory, piece))

    end = time()
    print "Total time elapsed: %d  " % (end - start)
    cap.release()



def split_frames_in_parts(number_of_parts):
    parts = 100
    return parts
    
    
def get_number_of_frames():
    cap = cv2.VideoCapture(film)
    number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if number_of_frames % 2 == 1:
        number_of_frames -= 1
    return number_of_frames
    
def puzzle_together(pieces, width):
    img_list = []
    global directory
    print directory
    for filename in glob('%s/*.png' % directory):
        img = Image.open(filename)
        img_list.append(img)

    size = ((width*pieces), 10)
    new_img = Image.new("RGB", size)
    if len(img_list) != pieces:
        raise Exception("inte lika manga bilder som delar")

    for index, image in enumerate(img_list):
        new_img.paste(image, ((width*index),0))

    new_img = new_img.resize((4000,1000), Image.ANTIALIAS)
    new_img.save("export/img%d.png" % time())



def get_width(number_of_frames, pieces):
    width = int(number_of_frames / pieces)
    return width


try:
    film = sys.argv[1]


    number_of_frames = get_number_of_frames()
    pieces = split_frames_in_parts(number_of_frames)
    width = get_width(number_of_frames, pieces)

    generate_image(number_of_frames, pieces, width)

    puzzle_together(pieces, width)

except Exception as e:
    print str(e)

