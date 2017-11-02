import os, sys
sys.path.insert(0, './Tokenizer')
import text_tokenizer as text
import code_tokenizer as code
import crf as crf
crf.DATA_ROOT = '../Data/'
import evaluation as eva


def regex2File(file):
    code.main(file)
    file_sep = os.path.splitext(file)
    newfile = file_sep[0] + "_codeAnno" + file_sep[1]
    finalfile = file_sep[0] + "_codeAnno" + "_textAnno" + file_sep[1]
    text.main(newfile)
    os.remove(newfile)
    os.rename(finalfile, file_sep[0] + "_predicted" + file_sep[1])
    print("Tokenized file is stored in", file_sep[0] + "_predicted" + file_sep[1])


if __name__ == '__main__':
    # take in 1+ file(s) for processing
    root = '../Data/'
    for file in ['posts_training_clean_old.txt','answers_training_clean.txt']:
        regex2File(root+file)
    eva.evaluate_regex_output('../Data/', 'Regex Performance')
    #crf.sample_output_dual(root+'val_predict.txt', 0.2, '../Data/val_true.txt')
    #crf.cross_validation_dual(0.2)