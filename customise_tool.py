"""This modul customise tool to blocks
"""

class Customise_tool:
    def __init__(self, My_block, title, instrument):
        self.My_block = My_block
        self.title = title
        self.instrument = instrument
        
    # This function set number of instrument for block
    def set_tool(self):
        instr = ''
        if self.title == 'Ren_150' or self.title == 'Ren_200':
            instr = '60'
        else:
            i = 0
            numbers = '0123456789'
            while i < len(self.My_block):
                if self.My_block[i][0] != '(' and len(self.My_block[i]) > 4 and 'M6T' in self.My_block[i]:
                    stroka = self.My_block[i].partition('M6T')[2]
                    j = 0
                    while j < len(stroka):
                        if stroka[j] in numbers:
                            instr = instr + stroka[j]
                        else:
                            j = len(stroka)
                        j += 1
                    i = len(self.My_block)
                i += 1
        if instr == '':
            instr = '58'
        return instr
