#tagseq1 = [('In', 'IN'), ('this', 'DT'), ('case', 'NN'), ('you', 'PRP'), ('might', 'MD'), ('consider', 'VB'), ('using', 'VBG'), ('a', 'DT'), ('<', 'JJ'), ('code', 'NN'), ('>', 'NN'), ('set', 'VBN'), ('<', 'NNP'), ('/code', 'NNP'), ('>', 'NNP'), (',', ','), ('especially', 'RB'), ('if', 'IN'), ('the', 'DT'), ('list', 'NN'), ('is', 'VBZ'), ("n't", 'RB'), ('meant', 'VBN'), ('to', 'TO'), ('store', 'VB'), ('duplicates', 'NNS'), ('.', '.')]
#tagseq=[('While', 'IN'), ('reading', 'VBG'), ('about', 'IN'), ('classes', 'NNS'), (',', ','), ('it', 'PRP'), ('goes', 'VBZ'), ('on', 'IN'), ('to', 'TO'), ('say', 'VB'), ('that', 'IN'), ('in', 'IN'), ('Python', 'NNP'), ('there', 'EX'), ('is', 'VBZ'), ('no', 'DT'), ('need', 'NN'), ('to', 'TO'), ('declare', 'VB'), ('instance', 'NN'), ('variables', 'NNS'), ('.', '.')]
#tagseq4=[('What', 'WP'), ('is', 'VBZ'), ('the', 'DT'), ('behavior', 'NN'), ('of', 'IN'), ('the', 'DT'), ('pre-increment/decrement', 'JJ'), ('operators', 'NNS'), ('(', '('), ('++/', 'NNP'), ('--', ':'), (')', ')'), ('in', 'IN'), ('Python', 'NNP'), ('?', '.')]
#tagseq=[('Here', 'RB'), ('is', 'VBZ'), ('some', 'DT'), ('sample', 'JJ'), ('output', 'NN'), ('I', 'PRP'), ('ran', 'VBD'), ('on', 'IN'), ('my', 'PRP$'), ('computer', 'NN'), (',', ','), ('converting', 'VBG'), ('it', 'PRP'), ('to', 'TO'), ('a', 'DT'), ('string', 'NN'), ('as', 'RB'), ('well', 'RB'), ('.', '.')]
#irregular_1 = [('&', 'CC'), ('gt', 'NN'), (';', ':'), ('&', 'CC'), ('gt', 'NN'), (';', ':'), ('&', 'CC'), ('gt', 'NN'), (';', ':'), ('l', 'CC'), ('=', 'JJ'), ('list', 'NN'), ('(', '('), ('1', 'CD'), (',', ','), ('2', 'CD'), (',', ','), ('3', 'CD'), (')', ')')]
#Irregular5=[('I', 'PRP'), ('am', 'VBP'), ('hoping', 'VBG'), ('it', 'PRP'), ('is', 'VBZ'), ('possible', 'JJ'), ('to', 'TO'), ('do', 'VB'), ('without', 'IN'), ('tinkering', 'VBG'), ('with', 'IN'), ('sys.path', 'NN'), ('.', '.')]
#tagseq7 = [('while', 'IN'), ('len', 'VBN'), ('(', '('), ('alist', 'NN'), (')', ')'), ('&', 'CC'), ('gt', 'NN'), (';', ':'), ('0', 'CD'), (':', ':'), ('alist.pop', 'NN'), ('(', '('), (')', ')')]
tagseq = [('def', 'NN'), ('uniq', 'NN'), ('(', '('), ('input', 'NN'), (')', ')'), (':', ':')]

latex = ''
for tag in tagseq:
    latex+="\inline{"+tag[0]+'}{'+tag[1]+'} '
print(latex)