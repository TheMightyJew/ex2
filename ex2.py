import csv
import os
import time

class Heap:
    def __init__(self, file_name):
        """
        :param file_name: the name of the heap file to create. example: kiva_heap.txt
        """
        self.filename=file_name

    def create(self, source_file):
        """
        The function create heap file from source file.
        :param source_file: the name of file to create from. example: kiva.txt
        """
        myfile=open(source_file,"r")
        targetfile=open(self.filename,"w")
        targetfile.write(myfile.read())
        targetfile.close()
        myfile.close()


    def insert(self, line):
        """
        The function insert new line to heap file
        :param line: string reprsent new row, separated by comma. example: '653207,1500.0,USD,Agriculture'
        """
        writefile=open(self.filename, 'a')
        writefile.write('\n'+line)
        writefile.close()

    def delete(self, col_name, value):
        """
        The function delete records from the heap file where their value in col_name is value.
        Deletion done by mark # in the head of line.
        :param col_name: the name of the column. example: 'currency'
        :param value: example: 'PKR'
        """
        writeFile = open('temp.txt','w')
        mycsv=csv.reader(open(self.filename))
        indexCol=0
        counter=0
        newRow = ""
        for word in next(mycsv):
            newRow += word + ','
            if word==col_name:
                indexCol=counter
            else :
                counter+=1
        newRow = newRow[:-1]
        writeFile.write(newRow)
        for row in mycsv:
            newRow = ''
            for word in row:
                newRow += word + ','
            newRow =newRow[:-1]
            if row[indexCol] == value:
                writeFile.write('\n'+'#' + newRow[1:])
            else:
                writeFile.write('\n'+newRow)
        writeFile.close()
        self.create('temp.txt')
        os.remove('temp.txt')
    def update(self, col_name, old_value, new_value, ):
        """
        The function update records from the heap file where their value in col_name is old_value to new_value.
        :param col_name: the name of the column. example: 'currency'
        :param old_value: example: 'TZS'
        :param new_value: example: 'NIS'
        """
        writeFile = open('temp.txt','w')
        mycsv=csv.reader(open(self.filename))
        indexCol=0
        counter=0
        newRow = ""
        for word in next(mycsv):
            newRow += word + ','
            if word==col_name:
                indexCol=counter
            else :
                counter+=1
        newRow = newRow[:-1]
        writeFile.write(newRow)
        for row in mycsv:
            newRow = ''
            counter=0
            for word in row:
                if counter==indexCol and word == old_value:
                    newRow += new_value + ','
                else :
                    newRow += word + ','
                counter+=1
            newRow = '\n'+newRow[:-1]
            writeFile.write(newRow)
        writeFile.close()
        self.create('temp.txt')
        os.remove('temp.txt')
# heap = Heap('heap.txt')
# heap.create('kiva.txt')
# heap.insert('653207,1500.0,USD,Agriculture')
# heap.update('currency','INR','NIS')
# heap.delete('currency','NIS')
# #heap.insert('653208,1500.0,USD,Agriculture')


def ifBigger(a, b):
    if(a.__len__()==0 or b.__len__()==0):
        return (a > b)
    checkA = a[0].isdigit()
    checkB = b[0].isdigit()
    if (checkA and checkB):
       return float(a) > float(b)
    return (a > b)

class SortedFile:

    def __init__(self, file_name, col_name):
        """
        :param file_name: the name of the sorted file to create. example: kiva_sorted.txt
        :param col_name: the name of the column to sort by. example: 'lid'
        """
        self.fileName=file_name
        self.sortBy=col_name

    def create(self, source_file):
        """
        The function create sorted file from source file.
        :param source_file: the name of file to create from. example: kiva.txt
        """
        reader=open(source_file,'r')
        mycsv=csv.reader(reader)
        targetfile=open(self.fileName,"w")
        newRow=''
        indexCol=0
        counter=0
        for word in next(mycsv):
            if word==self.sortBy:
                indexCol=counter
            newRow += word + ','
            counter+=1
        newRow =newRow[:-1]
        targetfile.write(newRow)
        num=0
        for row in mycsv:
            num+=1
        reader.seek(0)
        next(mycsv)
        minValue=next(mycsv)[indexCol]
        i=0
        for row in mycsv:
            if ifBigger(minValue,row[indexCol]):
                minValue=row[indexCol]
        nextMinValue=minValue
        i=0
        while i<num:
            minValue=nextMinValue
            nextMinValue=''
            reader.seek(0)
            next(mycsv)
            for row in mycsv:
                if row[indexCol]==minValue:
                    newRow=''
                    for word in row:
                        newRow += word + ','
                    newRow = newRow[:-1]
                    targetfile.write('\n'+newRow)
                    i+=1
                if ifBigger(row[indexCol],minValue) and (nextMinValue==''or ifBigger(nextMinValue,row[indexCol])):
                    nextMinValue=row[indexCol]
        targetfile.close()
        reader.close()

    def binarySearch(self, value):
        reader=open(self.fileName,'r');
        mycsv=csv.reader(reader)
        indexCol=0
        for word in next(mycsv):
            if word==self.sortBy:
                break
            indexCol+=1
        reader.seek(0)
        firstLength=reader.readline().__len__()+1
        lineLength=reader.readline().__len__()+1
        reader.seek(0)
        start=firstLength
        reader.seek(0,2)
        end=reader.tell()
        while(end-start>=lineLength):
            middle=(end+start)/2
            check=(middle-firstLength)%lineLength
            middle-=check
            reader.seek(middle)
            row=next(mycsv)
            if row[indexCol]==value:
                return middle
            elif ifBigger(row[indexCol],value):
                    end=middle-lineLength
            else:
                start=middle+lineLength
        return -1

    def insert(self, line):
        """
        The function insert new line to sorted file according to the value of col_name.
        :param line: string of row separated by comma. example: '653207,1500.0,USD,Agriculture'
        """
        writeFile = open('temp.txt','w')
        mycsv=csv.reader(open(self.fileName))
        indexCol=0
        counter=0
        newRow = ""
        for word in next(mycsv):
            newRow += word + ','
            if word==self.sortBy:
                indexCol=counter
            else :
                counter+=1
        newRow = newRow[:-1]
        writeFile.write(newRow)
        fields=line.split(',')
        written=False
        for row in mycsv:
            newRow = ''
            if ifBigger(row[indexCol],fields[indexCol]) and written==False:
                writeFile.write('\n'+line)
                written=True
            for word in row:
                newRow += word + ','
            newRow = '\n'+newRow[:-1]
            writeFile.write(newRow)
        if written==False:
            writeFile.write('\n' + line)
            written = True
        writeFile.close()
        myfile=open('temp.txt',"r")
        targetfile=open(self.fileName,"w")
        targetfile.write(myfile.read())
        targetfile.close()
        myfile.close()
        os.remove('temp.txt')

    def delete(self, value):
        """
        The function delete records from sorted file where their value in col_name is value.
        Deletion done by mark # in the head of line.
        :param value: example: 'PKR'
        """
        writeFile = open('temp.txt','w')
        mycsv=csv.reader(open(self.fileName))
        indexCol=0
        counter=0
        newRow = ""
        for word in next(mycsv):
            newRow += word + ','
            if word==self.sortBy:
                indexCol=counter
            else :
                counter+=1
        newRow = newRow[:-1]
        writeFile.write(newRow)
        for row in mycsv:
            newRow = ''
            for word in row:
                newRow += word + ','
            newRow =newRow[:-1]
            if row[indexCol] != value:
                writeFile.write('\n'+newRow)
        writeFile.close()
        self.create('temp.txt')
        os.remove('temp.txt')

    def update(self, old_value, new_value):
        """
        The function update records from the sorted file where their value in col_name is old_value to new_value.
        :param old_value: example: 'TZS'
        :param new_value: example: 'NIS'
        """
        writeFile = open('tempUpdate.txt','w')
        mycsv=csv.reader(open(self.fileName))
        indexCol=0
        counter=0
        newRow = ""
        for word in next(mycsv):
            newRow += word + ','
            if word==self.sortBy:
                indexCol=counter
            else :
                counter+=1
        newRow = newRow[:-1]
        writeFile.write(newRow)
        for row in mycsv:
            newRow = ''
            num = 0
            for word in row:
                if(num==indexCol and word==old_value):
                    newRow += new_value + ','
                else:
                    newRow += word + ','
                num+=1
            newRow = newRow[:-1]
            writeFile.write('\n' + newRow)
        writeFile.close()
        self.create('tempUpdate.txt')
        os.remove('tempUpdate.txt')

# sf = SortedFile('SortedFile.txt', 'loan_amount')
# sf.create('kiva.txt')
# sf.insert('653207,2.0,USD,Agricu')
# sf.binarySearch('2.0')
# # sf.delete('400.0')
# # sf.update('400.0','12.00')

def hashItUp(x,N):
    if(x[0].isdigit()):
        return (int(x)%N+1)
    return (ord(x[0])&N+1)

class Hash:
    def __init__(self, file_name, N=5):
        """
        :param file_name: the name of the hash file to create. example: kiva_hash.txt
        :param N: number of buckets/slots.
        """
        self.file_name=file_name
        self.NOB=N


    def create(self, source_file, col_name):
        """
        :param source_file: name of file to create from. example: kiva.txt
        :param col_name: the name of the column to index by example: 'lid'
        Every row will represent a bucket, every tuple <value|ptr> will separates by comma.
        Example for the first 20 instances in 'kiva.txt' and N=10:
        653060|11,
        653091|17,653051|1,
        653052|18,653062|14,653082|9,
        653063|4,653053|2,
        653054|16,653084|5,
        653075|15,
        653066|19,
        653067|7,
        653088|12,653048|10,653078|8,1080148|6,653068|3,
        653089|13,
        """
        writeFile = open(self.file_name,'w')
        writeTemp = open('tempCreate.txt','w')
        readfile=open(source_file,'r')
        mycsv=csv.reader(readfile)
        indexCol=0
        for word in next(mycsv):
            if word==col_name:
                break
            indexCol+=1
        for j in range (1,self.NOB+1):
            readfile.seek(0)
            next(mycsv)
            rowNum=0
            for row in mycsv:
                if hashItUp(row[indexCol],self.NOB)==j:
                    writeTemp.write(row[indexCol]+'|'+rowNum.__str__()+',')
                rowNum+=1
            writeTemp.write('\n')
        writeTemp.close()
        reader=open('tempCreate.txt','r')
        csvtmp=csv.reader(reader)
        for row in csvtmp:
            list=row
            i=len(list)-2
            while i>=0:
                writeFile.write(list[i]+',')
                i=i-1
            writeFile.write('\n')
        reader.close()

        os.remove('tempCreate.txt')
        writeFile.close()
        readfile.close()



    def add(self, value, ptr):
        """
        The function insert <value|ptr> to hash table according to the result of the hash function on value.
        :param value: the value of col_name of the new instance.
        :param ptr: the row number of the new instance in the heap file.
        """
        writeTemp = open('tempCreate.txt','w')
        reader=open(self.file_name,"r")
        mycsv=csv.reader(reader)
        rowNum=hashItUp(value,self.NOB)
        counter=1
        for row in mycsv:
            if counter==rowNum:
                writeTemp.write(value+'|'+ptr+',')
            for word in row:
                writeTemp.write(word+',')
            writeTemp.write('\n')
            counter+=1
        writeTemp.close()
        reader.close()
        writeTemp = open('tempCreate.txt','r')
        reader=open(self.file_name,"w")
        reader.write(writeTemp.read())
        writeTemp.close()
        os.remove('tempCreate.txt')
        reader.close()


    def remove(self, value, ptr):
        """
        The function delete <value|ptr> from hash table.
        :param value: the value of col_name.
        :param ptr: the row number of the instance in the heap file.
        """
        writeTemp = open('tempCreate.txt','w')
        reader=open(self.file_name,"r")
        mycsv=csv.reader(reader)
        for row in mycsv:
            for word in row:
                list=word.split('|')
                if value!=list[0] or ptr!=list[1]:
                    writeTemp.write(word+',')
            writeTemp.write('\n')
        writeTemp.close()
        reader.close()
        writeTemp = open('tempCreate.txt','r')
        reader=open(self.file_name,"w")
        reader.write(writeTemp.read())
        writeTemp.close()
        reader.close()
        os.remove('tempCreate.txt')


# heap = Heap("heap_for_hash.txt")
# heap.create('kiva.txt')
# hash = Hash('hash_file.txt', 1000)
# hash.create('kiva.txt', 'lid')
# heap.insert('653207,1500.0,USD,Agriculture')
# # hash.add('653207','11')
# # heap.delete('lid','653207')
# hash.remove('653207','11')

