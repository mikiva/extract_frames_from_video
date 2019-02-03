import cv2
from PIL import Image, ImageStat
from time import time
import sys
from glob import glob


directory = sys.argv[2]
export_dir = sys.argv[3]
interval = 1
def get_part(width):
    new_img = Image.new("RGB", (width, 10))
    return new_img

def generate_image(number_of_frames, pieces, width, interval):
    start = time()
    cap = cv2.VideoCapture(film)
    

    total_processed = 0


    for piece in range(pieces):
        global directory
        part_start = time()
        current = 0
        offset_x = 0
        offset_width = 1
        size = (width, 10)
        new_img = Image.new("RGB", size)
        while True:
            for x in range(interval):
                success, frame = cap.read()
            if frame is None or (current >= width):
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            median = ImageStat.Stat(img).median

            new_img.paste(Image.new("RGB", (1, 10), tuple(median)), (offset_x, 0))

            offset_x += offset_width
            current += 1
            total_processed += 1


        print "Piece: %d/%d," % (int(piece+1), pieces),
        print "Width: %d," % width, "Frames processed: %d/%d," % (total_processed, int(pieces*width)),
        part = time()
        print "Part time elapsed: %ds" % (part - part_start)
        new_img.save("%s/%05d.png" % (directory, int(piece+1)))

    end = time()
    print "Total time elapsed: %d  " % (end - start)
    cap.release()


# TODO: Dela upp relativt till antal frames
def split_frames_in_parts(number_of_frames):
    parts = 10
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
    global export_dir
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

    new_img = new_img.resize((8000,1000), Image.ANTIALIAS)
    img_filename = "%s_%d.png" % (export_dir, time())
    new_img.save(img_filename)


def get_width(number_of_frames, pieces, interval):

    width = int(int(number_of_frames/interval) / pieces)
    return width

def get_interval(number_of_frames):

    if (number_of_frames < 15000):
        return 1
    for x in range(1, 200):
        if int(number_of_frames / x) < 15000 and number_of_frames % x < 20:
            return x
    return 10

try:
    film = sys.argv[1]

    print "FILM: %s" % film

    total_number_of_frames = get_number_of_frames()
    interval = get_interval(total_number_of_frames)
    pieces = split_frames_in_parts(int(total_number_of_frames/interval))
    width = get_width(total_number_of_frames, pieces, interval)
    frames_to_be_processed = int(pieces*width)

    print "Total Frames: %d, Frames to be processed frames: %d, Frame Interval: %d, Pieces: %d, Piece Width: %d" \
    %  (total_number_of_frames, frames_to_be_processed, interval, pieces, width)
    generate_image(frames_to_be_processed, pieces, width, interval)

    puzzle_together(pieces, width)

except Exception as e:
    print str(e)

