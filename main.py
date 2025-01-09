import http2 as ht2

f = open("./rst.txt", "r")
line = f.readline()
n = 0
h = ht2.http_frame()
flag = ''
while(line):
    
    if '>>>' in line:
        n = n + 1
        print("#########  " + str(n) + "  ##############")
        print(line)
        if 'process ctr' in line:
            flag = 'c'
        else:
            flag = 's'
    else:
        line = line.replace('\\x', '').rstrip()
        if '505249202a20485454502f322e300d0a0d0a534d0d0a0d0a' in line:
            print('magic word')
        else:
            #s = [line[i:i + 2] for i in range(0, len(line), 2)]
            h.process(line, flag)
            flag = ''
    line = f.readline()
