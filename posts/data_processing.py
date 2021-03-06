'''	
	This file is to convert training data with html tags to training data without html tags(except for <code></code>)
	Clean data will be saved at file_clean.txt 
'''
import re
import sys
import os


def cleanhtml(raw_html):
    cleanr = re.compile('<(?!code|/code).*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def main():
    for file in sys.argv[1:]:
        data = open(file).read()
        cleandata = cleanhtml(data)
        file_sep = os.path.splitext(file)
        with open(file_sep[0] + "_clean" + file_sep[1], 'w') as new_file:
            new_file.write(cleandata)


if __name__ == '__main__':
    main()
