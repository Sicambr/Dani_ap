"""This modul make classes from file
"""

class Block_mist:
    def __init__(self, MyOld_file, title, first_n = 0):
        self.MyOld_file = MyOld_file
        self.title = title
        self.first_n = first_n
        self.last_n = 0
        

    # First renum
    def first_renum(self):
        stroka = ''
        #For old milling with GOTO
        if self.title == 'milling_GOTO':
            i = 0
            while i < len(self.MyOld_file):
                if (len(self.MyOld_file[i]) > 1 and self.MyOld_file[i][:1] == 'N'):
                    self.MyOld_file.pop(i)
                    i -= 1
                elif (len(self.MyOld_file[i]) > 2 and self.MyOld_file[i][:2] == 'M6'):
                    i = len(self.MyOld_file)
                i += 1
            stroka = 'N' + str(self.first_n) + '\n'
            self.last_n = self.first_n
            self.MyOld_file.insert(0,stroka)
            i = 1
            while i < len(self.MyOld_file):
                if (len(self.MyOld_file[i]) > 1 and self.MyOld_file[i][:1] == 'N'):
                    self.last_n += 1
                    stroka = 'N' + str(self.last_n) + '\n'
                    self.MyOld_file.pop(i)
                    self.MyOld_file.insert(i,stroka)
                elif (len(self.MyOld_file[i]) > 15 and self.MyOld_file[i][:15] == 'IF[#106GT0]GOTO'):
                    stroka = 'IF[#106GT0]GOTO' + str(self.last_n) + '\n'
                    self.MyOld_file.pop(i)
                    self.MyOld_file.insert(i,stroka)
                i += 1
        #For Renishow P150 P200
        elif self.title == 'Ren_150' or self.title == 'Ren_200':
            i = 0
            while i < len(self.MyOld_file):
                if (len(self.MyOld_file[i]) > 1 and self.MyOld_file[i][:1] == 'N'):
                    self.MyOld_file.pop(i)
                    i -= 1
                elif (len(self.MyOld_file[i]) > 3 and self.MyOld_file[i][:3] == 'G65'):
                    i = len(self.MyOld_file)
                i += 1
            stroka = 'N' + str(self.first_n) + '\n'
            self.last_n = self.first_n
            self.MyOld_file.insert(0,stroka)
        else:
            i = 0
            while i < len(self.MyOld_file):
                if (len(self.MyOld_file[i]) > 1 and self.MyOld_file[i][:1] == 'N'):
                    self.MyOld_file.pop(i)
                    i -= 1
                elif (len(self.MyOld_file[i]) > 2 and self.MyOld_file[i][:2] == 'M6'):
                    i = len(self.MyOld_file)
                i += 1
            stroka = 'N' + str(self.first_n) + '\n'
            self.last_n = self.first_n
            self.MyOld_file.insert(0,stroka)           
        # Put M00 to the end of block
        j = len(self.MyOld_file) - 1
        marker = 0
        stroka = 'M00\n'
        while j > 0:
            if (len(self.MyOld_file[j]) > 2 and self.MyOld_file[j][:2] == 'M0'):
                j = 0
                marker = 1
            elif (len(self.MyOld_file[j]) > 1 and self.MyOld_file[j][:1] == '%'):
                j = 0
                marker = 1
            elif (len(self.MyOld_file[j]) > 1 and self.MyOld_file[j][:1] == '('):
                j -= 1
            elif (len(self.MyOld_file[j]) > 0 and self.MyOld_file[j][:1] == '\n'):
                j -= 1
            else:
                if marker == 0:
                    self.MyOld_file.insert(j+1,stroka)        
                j = 0
        return self.MyOld_file


    # Replace wrong parenthesis
    def rep_parenthesis(self):
        i = 0
        numbers = '0123456789 '
        while i < len(self.MyOld_file):
            num_N = ''
            if '(' in self.MyOld_file[i] or ')' in self.MyOld_file[i]:
                if self.MyOld_file[i].count('(') > 1 or self.MyOld_file[i].count(')') > 1:
                    self.MyOld_file[i] = self.MyOld_file[i].replace('(' , '')
                    self.MyOld_file[i] = self.MyOld_file[i].replace(')' , '')
                    self.MyOld_file[i] = self.MyOld_file[i].rstrip('\n')
                    self.MyOld_file[i] = '(' + self.MyOld_file[i] + ')\n'
                if self.MyOld_file[i].count('(') != self.MyOld_file[i].count(')'):
                    self.MyOld_file[i] = self.MyOld_file[i].replace('(' , '')
                    self.MyOld_file[i] = self.MyOld_file[i].replace(')' , '')
                    self.MyOld_file[i] = self.MyOld_file[i].rstrip('\n')
                    self.MyOld_file[i] = '(' + self.MyOld_file[i] + ')\n'
                if len(self.MyOld_file[i]) > 2 and self.MyOld_file[i][:2] == '(N':
                    j = 2
                    num_N = 'N'
                    while j < len(self.MyOld_file[i]):
                        if self.MyOld_file[i][j] in numbers:
                            num_N = num_N + self.MyOld_file[i][j]
                        else:
                            j = len(self.MyOld_file[i])
                        j += 1
                    if num_N != 'N':
                        self.MyOld_file[i] = self.MyOld_file[i].replace(num_N , '')
                if len(self.MyOld_file[i]) > 3 and self.MyOld_file[i][:3] == '( N':
                    j = 3
                    num_N = 'N'
                    while j < len(self.MyOld_file[i]):
                        if self.MyOld_file[i][j] in numbers:
                            num_N = num_N + self.MyOld_file[i][j]
                        else:
                            j = len(self.MyOld_file[i])
                        j += 1
                    if num_N != 'N':
                        self.MyOld_file[i] = self.MyOld_file[i].replace(num_N , '')
            i += 1
        return self.MyOld_file


# New renumeration after we added new lock
def new_renum(My_blocks, block):
    number = 0
    stroka = 'N'
    i = 0
    while i < len(My_blocks):
        if block[i].title != 'title':
            number += 10
            if block[i].title == 'milling_GOTO':
                My_blocks[i][0] = 'N' + str(number) + '\n'
                j = 1
                while j < len(My_blocks[i]):
                    if len(My_blocks[i][j]) > 0 and My_blocks[i][j][0] == 'N':
                        number = number + 1
                        My_blocks[i][j] = 'N' + str(number) + '\n'
                    if len(My_blocks[i][j]) > 2 and My_blocks[i][j][:2] == 'IF':
                        My_blocks[i][j] = 'IF[#106GT0]GOTO' + str(number) + '\n'
                    j += 1
                number = number - number % 10
            else:
                My_blocks[i][0] = 'N' + str(number) + '\n'
        i += 1
    return My_blocks
