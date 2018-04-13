import os, stat

path = '/home/test/test/bin'

print stat.ST_MODE(os.stat(path).st_mode)