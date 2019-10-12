from AhoCorasick import *


if __name__ == '__main__':

    # ac = AhoCorasick('keywords.txt') # keywords.txt是一个关键词文件，一行一个，如果有value，用tab分隔
    keywords = {'he':'HE_VALUE','she':'SHE_VALUE','his':'HIS_VALUE','hers':'HERS_VALUE'}
    ac = AhoCorasick(keywords)
    text = 'ushers'
    print ('Default:')
    print (list(ac.process(text)))
    print ()

    print ('Keyword only:')
    print (list(ac.process(text,keyword_only=True)))
    print ()

    print ('Value only:')
    print (list(ac.process(text,value_only=True)))
    print ()

    print ('Check if match:')
    print (ac.match(text))
    print ()
    



