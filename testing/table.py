info = {'python': ['Python', 'python', 'pythonic', 'Pythonic', "'pythonic", "'python", 'pythoners', 'pythons', 'PYTHON', 'Pythons', "Python's", 'pythonators', 'Pythonically', "'Python", 'Pythoneers', 'Pythoning', "'Pythonic"],
'i': ['I', 'i', "'i'", "'I'"],
'get': ['get', 'getting', 'gets', 'Getting', 'GET', 'Get', "'getting", "'GET", "'get", 'Gets', "'gets", "'Get"],
'list': ['list', 'List', 'listing', 'Lists', 'lists', "'list", 'listed', 'listings', "'list'", 'LIST', "'List", 'Listing', "List'", "lists'"],
'function': ['function', 'functions', 'Function', 'functional', 'functionality', 'functioning', 'functionally', 'Functions', 'Functional', "'function", 'FUNCTION', "function'", 'FUNCTIONALLY'],
'method': ['method', 'methods', "method'", 'METHOD', 'Method', 'Methods', "'Method", 'methodically'],
'instal': ['installed', 'install', 'installation', 'installing', 'Installing', 'Install', 'installer', 'installations', 'installers', 'installs', "'Installing", 'Installation', 'Installers', 'INSTALLED', "'install", 'Installed', 'installable', 'Instal', 'instaled', 'instalation', 'Installer'],
'need': ['need', 'needed', 'needs', 'Need', 'Needed', 'needing'],
'one': ['one', 'One', 'ones', "'one", "'One", "'one'", "'ONE", 'ONE'],
'code': ['code', 'coding', 'codes', 'coded', 'Code', "code'", 'Coding', "'code", 'Codes', 'CODE'],
'way': ['way', 'ways', 'Way', 'WAY'],
'object': ['object', 'objects', "object'", 'Object', "'object", 'Objects', 'objected', 'OBJECT', 'objective', "'Object", "object's", "'object'"],
'work': ['working', 'work', 'works', 'WORKED', 'worked', 'Work', 'Works', 'Worked', 'Working', 'WORK', "works'", "work'", "'Works"],
'like': ['like', 'Like', 'likely', 'liked', "'like", 'likes', 'Likely'], 'string': ['string', 'strings', 'String', 'Strings',
'STRING', "'string", "string'", "'string'"],
'file': ['file', 'files', 'File', 'Files', "'file", 'FILE', "'file'", 'filed', "file'", "'File", 'FIle', "FILE'", "'files"],
'want': ['want', 'wanted', 'wants', 'wanting', 'Wanting', 'Want'],
'use': ['use', 'using', 'Using', 'useful', 'used', 'uses', 'Use', 'Useful', 'Uses', "'using", 'usefully', 'USE', 'usefulness', 'Used', "'Using", 'USe', 'USING'],
'you': ['you', "'you", 'You', 'YOU', "'You"],
'exampl': ['example', 'Example', 'examples', 'Examples', 'EXAMPLE', "'example", 'EXAMPLES', "'EXAMPLE'", "Example'"]}


for i in info:
    rowstr=''
    cnt=3
    set(info[i])
    for j in info[i]:
        if '\'' in j:
            j.lstrip('\'')
        rowstr+= (j+", ")
    print(i+" & " +rowstr+"\\\\\\hline")