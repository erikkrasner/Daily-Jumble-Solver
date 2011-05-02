#!/usr/bin/env python

import os, sys, re

for file_name in os.listdir(sys.argv[1]):
    raw_dict_file = open(sys.argv[1] + "/" + file_name,'r')
    popularity = re.search(r'\d+\Z',file_name).group(0)
    for line in raw_dict_file:
        word = line[:-1]
        letter = sorted(word)[0]
        length = len(word)
        dict_file = open("word_lists/%s%d" % (letter,length),'a')
        dict_file.write('%s %s\n' % (word, popularity))
        dict_file.close()
    raw_dict_file.close()
