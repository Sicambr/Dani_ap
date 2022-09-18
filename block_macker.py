"""This modul make classes from file
"""


# Delete empty spaces after number of block
def kill_emptySpaces(My_blocks):
    i = 1
    empty_string = (' ', '\n')
    marker = 0
    while marker == 0:
        if len(My_blocks[i]) == 0:
            My_blocks.pop(i)
        elif len(My_blocks[i]) >= 1 and My_blocks[i][0] in empty_string:
            My_blocks.pop(i)
        else:
            marker = 1
    return My_blocks


# Renum mistakes if we deleted empty spaces
def rename_mistakes(mis,cor):
    numbers = '0123456789'
    i = mis['total']
    while i > 0:
        stroka = mis[i]
        stroka2 = ''
        j = len(stroka) - 1 
        num_mistake = ''
        while j >= 0:
            if stroka[j] in numbers:
                num_mistake = num_mistake + stroka[j]
                j -= 1
            else:
                stroka2 = stroka[:j+1]
                j = -1
        #reverse string
        num_mistake = num_mistake[::-1]
        newnum_mis = int(num_mistake) - cor
        stroka = stroka2 + str(newnum_mis)
        mis[i] = stroka
        i -= 1
    return mis


# Identify title of single block
def initialization_block(MyOld_file):
    i = 0
    old_ras = ['G2I','G2J','G3I','G3J']
    cicl_loop = ['G65P43','G66P44','G65P47','G65P62','G65P63','G65P64','G65P70','G65P71','G65P80']
    title = 'title'
    while i < len(MyOld_file):
        if (len(MyOld_file[i]) > 2 and MyOld_file[i][:2] == 'M6'):
            title = 'milling'
        elif (len(MyOld_file[i]) >= 7 and MyOld_file[i][:7] == 'G65P200'):
            title = 'Ren_200'
            break
        elif (len(MyOld_file[i]) >= 7 and MyOld_file[i][:7] == 'G65P150'):
            title = 'Ren_150'
            break
        elif (len(MyOld_file[i]) > 2 and MyOld_file[i][0] != '(' and 'G81' in MyOld_file[i]):
            title = 'Drill'
            break
        elif (len(MyOld_file[i]) > 2 and MyOld_file[i][0] != '(' and 'G83' in MyOld_file[i]):
            title = 'Drill'
            break
        elif (len(MyOld_file[i]) > 6 and MyOld_file[i][:6] in cicl_loop):
            title = 'Loop'
            break
        elif (len(MyOld_file[i]) > 2 and MyOld_file[i][:2] == 'IF'):
            title = 'milling_GOTO'
            break
        elif (len(MyOld_file[i]) > 3 and MyOld_file[i][:3] in old_ras):
            title = 'old_boring'
            break
        i += 1
    return title


# Replace head from previous block
def replace_head(My_blocks,block,i):
    empty_newblock = []
    empty_newblock.append('N10\n')
    empty_newblock.append('(**********   NEW BLOCK   *********)\n')
    names_titels = ['Ren_200','Ren_150','title']
    marker = 0
    i = i - 1
    while i > 0:
        if block[i].title in names_titels:
            i -= 1
        else:
            j = 0
            while j < len(My_blocks[i]):
                if len(My_blocks[i][j]) > 2 and My_blocks[i][j][:2] == 'M6':
                    empty_newblock.append(My_blocks[i][j-1])
                    marker = 1
                if marker == 1:
                    empty_newblock.append(My_blocks[i][j])
                if len(My_blocks[i][j]) > 4 and My_blocks[i][j][:4] == 'G201':
                    marker = 2
                if marker == 2:
                    break
                j += 1
            break
    if len(empty_newblock) == 2:
        empty_newblock.append('(FR.6 L=30)\n')
        empty_newblock.append('M6T13H0B0\n')
        empty_newblock.append('M3S15000\n')
        empty_newblock.append('G0C0\n')
        empty_newblock.append('G211\n')
        empty_newblock.append('G0X60Y0Z100B90\n')
        empty_newblock.append('G49\n')
        empty_newblock.append('G304X#510Y#511Z#512C0.0\n')
        empty_newblock.append('G201X0Y0Z0B90.0\n')
    empty_newblock.append('G1X-30Y0Z60F2000\n')
    empty_newblock.append('M8M138\n')
    empty_newblock.append('Z50F1000\n')
    empty_newblock.append('\n')
    empty_newblock.append('\n')
    empty_newblock.append('M9\n')
    empty_newblock.append('G69\n')
    empty_newblock.append('G49\n')
    empty_newblock.append('M5\n')
    empty_newblock.append('M53\n')
    empty_newblock.append('M00\n')
    empty_newblock.append('\n')
    empty_newblock.append('\n')
    return empty_newblock


# Create a new block with boring
def create_boring(My_blocks,block,i,amount_ins,My_tool):
    need_findD = My_tool[int(block[i].tool)-1].DValue
    correct_tnum = {'ins':'T1','stroka':'(NET NUGNOGO INSTRUMENTA V KATALOGE)\n'}
    empty_newblock = []
    empty_newblock.append('N10\n')
    empty_newblock.append('(******  NEW RASTOCHKA D' + str(need_findD) +'  *****)'+'\n')
    my_newtext = []
    j = 2
    while j < len(My_blocks[i]):
        empty_newblock.append(My_blocks[i][j])
        if len(My_blocks[i][j]) > 4 and My_blocks[i][j][:4] == 'G201':
            j += 1
            break
        j += 1
    while j < len(My_blocks[i]):
        if (len(My_blocks[i][j]) > 3 and My_blocks[i][j][:3] == 'G83') or\
                (len(My_blocks[i][j]) > 3 and My_blocks[i][j][:3] == 'G81'):
            my_newtext.clear()
            correct_tnum = correct_t(My_blocks[i][j],My_tool,need_findD,correct_tnum,amount_ins)
            my_newtext = read_G83(j,My_blocks[i],str(need_findD))
            empty_newblock.extend(my_newtext)
            j = j + len(my_newtext)
        else:
            empty_newblock.append(My_blocks[i][j])
        j += 1
    i = 0
    while i < len(empty_newblock):
        if len(empty_newblock[i]) > 3 and empty_newblock[i][:3] == 'M6T':
            stroka =  'M6' + correct_tnum['ins'] + empty_newblock[i].partition('T')[2].lstrip('0123456789')
            empty_newblock[i] = stroka
            empty_newblock[i-1] = correct_tnum['stroka']
            break
        i += 1
    empty_newblock = short_loopCreater(empty_newblock)
    return empty_newblock


# Function try to find  correct T number
def correct_t(text,My_tool,need_findD,correct_tnum,amount_ins):
    G_param = {'X': '999', 'Y': '999', 'Z': '999', 'R': '999', 'Q': '0.05', 'F': '500', 'D': need_findD}
    G_param = read_paramtext(G_param, text.rstrip('\n'))
    need_findL = float(G_param['R']) - float(G_param['Z'])
    mas_frez = []
    # Search all MILLS
    for i in range(amount_ins):
        if str(My_tool[i].ToolNameType) == 'Концевая фреза' and My_tool[i].DValue < float(need_findD):
            mas_frez.append(i+1)
    # Sort Mills by DIAMETR
    if len(mas_frez) > 0:
        j = 0
        while j < len(mas_frez)-1:
            k = j + 1
            while k < len(mas_frez):
                if My_tool[mas_frez[k]-1].DValue > My_tool[mas_frez[j]-1].DValue:
                    prom = mas_frez[j]
                    mas_frez[j] = mas_frez[k]
                    mas_frez[k] = prom
                k += 1
            j += 1
    # Chose mill with normal lenght
    if len(mas_frez) > 0:
        correct_tnum['ins'] = 'T'+str(mas_frez[0])
        correct_tnum['stroka'] = instrument_name(My_tool,mas_frez[0])
        new_mas = []
        for j in mas_frez:
            if float(My_tool[j-1].LValue) >= need_findL:
                correct_tnum['ins'] = 'T' + str(j)
                correct_tnum['stroka'] = instrument_name(My_tool, j-1)
                new_mas.append(j)
        little_l = 99.0
        little_D = 99.0
        if len(new_mas) > 0:
            little_D = float(My_tool[new_mas[0]-1].DValue)
            correct_tnum['ins'] = 'T' + str(new_mas[0]-1)
            correct_tnum['stroka'] = instrument_name(My_tool, new_mas[0]-1)
        mark = 0
        for i in new_mas:
            if float(My_tool[i - 1].DValue) == little_D and float(My_tool[i - 1].LValue) < little_l:
                little_l = float(My_tool[i - 1].LValue)
                correct_tnum['ins'] = 'T' + str(i)
                correct_tnum['stroka'] = instrument_name(My_tool, i-1)
                mark = 1
            elif float(My_tool[i - 1].DValue) != little_D:
                if mark == 0:
                    correct_tnum['ins'] = 'T' + str(i)
                    correct_tnum['stroka'] = instrument_name(My_tool, i-1)
                    little_l = 99.0
                    little_D = float(My_tool[i - 1].DValue)
                else:
                    break
    return correct_tnum


# Create string with istrument name
def instrument_name(My_tool, number):
    stroka = '(FR.-' + str(My_tool[number].DValue) + '  L' + str(My_tool[number].LValue) + ')\n'
    return stroka


# Read G83 parametrs from drilling
def read_G83(i, original_t,diametr):
    G83_param = {'X':'999', 'Y':'999', 'Z':'999', 'R':'999', 'Q':'0.05', 'F':'500', 'D':diametr}
    end_mark = ['G80','G69','G49','M53','M00']
    my_new_loop = []
    while i < len(original_t):
        if len(original_t[i]) > 2 and original_t[i][:3] in end_mark:
            break
        else:
            G83_param = read_paramtext(G83_param, original_t[i].rstrip('\n'))
            my_new_loop.append(boring_stile(G83_param))
        i += 1
    return my_new_loop


# Function return new sting like P43
def boring_stile(my_param):
    Verh = str(int(float(my_param['R'])) + 20)
    stroka = 'G65P43' + 'X' + my_param['X'] + 'Y' + my_param['Y'] + 'V' + Verh + 'Z' + my_param['R']
    stroka = stroka + 'W' + my_param['Z'] + 'Q' + my_param['Q'] + 'F' + my_param['F'] + 'D' + my_param['D'] + '\n'
    return stroka


# Fuction reads parametrs from string and return them
def read_paramtext(my_param, text):
    letters = 'XYZRQF'
    numbers = '-.0123456789'
    stroka_p = ''
    i = 0
    while i < len(text):
        if text[i] in letters:
            stroka_p = text[i]
            j = i + 1
            while j < len(text):
                if text[j] in numbers:
                    stroka_p = stroka_p + text[j]
                else:
                    i = j - 1
                    break
                j += 1
            my_param[stroka_p[0]] = stroka_p[1:]
        i += 1
    return my_param


# Fuction create short form text
def short_loopCreater(main_text):
    i = 0
    save_arg = {'tip':'none'}
    full_arguments = {}
    short_arguments = {}
    while i < len(main_text):
        if len(main_text[i]) > 6 and main_text[i][:6] == 'G65P43':
            if save_arg['tip'] != 'P43':
                save_arg.clear()
                save_arg = {'tip':'P43','X':'999','Y':'999','V':'999','Z':'999','W':'999','D':'999','Q':'0.05','F':'500'}
                full_arguments = save_arg.copy()
                del full_arguments['tip']
                short_arguments = read_stringArg(full_arguments,main_text[i].rstrip('\n'))
                for j in full_arguments.keys():
                    full_arguments[j] = short_arguments[j]
            else:
                short_arguments = read_stringArg(full_arguments, main_text[i].rstrip('\n'))
                for j in full_arguments.keys():
                    if j in short_arguments.keys() and full_arguments[j] == short_arguments[j]:
                        del short_arguments[j]
                    elif j in short_arguments.keys() and full_arguments[j] != short_arguments[j]:
                        full_arguments[j] = short_arguments[j]
            main_text[i] = full_sting_par(short_arguments)
        else:
            save_arg['tip'] = 'none'
        i += 1
    return main_text


# Fuction create full form text
def full_loopCreater(main_text):
    i = 0
    save_arg = {'tip':'none'}
    full_arguments = {}
    short_arguments = {}
    while i < len(main_text):
        if len(main_text[i]) > 6 and main_text[i][:6] == 'G65P43':
            if save_arg['tip'] != 'P43':
                save_arg.clear()
                save_arg = {'tip':'P43','X':'999','Y':'999','V':'999','Z':'999','W':'999','D':'999','Q':'0.05','F':'500'}
                full_arguments = save_arg.copy()
                del full_arguments['tip']
                short_arguments = read_stringArg(full_arguments,main_text[i].rstrip('\n'))
                for j in full_arguments.keys():
                    if j in short_arguments.keys():
                        full_arguments[j] = short_arguments[j]
            else:
                short_arguments = read_stringArg(full_arguments, main_text[i].rstrip('\n'))
                for j in full_arguments.keys():
                    if j in short_arguments.keys():
                        full_arguments[j] = short_arguments[j]
            main_text[i] = full_sting_par(full_arguments)
        else:
            save_arg['tip'] = 'none'
        i += 1
    return main_text


# read arguments from sting
def read_stringArg(old_arg,text):
    arguments = {}
    numbers = '-0.123456789'
    letters = old_arg.keys()
    i = 0
    stroka = ''
    while i < len(text):
        if text[i] in letters:
            j = i + 1
            stroka = ''
            while j < len(text):
                if text[j] in numbers:
                    stroka = stroka + text[j]
                    if j == len(text)-1:
                        arguments[text[i]] = stroka
                else:
                    arguments[text[i]] = stroka
                    i = j - 1
                    break
                j += 1
        i += 1
    return arguments


# Create full string with new parametrs
def full_sting_par(short_arguments):
    stroka = 'G65P43'
    for i in short_arguments.keys():
        stroka = stroka + i + short_arguments[i]
    stroka = stroka + '\n'
    return stroka


class Block_macker:
    def __init__(self,MyOld_file):
        self.MyOld_file = MyOld_file
        self.body_b = []
        self.title = ''
        self.first_n = 0
        self.last_n = 0
        self.feed = []
        self.time_cutting = 0
        self.loop_arg = {}
        self.mistakes = {}
        self.warning_m = {}
        self.tool = ''
        self.milling_mode = ''
        self.loops_names = ''


    # First defenision for title
    def title_block(self):
        i = 0
        self.title = 'title'
        while i < len(self.MyOld_file):
            self.MyOld_file[i] = self.MyOld_file[i].rstrip('\n').rstrip()
            if (len(self.MyOld_file[i]) > 4 and self.MyOld_file[i][:4] == 'GOTO'):
                self.body_b.append(self.MyOld_file[i] + '\n')
                i = len(self.MyOld_file)
            elif (len(self.MyOld_file[i]) > 1 and self.MyOld_file[i][:1] == 'N'):
                i = len(self.MyOld_file)
            else:
                self.body_b.append(self.MyOld_file[i] + '\n')
            i += 1
        return self.body_b


    # First defenision for title
    def common_block(self):
        i = 0
        marker = 0
        old_ras = ['G2I','G2J','G3I','G3J']
        cicl_loop = ['G65P43','G66P44','G65P47','G65P62','G65P63','G65P64','G65P70','G65P71','G65P80']
        self.title = 'none'        
        while i < len(self.MyOld_file):
            self.MyOld_file[i] = self.MyOld_file[i].rstrip('\n').rstrip()
            if (len(self.MyOld_file[i]) > 2 and self.MyOld_file[i][:2] == 'M6'):
                marker += 1
                if marker < 2 :
                    self.title = 'milling'
            elif (len(self.MyOld_file[i]) >= 7 and self.MyOld_file[i][:7] == 'G65P200'):
                marker += 1
                if marker < 2 :
                    self.title = 'Ren_200'
            elif (len(self.MyOld_file[i]) >= 7 and self.MyOld_file[i][:7] == 'G65P150'):
                if marker < 1 :
                    i = self.Case_withREN150(i)
                marker += 1
                if marker < 2 :
                    self.title = 'Ren_150'
            elif (len(self.MyOld_file[i]) > 2 and self.MyOld_file[i][0] != '(' and 'G81' in self.MyOld_file[i]):
                if marker < 2 :
                    self.title = 'Drill'
            elif (len(self.MyOld_file[i]) > 2 and self.MyOld_file[i][0] != '(' and 'G83' in self.MyOld_file[i]):
                if marker < 2 :
                    self.title = 'Drill'
            elif (len(self.MyOld_file[i]) > 6 and self.MyOld_file[i][:6] in cicl_loop):
                if marker < 2 :
                    self.title = 'Loop'
            elif (len(self.MyOld_file[i]) > 2 and self.MyOld_file[i][:2] == 'IF'):
                if marker < 2 :
                    self.title = 'milling_GOTO'
            elif (len(self.MyOld_file[i]) > 3 and self.MyOld_file[i][:3] in old_ras):
                if marker < 2 :
                    self.title = 'old_boring'
            self.body_b.append(self.MyOld_file[i] + '\n')
            if marker == 2:
                self.body_b.pop()
                j = i - 1
                while j > 0:
                    if (len(self.MyOld_file[j]) >= 1 and self.MyOld_file[j][:1] == 'N'):
                        self.body_b.pop()
                        j = 0
                    elif (len(self.MyOld_file[j]) >= 2 and self.MyOld_file[j][:2] == 'M0'):
                        j = 0
                    elif (len(self.MyOld_file[j]) >= 3 and self.MyOld_file[j][:3] == 'M53'):
                        j = 0
                    elif (len(self.MyOld_file[j]) >= 7 and self.MyOld_file[j][:7] == 'G65P159'):
                        j = 0
                    elif (len(self.MyOld_file[j]) >= 7 and self.MyOld_file[j][:7] == 'G65P151'):
                        j = 0
                    else:
                        self.body_b.pop()
                    j -= 1
                i = len(self.MyOld_file)
            i += 1
        return self.body_b


    # case with REN150
    def Case_withREN150(self, i):
        j = i
        while i < len(self.MyOld_file):
            self.MyOld_file[i] = self.MyOld_file[i].rstrip('\n').rstrip()
            if (len(self.MyOld_file[i]) >= 7 and self.MyOld_file[i][:7] == 'G65P151'):
                self.body_b.append(self.MyOld_file[i] + '\n')
                i += 1
            elif (len(self.MyOld_file[i]) >= 7 and self.MyOld_file[i][:7] == 'G65P150'):
                self.body_b.append(self.MyOld_file[i] + '\n')
                i += 1
            elif (len(self.MyOld_file[i]) >= 7 and self.MyOld_file[i][:7] == 'G65P159'):
                j = i - 1
                i = len(self.MyOld_file)
            elif (len(self.MyOld_file[i]) >= 2 and self.MyOld_file[i][:2] == 'M0'):
                j = i - 1
                i = len(self.MyOld_file)
            elif (len(self.MyOld_file[i]) >= 1 and self.MyOld_file[i][:1] == 'N'):
                j = i - 1
                i = len(self.MyOld_file)
            else:
                self.body_b.append(self.MyOld_file[i] + '\n')
                i += 1
        self.body_b.pop()
        return j
