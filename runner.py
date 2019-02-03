import os
from time import time

start = time()
for x in range(1,9):
    os.system("python extract_frames.py harry/h{0}.mkv harry/{0} harry/export/h{0}".format(x))

end = time()

print "Alla filmer: %ds" % (end - start)