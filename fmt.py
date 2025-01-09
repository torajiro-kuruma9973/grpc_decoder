inputFile = open('data.py', 'r') 
exportFile = open('data2.py', 'w')
for line in inputFile:
   new_line = line.replace('\t', ' ')
   exportFile.write(new_line) 

inputFile.close()
exportFile.close()
