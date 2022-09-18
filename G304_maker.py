"""This modul replace G201 function with G304
"""


class Offset_maker:
    def __init__(self,Myblock,title):
        self.Myblock = Myblock
        self.mistakes = {'total': 0}
        self.title = title
        
    # Replace G201 with I J K to G304
    def g304_offset(self):
        i = 0
        C = 0
        B = 0
        X = 0
        Y = 0
        Z = 0
        marker = 0
        arg = []
        while i < len(self.Myblock):
            if self.Myblock[i][0] != '(' and 'C' in self.Myblock[i]:
                arg = self.arg_read(self.Myblock[i])
                for j in arg:
                    if 'C' in j:
                        C = float(j[1:])
            elif 'G201' in self.Myblock[i]:
                marker = 1
                arg = self.arg_read(self.Myblock[i])
                for j in arg:
                    if 'X' in j:
                        X = float(j[1:])
                    if 'Y' in j:
                        Y = float(j[1:])
                    if 'Z' in j:
                        Z = float(j[1:])
                    if 'B' in j:
                        B = float(j[1:])
                stroka = 'G201' + 'X' + str(int(X)) + 'Y' + str(int(Y)) + 'Z' + str(int(Z)) + 'B' + str(B) + '\n'
                del self.Myblock[i]
                self.Myblock.insert(i,stroka)
                stroka = 'G304X#510Y#511Z#512C' + str(C) + '\n'
                if 'G304' in self.Myblock[i-1]:
                    del self.Myblock[i-1]
                    self.Myblock.insert(i-1,stroka)
                else:
                    self.Myblock.insert(i,stroka)
            if i == (len(self.Myblock) - 1) and marker == 0 and self.title != 'Ren_200' and self.title != 'Ren_150':
                self.mistakes['total'] = self.mistakes['total'] + 1
                mis = self.mistakes['total']
                self.mistakes[mis] = 'Нет функции G201 после функции G304*10'
            i += 1
        return self.Myblock

    # Replace parametrs in title
    def g304_title(self):
        i = 0
        while i < len(self.Myblock):
            if self.Myblock[i][0] == '#':
                del self.Myblock[i]
                i -= 1
            i += 1
        i = 0
        while i < len(self.Myblock):
            if len(self.Myblock[i]) > 2 and self.Myblock[i][:2] == '(#':
                del self.Myblock[i]
                i -= 1
            i += 1
        i = 0
        while i < len(self.Myblock):
            if (len(self.Myblock[i]) > 4 and (self.Myblock[i][:4] == 'M148'
                or self.Myblock[i][:3] == 'M53' or self.Myblock[i][:4] == 'GOTO')):
                if self.Myblock[i-1] == '\n':
                    self.Myblock.insert((i-1),'(#512 SMESHENIE PO Z)\n')
                    self.Myblock.insert((i-1),'(#511 SMESHENIE PO Y)\n')
                    self.Myblock.insert((i-1),'(#510 SMESHENIE PO X)\n')
                    i = len(self.Myblock)
                else:
                    self.Myblock.insert(i,'\n')                    
                    self.Myblock.insert(i,'(#512 SMESHENIE PO Z)\n')
                    self.Myblock.insert(i,'(#511 SMESHENIE PO Y)\n')
                    self.Myblock.insert(i,'(#510 SMESHENIE PO X)\n')
                    i = len(self.Myblock)
            i += 1
        return self.Myblock


    # Read arguments from line
    def arg_read(self, stroka):
        arguments = []
        i = 0
        numbers = '#-.0123456789'
        arg = ''
        while i < len(stroka):
            if stroka[i] == '(':
                arguments.append(arg)
                i = len(stroka)
            elif stroka[i] not in numbers:
                arguments.append(arg)
                arg = stroka[i]
            else:
                arg = arg+stroka[i]
            i += 1
        if len(arguments) > 0:
            arguments.pop(0)
        return arguments
