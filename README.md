# AhoCorasick
Python dict Implementation of [AhoCorasick Pattern Matching Machine](https://cr.yp.to/bib/1975/aho.pdf)



```bash
# ac = AhoCorasick('keywords.txt') # keywords.txt是一个关键词文件，一行一个，如果有value，用tab分隔
>> keywords = {'he':'HE_VALUE','she':'SHE_VALUE','his':'HIS_VALUE','hers':'HERS_VALUE'}
>> ac = AhoCorasick(keywords)
>> text = 'ushers'
>> print ('Default:')
>> print (list(ac.process(text)))

>> print ('Keyword only:')
>> print (list(ac.process(text,keyword_only=True)))

>> print ('Value only:')
>> print (list(ac.process(text,value_only=True)))

>> print ('Check if match:')
>> print (ac.match(text))


Outputs:
Default:
[Match(begin=2, end=4, keyword='he', value='HE_VALUE'), Match(begin=1, end=4, keyword='she', value='SHE_VALUE'), Match(begin=2, end=6, keyword='hers', value='HERS_VALUE')]

Keyword only:
['he', 'she', 'hers']

Value only:
['HE_VALUE', 'SHE_VALUE', 'HERS_VALUE']

Check if match:
True

```



