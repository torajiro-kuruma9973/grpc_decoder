from bitarray import bitarray
import sys
#raw = '\x9a\xca\xc8\xb5\x25\x42\x07\x31\x7f'
# remove "\x"
#s = ''.join(f'{ord(c):02x}' for c in raw)
# To avoid to delete the leading zeros
s = sys.argv[1]
fill = len(s) * 4
b = bin(int(s, 16))[2:].zfill(fill)
#print(b)

#print(type(b))
# initialization
ba = bitarray('010100')
dic = {' ': ba}
ba = bitarray('11111111010')
#dic['\''] = ba
#ba = bitarray('1111111010')
dic['('] = ba
ba = bitarray('1111111011')
dic[')'] = ba
ba = bitarray('11111111100')
dic['|'] = ba
# start to read source dictionary
f = open("hfm.txt", "r")

while(1):

    s = f.readline()
    if not s:
        break;
    s = s.replace('(', '').replace(')', '').replace('\'', '').replace('|', '').split()
    #print(s)
    dic[s[0]] = bitarray(s[2])

#print(dic)
while(1):
    dec = bitarray(b).decode(dic)
    try:
        print(''.join(dec))
    except:
        b = b[:-1]
        continue
    break
print(''.join(dec))
