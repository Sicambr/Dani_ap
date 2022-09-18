"""This modul add ways for tool store and files
"""

import os
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

def Customise_ToolWay():
    way_tools = ''
    name_of_file = 'Config_d.txt'
    f_home = list(os.listdir())
    # Read all stings from file
    if 'Config_d.txt' not in f_home:
        print('Программа не запускается!\n Не найден файл Config_d.txt с настройками системы в главной папке программы!\n')
        a = input('Нажмите любую клавишу...')
    else:
        Myconfig = []
        for line in open(name_of_file):Myconfig.append(line)
        way_tools = Myconfig[1].rstrip('\n')
        if os.path.isdir(determinate_new_way(way_tools)) == True:
            way_fil = list(os.listdir(determinate_new_way(way_tools)))
            for i in way_fil:
                if '.json' not in i:
                    way_tools = 'Неправильный путь для .json файла'
        else:
            way_tools = 'Неправильный путь для .json файла'
    return way_tools

def Directory_files():
    way = ''
    name_of_file = 'Config_d.txt'
    Myconfig = []
    for line in open(name_of_file):Myconfig.append(line)
    way = Myconfig[3].rstrip('\n')
    if os.path.isdir(way) == False:
        way = 'Несуществующий каталог'
    return way

def determinate_new_name(Full_way):
    i = len(Full_way)
    new_file_name = ''
    while i > 0:
        if Full_way[i-1] != '/':
            new_file_name = new_file_name + Full_way[i-1]
        else:
            break
        i -= 1
    stroka = ''
    i = len(new_file_name)
    while i > 0:
        stroka = stroka + new_file_name[i-1]
        i -= 1
    return stroka

def determinate_new_way(Full_way):
    i = len(Full_way)
    new_file_name = ''
    while i > 0:
        if Full_way[i-1] != '/':
            new_file_name = new_file_name + Full_way[i-1]
        else:
            break
        i -= 1
    i = len(new_file_name)
    stroka = Full_way[:(-1*i)]
    return stroka

"""
def label_maker2(My_blocks, block, My_tool, n):
    stroka = My_blocks[n][0].rstrip('\n') + '  '
    if block[n].title == 'milling':
        stroka = stroka + 'Фрезерование ' + block[n].milling_mode + ',  '
    elif block[n].title == 'milling_GOTO':
        stroka = stroka + 'GOTO фрезерование ' + block[n].milling_mode + ',  '
    elif block[n].title == 'Drill':
        stroka = stroka + 'Сверление,  '
    elif block[n].title == 'old_boring':
        stroka = stroka + 'Старая расточка,  '
    elif block[n].title == 'Loop':
        if len(block[n].loops_names) == 1 and block[n].loops_names[0] == 'P43':
            stroka = stroka + 'Расточка P43,  '
        elif len(block[n].loops_names) == 1 and block[n].loops_names[0] == 'P44':
            stroka = stroka + 'Резьба P44,  '
        elif len(block[n].loops_names) == 1 and block[n].loops_names[0] == 'P47':
            stroka = stroka + 'Конус P47,  '
        elif len(block[n].loops_names) == 1 and block[n].loops_names[0] == 'P80':
            stroka = stroka + 'Плоскость P80,  '
        elif len(block[n].loops_names) == 1 and block[n].loops_names[0] == 'P64':
            stroka = stroka + 'Фланец P64,  '
        elif len(block[n].loops_names) == 1:
            stroka = stroka + 'Цикл ' + block[n].loops_names[0] + ',  '
        else:
            G_stroka = ''
            for j in block[n].loops_names:
                G_stroka = G_stroka + j + ','
            stroka = stroka + 'Циклы ' + G_stroka.rstrip(',') + ',  '
    elif block[n].title == 'Ren_150':
        stroka = stroka + 'Измерения P150,  '
    elif block[n].title == 'Ren_200':
        stroka = stroka + 'Настройка P200,  '
    if block[n].title == 'Ren_200' or block[n].title == 'Ren_150':
        stroka = stroka + 'RENISHAW'
        stroka = stroka + ' ['
        time_second = block[n].time_cutting - int(block[n].time_cutting)
        time_second = int(time_second * 60)
        all_time = str(int(block[n].time_cutting)) + ':'
        all_time = all_time + str(time_second)
        stroka = stroka + all_time + ']'
    else:
        if (int(block[n].tool)-1)<=59:
            if str(My_tool[int(block[n].tool)-1].ToolNameType) == 'Концевая фреза':
                stroka = stroka + 'фреза'
            else:
                stroka = stroka + str(My_tool[int(block[n].tool)-1].ToolNameType)
            stroka = stroka + '(T' + block[n].tool + ') D='
            diametr_sv = '?'
            diametr_sv = str(My_tool[int(block[n].tool)-1].DValue)
            stroka = stroka + diametr_sv + ' L='
            dlina_sv = '?'
            dlina_sv = str(My_tool[int(block[n].tool)-1].LValue)
            stroka = stroka + dlina_sv
            if str(My_tool[int(block[n].tool)-1].ToolNameType) == 'Фреза с радиусом':
                stroka = stroka + ' R='
                stroka = stroka + str(My_tool[int(block[n].tool)-1].RValue)
            if str(My_tool[int(block[n].tool)-1].ToolNameType) == 'Фреза грибковая':
                stroka = stroka + ' B='
                stroka = stroka + str(My_tool[int(block[n].tool)-1].BValue)
            if str(My_tool[int(block[n].tool)-1].ToolNameType) == 'Фреза дисковая':
                stroka = stroka + ' B='
                stroka = stroka + str(My_tool[int(block[n].tool)-1].BValue)
        else:
            stroka = stroka + 'Неопределен' + '(T' + block[n].tool + ')'
        stroka = stroka + ' ['
        time_second = block[n].time_cutting - int(block[n].time_cutting)
        time_second = int(time_second * 60)
        all_time = str(int(block[n].time_cutting)) + ':'
        all_time = all_time + str(time_second)
        stroka = stroka + all_time + ']'
    return stroka
"""

def time_cut(label_timer, block, n):
    stroka = '['
    time_second = block[n].time_cutting - int(block[n].time_cutting)
    time_second = int(time_second * 60)
    all_time = str(int(block[n].time_cutting)) + ':'
    all_time = all_time + str(time_second)
    stroka = stroka + all_time + ']'
    label_timer.setText(stroka)
    return None


def type_operation(label_operation, block, n):
    if block[n].title == 'milling':
        label_operation.setPixmap(QPixmap('Icons_milling/millnig.png'))
        label_operation.setToolTip('ФРЕЗЕРОВАНИЕ')
    elif block[n].title == 'milling_GOTO':
        label_operation.setPixmap(QPixmap('Icons_milling/GOTO_milling.png'))
        label_operation.setToolTip('СТАРОЕ ФРЕЗЕРОВАНИЕ ГДЕ КОНТУР ЗАЦИКЛЕН МЕТКОЙ GOTO')
    elif block[n].title == 'Drill':
        label_operation.setPixmap(QPixmap('Icons_milling/drilling.png'))
        label_operation.setToolTip('СВЕРЛЕНИЕ')
    elif block[n].title == 'old_boring':
        label_operation.setPixmap(QPixmap('Icons_milling/Old_boring.png'))
        label_operation.setToolTip('СТАРАЯ РАСТОЧКА ПРЯМЫМ КОДОМ')
    elif block[n].title == 'Loop':
        label_operation.setPixmap(QPixmap('Icons_milling/loop.png'))
        G_stroka = ''
        for j in block[n].loops_names:
            G_stroka = G_stroka + j + ','
        stroka = 'ЦИКЛЫ ' + G_stroka.rstrip(',') + ',  '
        label_operation.setToolTip(stroka)
    elif block[n].title == 'Ren_150':
        label_operation.setPixmap(QPixmap('Icons_milling/Ren_150.png'))
        label_operation.setToolTip('ИЗМЕРИТЕЛЬНЫЕ 150-Е ПРОГРАММЫ RENISHAW')
    elif block[n].title == 'Ren_200':
        label_operation.setPixmap(QPixmap('Icons_milling/Ren_200.png'))
        label_operation.setToolTip('НАСТРОЕЧНЫЕ 200-Е ПРОГРАММЫ RENISHAW')
    return None


def type_g40(label_g40, block, n):
    if block[n].milling_mode == 'G40':
        label_g40.setPixmap(QPixmap('Icons_milling/G40.png'))
    elif block[n].milling_mode == 'G41':
        label_g40.setPixmap(QPixmap('Icons_milling/G41.png'))
    return None


def type_instrument(label_instrument, block, n, My_tool, amount_tool):
    label_instrument.setPixmap(QPixmap('Icons_milling/unkown.png'))
    label_instrument.setToolTip('НОМЕР ИНСТРУМЕНТА ВНЕ ДИАПАЗОНА 1<=T<=60')
    if (int(block[n].tool)-1)<=amount_tool:
        if str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Концевая фреза' or str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза с напайками':
            label_instrument.setPixmap(QPixmap('Icons_milling/end_mill.png'))
            label_instrument.setToolTip('КОНЦЕВАЯ ФРЕЗА')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза с радиусом':
            label_instrument.setPixmap(QPixmap('Icons_milling/radius_mill.png'))
            label_instrument.setToolTip('ФРЕЗА С РАДИУСОМ')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Сверло':
            label_instrument.setPixmap(QPixmap('Icons_milling/drill.png'))
            label_instrument.setToolTip('СВЕРЛО')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Центровка':
            label_instrument.setPixmap(QPixmap('Icons_milling/centro_drill.png'))
            label_instrument.setToolTip('ЦЕНТРОВОЧНОЕ СВЕРЛО')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза грибковая':
            label_instrument.setPixmap(QPixmap('Icons_milling/mush_milll.png'))
            label_instrument.setToolTip('ФРЕЗА ГРИБКОВАЯ')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза дисковая':
            label_instrument.setPixmap(QPixmap('Icons_milling/Disk_mill.png'))
            label_instrument.setToolTip('ФРЕЗА ДИСКОВАЯ')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза резьбовая':
            label_instrument.setPixmap(QPixmap('Icons_milling/rezb_mill.png'))
            label_instrument.setToolTip('ФРЕЗА РЕЗЬБОВАЯ')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза угловая':
            label_instrument.setPixmap(QPixmap('Icons_milling/angle_mill.png'))
            label_instrument.setToolTip('ФРЕЗА УГЛОВАЯ')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза гравировальная':
            label_instrument.setPixmap(QPixmap('Icons_milling/Grav_mill.png'))
            label_instrument.setToolTip('ФРЕЗА ГРАВИРОВАЛЬНАЯ')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Развертка':
            label_instrument.setPixmap(QPixmap('Icons_milling/razvertka.png'))
            label_instrument.setToolTip('РАЗВЕРТКА')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Renishow OMP-400':
            label_instrument.setPixmap(QPixmap('Icons_milling/renishaw.png'))
            label_instrument.setToolTip('RENISHAW OMP-60')
        elif str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Пустой':
            label_instrument.setPixmap(QPixmap('Icons_milling/empty.png'))
            label_instrument.setToolTip('ИНСТРУМЕНТ ОТСУТСТВУЕТ В КОНУСЕ')
    return None


def number_Tins(label_Tnum, block, n, My_tool, My_blocks,tool_amount):
    stroka = ''
    if (int(block[n].tool) - 1) <= tool_amount:
        stroka = stroka + '(T' + block[n].tool + ')  D'
        diametr_sv = '?'
        diametr_ins = My_tool[int(block[n].tool) - 1].DValue
        if diametr_ins - int(diametr_ins) != 0:
            diametr_sv = str(My_tool[int(block[n].tool) - 1].DValue)
        else:
            diametr_sv = str(int(My_tool[int(block[n].tool) - 1].DValue))
        stroka = stroka + diametr_sv + '  L'
        dlina_sv = '?'
        dlina_sv = str(My_tool[int(block[n].tool) - 1].LValue)
        stroka = stroka + dlina_sv
        if str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза с радиусом':
            stroka = stroka + ' R='
            stroka = stroka + str(My_tool[int(block[n].tool) - 1].RValue)
        if str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза грибковая':
            stroka = stroka + ' B='
            stroka = stroka + str(My_tool[int(block[n].tool) - 1].BValue)
        if str(My_tool[int(block[n].tool) - 1].ToolNameType) == 'Фреза дисковая':
            stroka = stroka + ' B='
            stroka = stroka + str(My_tool[int(block[n].tool) - 1].BValue)
    else:
        stroka = stroka + 'Неизвестный (T' + block[n].tool + ')'
    label_Tnum.setText(stroka)
    stroka_tip = ''
    j = 0
    while j < len(block):
        if block[j].tool == block[n].tool:
            stroka_tip = stroka_tip + My_blocks[j][0].rstrip('\n') + ',  '
        j += 1
    stroka_tip = stroka_tip.rstrip(',  ')
    label_Tnum.setToolTip(stroka_tip)
    return None


# Function reads new arguments S and T from begin of block
def Read_new_TandS(My_blocks):
    my_new_TS = {}
    allow_letters = ('(', '\n', ' ', 'M', 'N')
    j = 0
    numbers = '#-.0123456789'
    while j < len(My_blocks):
        if My_blocks[j][0] in allow_letters:
            if My_blocks[j][0] == ' ' or My_blocks[j][0] == '\n' or My_blocks[j][0] == 'N' or My_blocks[j][0] == '(':
                j += 1
            else:
                arguments = []
                i = 0
                arg = ''
                while i < len(My_blocks[j]):
                    if My_blocks[j][i] == '(' or My_blocks[j][i] == ' ' or My_blocks[j][i] == '\n':
                        arguments.append(arg)
                        i = len(My_blocks[j])
                    elif My_blocks[j][i] not in numbers:
                        if arg != '':
                            arguments.append(arg)
                        arg = My_blocks[j][i]
                    else:
                        arg = arg+My_blocks[j][i]
                    i += 1
                for k in arguments:
                    if k[0] == 'T':
                        my_new_TS['T'] = k[1:]
                    if k[0] == 'S':
                        my_new_TS['S'] = k[1:]
                j += 1
        else:
            j = len(My_blocks)
    return my_new_TS



# Function helps to set new values for S in all blocks
def Set_new_TandS(My_blocks,block,my_new_TS):
    allow_letters = ('(', '\n', ' ', 'M', 'N')
    numbers = '#-.0123456789'
    replace_S = ''
    stroka = ''
    i = 0
    while i < len(My_blocks):
        if block[i].title != 'Ren_200' and block[i].title != 'Ren_150' and block[i].title != 'none':
            if 'T' in my_new_TS:
                if my_new_TS['T'] == block[i].tool:
                    j = 0
                    while j < len(My_blocks[i]):
                        if My_blocks[i][j][0] in allow_letters:
                            if My_blocks[i][j][0] == ' ' or My_blocks[i][j][0] == '\n' or My_blocks[i][j][0] == 'N' or My_blocks[i][j][0] == '(':
                                j += 1
                            else:
                                arguments = []
                                k = 0
                                arg = ''
                                while k < len(My_blocks[i][j]):
                                    if My_blocks[i][j][k] == '(' or My_blocks[i][j][k] == ' ' or My_blocks[i][j][k] == '\n':
                                        arguments.append(arg)
                                        k = len(My_blocks[i][j])
                                    elif My_blocks[i][j][k] not in numbers:
                                        if arg != '':
                                            arguments.append(arg)
                                        arg = My_blocks[i][j][k]
                                    else:
                                        arg = arg+My_blocks[i][j][k]
                                    k += 1
                                for ar in arguments:
                                    if ar[0] == 'S' and 'S' in my_new_TS:
                                        replace_S = 'S' + my_new_TS['S']
                                        stroka = stroka + My_blocks[i][0].rstrip('\n') + '   ' + ar + ' --> ' + replace_S + '\n'
                                        My_blocks[i][j] = My_blocks[i][j].replace(ar,replace_S)
                                j += 1
                        else:
                            j = len(My_blocks[i])
        i += 1
    return stroka


# Function helps to set new values for T in all blocks
def Set_new_allT(tool_n1, tool_n2, My_blocks, block):
    allow_letters = ('(', '\n', ' ', 'M', 'N')
    numbers = '#-.0123456789'
    replace_S = ''
    replaced_n = []
    i = 0
    while i < len(My_blocks):
        if block[i].title != 'Ren_200' and block[i].title != 'Ren_150' and block[i].title != 'none':
            if block[i].tool == tool_n1:
                j = 0
                while j < len(My_blocks[i]):
                    if My_blocks[i][j][0] in allow_letters:
                        if My_blocks[i][j][0] == ' ' or My_blocks[i][j][0] == '\n' or My_blocks[i][j][0] == 'N' or My_blocks[i][j][0] == '(':
                            j += 1
                        else:
                            arguments = []
                            k = 0
                            arg = ''
                            while k < len(My_blocks[i][j]):
                                if My_blocks[i][j][k] == '(' or My_blocks[i][j][k] == ' ' or My_blocks[i][j][k] == '\n':
                                    arguments.append(arg)
                                    k = len(My_blocks[i][j])
                                elif My_blocks[i][j][k] not in numbers:
                                    if arg != '':
                                        arguments.append(arg)
                                    arg = My_blocks[i][j][k]
                                else:
                                    arg = arg+My_blocks[i][j][k]
                                k += 1
                            for ar in arguments:
                                if ar[0] == 'T' and ar[1:] == tool_n1:
                                    replace_T = 'T' + tool_n2
                                    My_blocks[i][j] = My_blocks[i][j].replace(ar,replace_T)
                                    replaced_n.append(i)
                            j += 1
                    else:
                        j = len(My_blocks[i])
        i += 1
    return replaced_n


# Make list of tool's number for tip when we change T numbers
def helper_field_T(block, My_blocks):
    T_numbers = []
    stroka = 'Инструмент встречающийся в программе:\n'
    j = 1
    while j < len(block):
        if block[j].tool not in T_numbers:
            T_numbers.append(block[j].tool)
        j += 1
    for i in T_numbers:
        stroka = stroka + 'T' + i + ': '
        j = 1
        while j < len(My_blocks):
            if i == block[j].tool:
               stroka = stroka + My_blocks[j][0].rstrip('\n') + ', '
            j += 1
        stroka = stroka.rstrip(', ') + '\n'
    return stroka


class My_current_page:
        def __init__(self, old_Textpage, new_Textpage, check_mistakesBlock, switch_check,tool_amount,name_of_mainFile, way_of_mainFile,file_without_changing):
            self.old_Textpage = old_Textpage
            self.new_Textpage = new_Textpage
            self.check_mistakesBlock = check_mistakesBlock
            self.switch_check = switch_check
            self.tool_amount = tool_amount
            self.name_of_mainFile = name_of_mainFile
            self.way_of_mainFile = way_of_mainFile
            self.file_without_changing = file_without_changing

