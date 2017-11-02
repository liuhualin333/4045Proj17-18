import text_tokenizer as text
import code_tokenizer as code
import os, sys


def main(file):
    code.main(file)
    file_sep = os.path.splitext(file)
    newfile = file_sep[0] + "_codeAnno" + file_sep[1]
    finalfile = file_sep[0] + "_codeAnno" + "_textAnno" + file_sep[1]
    text.main(newfile)
    os.remove(newfile)
    os.rename(finalfile, file_sep[0] + "_annotated" + file_sep[1])


if __name__ == '__main__':
    # take in 1+ file(s) for processing
    for file in sys.argv[1:]:
        main(file)