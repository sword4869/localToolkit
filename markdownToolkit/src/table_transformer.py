# output file content
from msilib import sequence


content = []
with open('source.txt', 'r', encoding='utf-8') as fp:
    for index, line in enumerate(fp):
        # |-|-|
        if index == 1:
            Onelines = line.split(r'	')
            sequence = '|' * (len(lines) + 1)
            Oneline = '-'.join(sequence)
            content.append(Oneline)
        
        # black line still it is
        if len(line) == 1 and line=='\n':
            content.append(line)
            continue

            
        else:
            line = '|' + line[:-1] + '|'
            ##### Please check the char is TAB or space  ######
            lines = line.split(r'	')
            line = '|'.join(lines) 
            content.append(line)

with open('destination.txt', 'w', encoding='utf-8') as fp:
    fp.writelines([i+'\n' for i in content])