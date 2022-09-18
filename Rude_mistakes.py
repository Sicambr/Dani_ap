"""This modul will find rude mistakes and will
find arguments for different loops
"""

class Rude_mist:
    def __init__(self,Myblock, title, correctT, diametr_f = 0):
        self.Myblock = Myblock
        self.title = title
        self.drill_arg = {}
        self.loop_arg = {}
        self.rude_mistakes = {'total': 0}
        self.param = {'#510':0,'#511':0,'#512':0}
        self.warning_m = {'total': 0}
        self.radius_f = diametr_f / 2
        self.milling_mode = 'G40'
        self.loops_names = []
        self.correctH = 'None'
        self.correctS = 'None'
        self.correctC = 'None'
        self.correctT = correctT
        self.correctB = '0'
        
        
    # Try to find rude mistakes
    def rude_mist(self):
        if self.title == 'milling':
            self.mis_in_Milling()
        if self.title == 'Drill':
            self.mis_in_Drill()
        if self.title == 'Loop':
            self.mis_in_Loop()
        if self.title == 'milling_GOTO':
            self.mis_in_MillingGOTO()
        if self.title == 'Ren_150':
            self.mis_in_Ren150()
        if self.title == 'Ren_200':
            self.mis_in_Ren200()
        return self.rude_mistakes


    # Try to find mistakes in 'milling' category of block
    def mis_in_Milling(self):
        allow_M = ('M6','M3','M8','M138','M12','M0','M00','M9','M5','M53','M30')
        allow_Gfunc = ('G211','G0','G1','G2','G3','G304','G201','G40',
                       'G41','G42','G49','G69')
        allow_letters = 'NMTHBSGCXYZFR'
        numbers = '0123456789.-#'
        i = 0
        mark_slesh = 0
        while i < len(self.Myblock):
            if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%':
                self.Myblock[i] = self.Myblock[i].rstrip('\n')
                self.Myblock[i] = self.Myblock[i].replace(' ','')
                if self.Myblock[i][0] == '/':
                    mark_slesh = 1
                self.Myblock[i] = self.Myblock[i].lstrip('/')
                self.first_check(self.Myblock[i], allow_M, allow_Gfunc, allow_letters, numbers, i)
                self.Myblock[i] = self.Myblock[i] + '\n'
                if mark_slesh == 1:
                    self.Myblock[i] = '/' + self.Myblock[i]
                    mark_slesh = 0
            i += 1
        if self.rude_mistakes['total'] == 0:
            self.check_face()
        return self.rude_mistakes



    #Check top face part of block. Fit for milling
    def check_face(self):
        i = 0
        arguments = []
        next_i = 0
        #Command M6T13H0B0
        while i < len (self.Myblock):
            if self.Myblock[i][0] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            else:
                if len(self.Myblock[i]) < 4:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Кадр должен начинаться с команды M6T(номер инструмента)*'+ str(i)
                    i = len(self.Myblock)
                elif len(self.Myblock[i]) >= 4 and 'M6T' not in self.Myblock[i]:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Кадр должен начинаться с команды M6T(номер инструмента)*'+ str(i)
                    i = len(self.Myblock)
                else:
                    arguments = self.arg_read(self.Myblock[i])
                    allow_m6_letters = 'MTHB'
                    allow_h = ('0','1','2','3','4','5','6','7','8','9')
                    for j in arguments:
                        if j[0] not in allow_m6_letters:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Кадр смены инструмента должен быть вида M_T_H_B_. Аргумент '+j[0]+' лишний*'+ str(i)
                            i = len(self.Myblock)
                        else:
                            if (j[0] == 'T' and int(j[1:]) < 1) or (j[0] == 'T' and int(j[1:]) > 60):
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Номер инструмента вне диапазона магазина BUMOTEC 1<=T<=60*'+ str(i)
                                i = len(self.Myblock)
                                self.correctT = j[1:]
                            elif (j[0] == 'T' and int(j[1:]) >= 1) or (j[0] == 'T' and int(j[1:]) <= 60):
                                self.correctT = j[1:]
                            if j[0] == 'H' and j[1:] not in allow_h:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Корректор инструмента H может быть целым числом в диапазоне 0<=H<=9 для BUMOTEC*'+ str(i)
                                i = len(self.Myblock)
                            elif j[0] == 'H' and j[1:] in allow_h:
                                self.correctH = j[1:]
                            if j[0] == 'B' and j[1:] != '0' :
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Угол поворота головы должен быть B=0 для команды M6*'+ str(i)
                                i = len(self.Myblock)
                    if i < len(self.Myblock):
                        if 'H' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Отсутствует корректор H в команде смены инструмента M6*'+ str(i)
                            i = len(self.Myblock)
                    next_i = i + 1
                    i = len(self.Myblock)
                i += 1
        i = next_i
        # Command M3S11650
        while i < len (self.Myblock):
            if self.Myblock[i][0] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            else:
                if len(self.Myblock[i]) < 4:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'После команды смены инструмента M6 должна стоять команда включения оборотов M3S(обороты)*'+ str(i)
                    i = len(self.Myblock)
                elif len(self.Myblock[i]) >= 4 and 'M3S' not in self.Myblock[i]:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'После команды смены инструмента M6 должна стоять команда включения оборотов M3S(обороты)*'+ str(i)
                    i = len(self.Myblock)
                else:
                    arguments = self.arg_read(self.Myblock[i])
                    allow_m3s_letters = 'MS'
                    for j in arguments:
                        if j[0] not in allow_m3s_letters:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Кадр включения оборотов должен быть вида M3S_. Аргумент '+j[0]+' лишний*'+ str(i)
                            i = len(self.Myblock)
                        else:
                            if j[0] == 'S' and float(j[1:]) < 50:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Слишком низкие обороты*'+ str(i)
                                i = len(self.Myblock)
                            if j[0] == 'S' and float(j[1:]) > 30000:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Слишком высокие обороты! При S > 35000 отправишь шпиндель в мульду*'+ str(i)
                                i = len(self.Myblock)
                            if j[0] == 'S' and float(j[1:]) > 50 and float(j[1:]) < 30000:
                                self.correctS = j[1:]
                    next_i = i + 1
                    i = len(self.Myblock)
                i += 1
        i = next_i
        # Command G0C27
        while i < len (self.Myblock):
            if self.Myblock[i][0] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            else:
                if len(self.Myblock[i]) < 4:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'После команды включения оборотов M3S(обороты) должна стоять команда поворота стола G0C(Угол)*'+ str(i)
                    i = len(self.Myblock)
                elif len(self.Myblock[i]) >= 4 and 'G0C' not in self.Myblock[i]:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'После команды включения оборотов M3S(обороты) должна стоять команда поворота стола G0C(Угол)*'+ str(i)
                    i = len(self.Myblock)
                else:
                    arguments = self.arg_read(self.Myblock[i])
                    allow_GC_letters = 'GC'
                    for j in arguments:
                        if j[0] not in allow_GC_letters:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'В кадре поворота на угол C, арумент '+j[0]+' лишний*'+ str(i)
                            i = len(self.Myblock)
                        else:
                            if j[0] == 'G' and j[1:] != '0':
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Поставь команду G0C(угол) для поворота на угол C*'+ str(i)
                                i = len(self.Myblock)
                            if j[0] == 'C' and float(j[1:]) < -360:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Угол поворота стола должен быть задан в диапазоне -360<=C<=360*'+ str(i)
                                i = len(self.Myblock)
                            if j[0] == 'C' and float(j[1:]) > 360:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Угол поворота стола должен быть задан в диапазоне -360<=C<=360*'+ str(i)
                                i = len(self.Myblock)                                
                            if j[0] == 'C' and float(j[1:]) >= -360 and float(j[1:]) <= 360:
                                self.correctC = j[1:]
                    next_i = i + 1
                    i = len(self.Myblock)
                i += 1
        i = next_i
        #additional check if angle B!=0
        while i < len (self.Myblock):
            if self.Myblock[i][0] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            else:
                if len(self.Myblock[i]) < 4:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'После команды G0C(Угол) должна стоять команда G211 (если B>0) или G304 (если B=0)*'+ str(i)
                    i = len(self.Myblock)
                elif len(self.Myblock[i]) >= 4 and 'G211' not in self.Myblock[i] and 'G304' not in self.Myblock[i]:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'После команды G0C(Угол) должна стоять команда G211 (если B>0) или G304 (если B=0)*'+ str(i)
                    i = len(self.Myblock)
                elif len(self.Myblock[i]) >= 4 and 'G211' in self.Myblock[i]:
                    i = self.dop_checkB90(i)
                next_i = i
                i = len(self.Myblock)
        i = next_i
        # G304X#510Y#511Z#512C270.0
        while i < len (self.Myblock):
            if self.Myblock[i][0] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            else:
                if len(self.Myblock[i]) < 15:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Пропущена команда G304 перед G201*'+ str(i)
                    i = len(self.Myblock)
                elif len(self.Myblock[i]) >= 4 and self.Myblock[i][:4] != 'G304':
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Пропущена команда G304 перед G201*'+ str(i)
                    i = len(self.Myblock)                    
                else:
                    arguments = self.arg_read(self.Myblock[i])
                    allow_G304_letters = 'GXYZC'
                    for j in arguments:
                        if j[0] not in allow_G304_letters:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'В команде G304 не должно присутствовать аргумента '+ j +'*'+ str(i)
                            i = len(self.Myblock)
                        else:
                            if j[0] == 'X' and j[1:] != '#510':
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Смещение для X в G304 должно задаваться через #510*'+ str(i)
                                i = len(self.Myblock)
                            if j[0] == 'Y' and j[1:] != '#511':
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Смещение для Y в G304 должно задаваться через #511*'+ str(i)
                                i = len(self.Myblock)                                
                            if j[0] == 'Z' and j[1:] != '#512':
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Смещение для Z в G304 должно задаваться через #512*'+ str(i)
                                i = len(self.Myblock)                                
                            if j[0] == 'C' and float(j[1:]) != float(self.correctC):
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Угол C в команде G304 должен совпадать с углом поворота стола заданным выше в коде*'+ str(i)
                                i = len(self.Myblock)                                
                    if i != len(self.Myblock):
                        if 'X' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан X#510 в команде G304*'+ str(i)
                            i = len(self.Myblock)
                        if i != len(self.Myblock) and 'Y' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан Y#511 в команде G304*'+ str(i)
                            i = len(self.Myblock)
                        if i != len(self.Myblock) and 'Z' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан Z#512 в команде G304*'+ str(i)
                            i = len(self.Myblock)
                        if i != len(self.Myblock) and 'C' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть указан угол C в команде G304*'+ str(i)
                            i = len(self.Myblock)
                    next_i = i + 1
                    i = len(self.Myblock)
                i += 1
        i = next_i
        # G201X0Y0Z0B90.0
        while i < len (self.Myblock):
            if self.Myblock[i][0] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            else:
                if len(self.Myblock[i]) < 12:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Пропущена команда G201 после G304*'+ str(i)
                    i = len(self.Myblock)
                elif len(self.Myblock[i]) >= 4 and self.Myblock[i][:4] != 'G201':
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Пропущена команда G201 после G304*'+ str(i)
                    i = len(self.Myblock)                    
                else:
                    arguments = self.arg_read(self.Myblock[i])
                    allow_G304_letters = 'GXYZB'
                    for j in arguments:
                        if j[0] not in allow_G304_letters:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'В команде G201 не должно присутствовать аргумента '+ j +'*'+ str(i)
                            i = len(self.Myblock)
                        else:
                            if j[0] == 'B' and float(j[1:]) != float(self.correctB): 
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Угол B в команде G201 должен совпадать с углом поворота B заданного после G211*'+ str(i)
                                i = len(self.Myblock)                                
                    if i != len(self.Myblock):
                        if 'X' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан X в команде G201*'+ str(i)
                            i = len(self.Myblock)
                        if i != len(self.Myblock) and 'Y' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан Y в команде G201*'+ str(i)
                            i = len(self.Myblock)
                        if i != len(self.Myblock) and 'Z' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан Z в команде G201*'+ str(i)
                            i = len(self.Myblock)
                        if i != len(self.Myblock) and 'B' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть указан угол B в команде G201*'+ str(i)
                            i = len(self.Myblock)
                    next_i = i + 1
                    i = len(self.Myblock)
                i += 1
        i = next_i
        return None
        



    #Additional check for angle B!=0
    def dop_checkB90(self, i):
        while i < len (self.Myblock):
            if self.Myblock[i][0] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            else:
                arguments = self.arg_read(self.Myblock[i])
                allow_G211_letters = 'G'
                for j in arguments:
                    if j[0] not in allow_G211_letters:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'В кадре G211 не должно встречаться других аргументов*'+ str(i)
                        i = len(self.Myblock)
                next_i = i + 1
                i = len(self.Myblock)
        i = next_i
        # Command G0X60Y0Z100B90
        while i < len (self.Myblock):
            if self.Myblock[i][0] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            else:
                if len(self.Myblock[i]) < 11:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'После команды G211 должна стоять точка разворота на угол B формата G0X_Y_Z_B_*'+ str(i)
                    i = len(self.Myblock)
                elif len(self.Myblock[i]) >= 11 and self.Myblock[i][:2] != 'G0':
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Команда должна начинаться с G0 в этой строке*'+ str(i)
                    i = len(self.Myblock)                    
                else:
                    arguments = self.arg_read(self.Myblock[i])
                    allow_Gt_letters = 'GXYZB'
                    for j in arguments:
                        if j[0] not in allow_Gt_letters:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'В кадре после G211 не должно присутствовать аргумента '+ j +'*'+ str(i)
                            i = len(self.Myblock)
                        else:
                            if j[0] == 'G' and j[1:] != '0':
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Поставь команду G0 для кадра разворота головы*'+ str(i)
                                i = len(self.Myblock)
                            if j[0] == 'X' and float(j[1:]) < 60:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Отодвинь точку X хотя бы на 60 для разворота B*'+ str(i)
                                i = len(self.Myblock)
                            if j[0] == 'Z' and float(j[1:]) < 0:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Отодвинь точку Z выше над деталью для разворота B*'+ str(i)
                                i = len(self.Myblock)                                
                            if j[0] == 'B' and float(j[1:]) < -25:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Угол поворота головы B должен быть в диапазоне -25<=B<=115*'+ str(i)
                                i = len(self.Myblock)                                
                            if j[0] == 'B' and float(j[1:]) > 115:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Угол поворота головы B должен быть в диапазоне -25<=B<=115*'+ str(i)
                                i = len(self.Myblock)
                            if j[0] == 'B' and float(j[1:]) >= -25 and float(j[1:]) <= 115:
                                self.correctB = j[1:]
                    if i != len(self.Myblock):
                        if 'X' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан X в строке с поворотом угла B после G211*'+ str(i)
                            i = len(self.Myblock)
                        if i != len(self.Myblock) and 'Y' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан Y в строке с поворотом угла B после G211*'+ str(i)
                            i = len(self.Myblock)
                        if i != len(self.Myblock) and 'Z' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан Z в строке с поворотом угла B после G211*'+ str(i)
                            i = len(self.Myblock)
                        if i != len(self.Myblock) and 'B' not in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Должен быть задан угол B в строке с поворотом после G211*'+ str(i)
                            i = len(self.Myblock)
                    next_i = i + 1
                    i = len(self.Myblock)
                i += 1
        i = next_i
        # Command G49
        while i < len (self.Myblock):
            if self.Myblock[i][0] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            elif len(self.Myblock[i]) < 3:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'После разворота по G211 должна быть команда G49*'+ str(i)
                i = len(self.Myblock)
            elif len(self.Myblock[i]) >= 3 and self.Myblock[i][:3] != 'G49':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'После разворота по G211 должна быть команда G49*'+ str(i)
                i = len(self.Myblock)
            else:
                arguments = self.arg_read(self.Myblock[i])
                allow_G49_letters = 'G'
                for j in arguments:
                    if j[0] not in allow_G49_letters:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'В кадре G49 не должно встречаться других аргументов*'+ str(i)
                        i = len(self.Myblock)
                next_i = i + 1
                i = len(self.Myblock)
        i = next_i
        return i
    


    # Try to find mistakes in 'Drill' category of block
    def mis_in_Drill(self):
        allow_M = ('M6','M3','M8','M138','M12','M0','M00','M9','M5','M53','M30','M240','M241')
        allow_Gfunc = ('G211','G0','G1','G304','G201','G40','G81','G83','G80',
                       'G49','G69')
        allow_letters = 'NMTHBSGCXYZFRQ'
        numbers = '0123456789.-#'
        i = 0
        mark_slesh = 0
        # Try to find parametr means and save it
        i = 0
        while i < len(self.Myblock):
            if self.Myblock[i][0] == '#':
                self.Myblock[i] = self.Myblock[i].rstrip('\n')
                self.Myblock[i] = self.Myblock[i].replace(' ','')
                self.param_reader(self.Myblock[i],i)
                self.Myblock[i] = self.Myblock[i] + '\n'          
            i += 1        
        i = 0
        while i < len(self.Myblock):
            if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%' and self.Myblock[i][0] != '#':
                self.Myblock[i] = self.Myblock[i].rstrip('\n')
                self.Myblock[i] = self.Myblock[i].replace(' ','')
                if self.Myblock[i][0] == '/':
                    mark_slesh = 1
                self.Myblock[i] = self.Myblock[i].lstrip('/')                
                self.first_check(self.Myblock[i], allow_M, allow_Gfunc, allow_letters, numbers, i)
                self.Myblock[i] = self.Myblock[i] + '\n'
                if mark_slesh == 1:
                    self.Myblock[i] = '/' + self.Myblock[i]
                    mark_slesh = 0                
            i += 1
        if self.rude_mistakes['total'] == 0:
            self.check_face()
        i = 0
        # Check mistakes in title
        if self.rude_mistakes['total'] == 0:
            arg = []
            marker = 0
            X = 0.0
            Y = 0.0
            Z = 0.0
            R = 0.0
            Q = 0.0
            F = 0.0
            all_arg = {}
            G_mode = 'G1'
            while marker == 0:
                if 'G201' in self.Myblock[i]:
                    marker = 1
                i += 1
            while i < len(self.Myblock):
                if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%' and self.Myblock[i][0] != '#':
                    if self.Myblock[i][0] == '/':
                        mark_slesh = 1
                    self.Myblock[i] = self.Myblock[i].lstrip('/')                    
                    arg = self.arg_read(self.Myblock[i])
                    arg_loop = self.arg_read(self.Myblock[i])
                    for j in arg_loop:
                        if j[1] == '#':
                            if j[1:] == '#510' or j[1:] == '#511' or j[1:] == '#512':
                                all_arg[j[0]] = 0
                            elif j[1:] not in self.param:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Значение не опеределено для '+j[1:]+'в этом блоке*'+ str(i)                                
                            else:
                                all_arg[j[0]] = self.param[j[1:]]
                        else:
                            all_arg[j[0]] = float(j[1:])
                if self.rude_mistakes['total'] == 0:
                    for j in arg:
                        if 'X' in j:
                            if j[1] == '#' and j[1:] in self.param:
                                X2 = self.param[j[1:]]
                            else:
                                X2 = float(j[1:])                    
                        elif 'Y' in j:
                            if j[1] == '#' and j[1:] in self.param:
                                Y2 = self.param[j[1:]]
                            else:
                                Y2 = float(j[1:])                    
                        elif 'Z' in j:
                            if j[1] == '#' and j[1:] in self.param:
                                Z2 = self.param[j[1:]]
                            else:
                                Z2 = float(j[1:])                    
                        elif 'R' in j:
                            if j[1] == '#' and j[1:] in self.param:
                                R = self.param[j[1:]]
                            else:
                                R = float(j[1:])                    
                        elif 'F' in j:
                            if j[1] == '#' and j[1:] in self.param:
                                F = self.param[j[1:]]
                            else:
                                F = float(j[1:])
                        elif 'Q' in j:
                            if j[1] == '#' and j[1:] in self.param:
                                Q = self.param[j[1:]]
                            else:
                                Q = float(j[1:]) 
                    if 'G81' in self.Myblock[i]:
                        G_mode = 'G81'
                    elif 'G83' in self.Myblock[i]:
                        G_mode = 'G83'
                    elif 'G1' in self.Myblock[i]:
                        G_mode = 'G1'
                    elif 'G80' in self.Myblock[i]:
                        G_mode = 'G1'
                    if G_mode == 'G81':
                        if R <= Z:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Уровень R должен быть выше уровня Z в цикле сверления G81*' + str(i)
                        if F <= 0:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Подача F в цикле сверления G81 слишком медленная или отсутствует*' + str(i)
                        elif F > 500:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Подача F > 500 в цикле сверления G81!*' + str(i)
                    elif G_mode == 'G83':
                        if R <= Z:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Уровень R должен быть выше уровня Z в цикле сверления G83*' + str(i)
                        if F <= 0:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Подача F в цикле сверления G83 слишком медленная или отсутствует*' + str(i)
                        elif F > 500:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Подача F > 500 в цикле сверления G83!*' + str(i)                                
                        if Q <= 0:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Съем Q <= 0 в цикле сверления G83!*' + str(i)
                    if mark_slesh == 1:
                        self.Myblock[i] = '/' + self.Myblock[i]
                        mark_slesh = 0                             
                i += 1
        return self.rude_mistakes



    # Try to find mistakes in 'mis_in_MillingGOTO' category of block
    def mis_in_MillingGOTO(self):
        allow_M = ('M6','M3','M8','M138','M12','M0','M00','M9','M5','M53','M30','M240','M241')
        allow_Gfunc = ('G211','G0','G1','G304','G201','G40','G41','G2','G3','G49','G69','G31')
        allow_letters = 'NMTHBSGCXYZFROI'
        numbers = '0123456789.-#'
        i = 0
        mark_slesh = 0
        while i < len(self.Myblock):
            if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%':
                self.Myblock[i] = self.Myblock[i].rstrip('\n')
                self.Myblock[i] = self.Myblock[i].replace(' ','')
                if self.Myblock[i][0] == '/':
                    mark_slesh = 1
                self.Myblock[i] = self.Myblock[i].lstrip('/')                
                self.GOTOfirst_check(self.Myblock[i], allow_M, allow_Gfunc, allow_letters, numbers, i)
                self.Myblock[i] = self.Myblock[i] + '\n'
                if mark_slesh == 1:
                    self.Myblock[i] = '/' + self.Myblock[i]
                    mark_slesh = 0                
            i += 1
        if self.rude_mistakes['total'] == 0:
            self.check_face()
        return self.rude_mistakes


    # Check rude mistakes in loop
    def mis_in_Loop(self):
        allow_M = ('M6','M3','M8','M138','M12','M0','M00','M9','M5','M53','M30','M2','M4','M10','M14','M1.4','M1.6','M2.5','M16','M18','M20')
        allow_Gfunc = ('G211','G0','G1','G304','G201','G40','G49','G69','G65','G66','G67')
        allow_loops = ('P43','P44','P47','P62','P63','P64','P71','P80')
        allow_letters = 'NMPTHBSGCXYZFRQWVKEABIJUQD'
        numbers = '0123456789.-#'
        mark_slesh = 0
        # Try to find parametr means and save it
        i = 0
        while i < len(self.Myblock):
            if self.Myblock[i][0] == '#':
                self.Myblock[i] = self.Myblock[i].rstrip('\n')
                self.Myblock[i] = self.Myblock[i].replace(' ','')
                self.param_reader(self.Myblock[i],i)
                self.Myblock[i] = self.Myblock[i] + '\n'          
            i += 1        
        i = 0
        while i < len(self.Myblock):
            if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%' and self.Myblock[i][0] != '#':
                self.Myblock[i] = self.Myblock[i].rstrip('\n')
                self.Myblock[i] = self.Myblock[i].replace(' ','')
                if self.Myblock[i][0] == '/':
                    mark_slesh = 1
                self.Myblock[i] = self.Myblock[i].lstrip('/')                
                self.first_check(self.Myblock[i], allow_M, allow_Gfunc, allow_letters, numbers, i)
                self.Myblock[i] = self.Myblock[i] + '\n'
                if mark_slesh == 1:
                    self.Myblock[i] = '/' + self.Myblock[i]
                    mark_slesh = 0                
            i += 1
        if self.rude_mistakes['total'] == 0:
            self.check_face()
        i = 0
        if self.rude_mistakes['total'] == 0:
            all_arg = {}
            old_P = ''
            now_P = ''
            G65_mode = 'G65'
            while i < len(self.Myblock):
                if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%' and self.Myblock[i][0] != '#':
                    if self.Myblock[i][0] == '/':
                        mark_slesh = 1
                    self.Myblock[i] = self.Myblock[i].lstrip('/')                    
                    arg_loop = self.arg_read(self.Myblock[i])
                    for j in arg_loop:
                        if 'G' in j[0] and self.Myblock[i].count(j) > 1:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Повторение функции '+j+'*'+ str(i)
                        if 'P' in j[0] and j not in allow_loops:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Вызов неизвестной подпрограммы '+j+'*'+ str(i)
                        if j[1] == '#':
                            if j[1:] == '#510' or j[1:] == '#511' or j[1:] == '#512':
                                all_arg[j[0]] = 0
                            elif j[1:] not in self.param:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Значение не опеределено для '+j[1:]+'*'+ str(i)                                
                            else:
                                all_arg[j[0]] = self.param[j[1:]]
                        else:
                            all_arg[j[0]] = float(j[1:])
                    old_P = now_P
                    if self.rude_mistakes['total'] == 0 and 'P44' in arg_loop:
                        G65_mode = 'G66'
                        if 'G65' in self.Myblock[i]:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Макропрограмма нарезания резьбы P44 должна вызываться через G66*'+ str(i)
                    if 'G67' in self.Myblock[i]:
                        G65_mode = 'G65'
                    if self.rude_mistakes['total'] == 0:
                        if G65_mode == 'G66':
                            for n in arg_loop:
                                if n[0] not in 'ZWMVKEGPXY':
                                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                    mis = self.rude_mistakes['total']
                                    self.rude_mistakes[mis] = 'Неправильный аргумент для макропрограммы P44*'+ str(i)
                                if n[0]=='G' and n != 'G66':
                                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                    mis = self.rude_mistakes['total']
                                    self.rude_mistakes[mis] = 'Неверная G функция во время режима работы G66. Макропрограмма P44 должна заканчиваться функцией G67*'+ str(i)
                                if n[0]=='P' and n != 'P44':
                                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                    mis = self.rude_mistakes['total']
                                    self.rude_mistakes[mis] = 'Только макропрограмма P44 может работать в режиме G66*'+ str(i)
                            if self.rude_mistakes['total'] == 0:
                                if 'P44' not in self.loops_names:
                                    self.loops_names.append('P44')
                                now_P = 'P44'
                                self.P44_check(self.Myblock[i],all_arg,i,self.radius_f)                                
                        if 'P43' in arg_loop:
                            queue = 2
                            now_P = 'P43'
                            if 'P43' not in self.loops_names:
                                self.loops_names.append('P43')
                            if old_P != now_P:
                                queue = 1
                            all_arg = self.P43_check(self.Myblock[i],all_arg,queue,i,self.radius_f,arg_loop)
                        if 'P80' in arg_loop:
                            queue = 2
                            now_P = 'P80'
                            if 'P80' not in self.loops_names:
                                self.loops_names.append('P80')
                            if old_P != now_P:
                                queue = 1
                            self.P80_check(self.Myblock[i],all_arg,queue,i,arg_loop)
                        if 'P64' in arg_loop:
                            queue = 2
                            now_P = 'P64'
                            if 'P64' not in self.loops_names:
                                self.loops_names.append('P64')
                            if old_P != now_P:
                                queue = 1
                            I_pos = -1
                            J_pos = -1
                            K_pos = -1
                            if 'I' in self.Myblock[i]:
                                I_pos = self.Myblock[i].index('I')
                            if 'J' in self.Myblock[i]:
                                J_pos = self.Myblock[i].index('J')
                            if 'K' in self.Myblock[i]:
                                K_pos = self.Myblock[i].index('K')
                            if I_pos > -1 and J_pos > -1 and K_pos > -1:
                                if J_pos < I_pos:
                                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                    mis = self.rude_mistakes['total']
                                    self.rude_mistakes[mis] = 'Аргумент I должен стоять перед аргументом J в P64*'+ str(i)
                                if K_pos < I_pos:
                                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                    mis = self.rude_mistakes['total']
                                    self.rude_mistakes[mis] = 'Аргумент I должен стоять перед аргументом K в P64*'+ str(i)                                
                                if K_pos < J_pos:
                                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                    mis = self.rude_mistakes['total']
                                    self.rude_mistakes[mis] = 'Аргумент J должен стоять перед аргументом K в P64*'+ str(i)                                
                            elif I_pos > -1 and J_pos > -1 and J_pos < I_pos:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Аргумент I должен стоять перед аргументом J в P64*'+ str(i)
                            elif I_pos > -1 and K_pos > -1 and K_pos < I_pos:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Аргумент I должен стоять перед аргументом K в P64*'+ str(i)                                
                            elif J_pos > -1 and K_pos > -1 and K_pos < J_pos:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Аргумент J должен стоять перед аргументом K в P64*'+ str(i)                                
                            self.Myblock[i]
                            self.P64_check(self.Myblock[i],all_arg,queue,i,arg_loop)
                        if 'P47' in arg_loop:
                            queue = 2
                            now_P = 'P47'
                            if 'P47' not in self.loops_names:
                                self.loops_names.append('P47')
                            if old_P != now_P:
                                queue = 1
                            self.P47_check(self.Myblock[i],all_arg,queue,i,self.radius_f,arg_loop)
                        if 'P62' in arg_loop:
                            queue = 2
                            now_P = 'P62'
                            if 'P62' not in self.loops_names:
                                self.loops_names.append('P62')
                            if old_P != now_P:
                                queue = 1
                            self.P62_check(self.Myblock[i],all_arg,queue,i,self.radius_f,arg_loop)
                        if 'P63' in arg_loop:
                            queue = 2
                            now_P = 'P63'
                            if 'P63' not in self.loops_names:
                                self.loops_names.append('P63')
                            if old_P != now_P:
                                queue = 1
                            self.P63_check(self.Myblock[i],all_arg,queue,i,self.radius_f,arg_loop)
                    if mark_slesh == 1:
                        self.Myblock[i] = '/' + self.Myblock[i]
                        mark_slesh = 0                    
                i += 1
        return self.rude_mistakes


    # First check for all types of titels
    def first_check(self,stroka,allow_M,allow_Gfunc,allow_letters,numbers,i):
        j = 0
        arguments = []
        name_ar = ''
        marker = 0
        while j < len(stroka):
            if stroka[j] in allow_letters:
                name_ar = stroka[j]
                j += 1
                while j < len(stroka) and  stroka[j] in numbers:
                    name_ar = name_ar + stroka[j]
                    j += 1
                arguments.append(name_ar)
                j -= 1
            else:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Неправильный символ ' + stroka[j] + ' в строке*'  + str(i)
                j = len(stroka)
                marker += 1
            j += 1
        if marker == 0:
            for a in arguments:
                if len(a) == 1 or len(a.replace('#','').replace('-','').replace('.','')) == 1:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Пустые аргументы в строке*' + str(i)
                elif (a.count('.') > 1 or a.count('#') > 1 or a.count('-') > 1):
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Слишком много знаков для аргумента ' + a[0] + '*' + str(i)
                elif a.count('-') != 0 and a[1:][0] != '-' :
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Знак минус стоит не на месте*' + str(i)
                elif a.count('#') != 0 and a[1:][0] != '#' :
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Значек # стоит не на месте*' + str(i)
                elif a[0] == 'G' and a not in allow_Gfunc:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Недопустимая G функция*' + str(i)
                elif a == 'G41':
                    self.milling_mode = 'G41'
                elif a[0] == 'M' and a not in allow_M:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Недопустимая M функция*' + str(i)
                elif a[0] == 'F':
                    if a[1] == '#' and a[1:] in self.param:
                        if float(self.param[a[1:]]) > 5000:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Слишком высокая подача F > 5000*' + str(i)
                        elif float(self.param[a[1:]]) < 10:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Слишком медленная подача F < 10*' + str(i)                            
                    elif a[1] == '#' and a[1:] not in self.param:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Значение данного номера # для F не определено в этом кадре*' + str(i)                      
                    elif float(a[1:]) > 5000:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Слишком высокая подача F > 5000*' + str(i)
                    elif float(a[1:]) < 10:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Слишком медленная подача F < 10*' + str(i)
                elif a[0] == 'S' and self.title != 'Ren_150' and self.title != 'Ren_200':
                    if a[1] == '#' and a[1:] in self.param:
                        if float(self.param[a[1:]]) > 30000:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Слишком высокие обороты S! Отправиш шпиндель в мульду*' + str(i)                        
                        elif float(self.param[a[1:]]) < 10:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Слишком маленькие обороты S!*' + str(i)                        
                    elif a[1] == '#' and a[1:] not in self.param:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Значение данного номера # для S не определено в этом кадре*' + str(i)                      
                    elif float(a[1:]) > 30000:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Слишком высокие обороты S! Отправиш шпиндель в мульду*' + str(i)
                    elif float(a[1:]) < 10:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Слишком маленькиее обороты S!*' + str(i)
                elif a[0] == 'T':
                    if float(a[1:]) > 60 or float(a[1:]) < 1 :
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Номер инструмента вне диапазона магазина BUMOTEC 1<T<60*' + str(i)                        
        if (stroka.count('X') > 1 or stroka.count('Y') > 1
            or stroka.count('Z') > 1 or stroka.count('R') > 1
            or stroka.count('F') > 1 or stroka.count('N') > 1
            or stroka.count('T') > 1 or stroka.count('H') > 1
            or stroka.count('B') > 1 or stroka.count('S') > 1
            or stroka.count('A') > 1 or stroka.count('B') > 1
            or stroka.count('I') > 1 or stroka.count('J') > 1
            or stroka.count('V') > 1 or stroka.count('W') > 1
            or stroka.count('K') > 1 or stroka.count('E') > 1
            or stroka.count('U') > 1 or stroka.count('Q') > 1
            or stroka.count('P') > 1 or stroka.count('D') > 1
            or stroka.count('C') > 1):
            povt_arg = 'XZFTBAIVKUPCYRNHSBJWEQD'
            double_arg = ''
            for k in povt_arg:
                if stroka.count(k) > 1:
                    double_arg = k        
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Повторяющийся аргумент ' + double_arg + ' в строке*' + str(i)
        return self.rude_mistakes


    # First check for GOTO milling (special)
    def GOTOfirst_check(self,stroka,allow_M,allow_Gfunc,allow_letters,numbers,i):
        j = 0
        arguments = []
        name_ar = ''
        marker = 0
        if stroka[0] == '#':
            self.check_parGOTO(stroka,i)
        elif stroka[0] == 'I':
            self.check_IFstroka(stroka,i)
        else:
            while j < len(stroka):
                if stroka[j] == '(':
                    k = j + 1
                    while k < len(stroka):
                        if k == ')':
                            k = len(stroka)
                        j += 1
                        k += 1
                elif stroka[j] in allow_letters:
                    name_ar = stroka[j]
                    j += 1
                    while j < len(stroka) and  stroka[j] in numbers:
                        name_ar = name_ar + stroka[j]
                        j += 1
                    arguments.append(name_ar)
                    j -= 1
                else:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Неправильный символ ' + stroka[j] + ' в строке*' + str(i)
                    j = len(stroka)
                    marker += 1
                j += 1
        if marker == 0:
            for a in arguments:
                if len(a) == 1 or len(a.replace('#','').replace('-','').replace('.','')) == 1:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Пустые аргументы в строке*' + str(i)
                elif (a.count('.') > 1 or a.count('#') > 1 or a.count('-') > 1):
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Слишком много знаков для аргумента*' + str(i)
                elif a.count('-') != 0 and a[1:][0] != '-' :
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Знак минус стоит не на месте*' + str(i)
                elif a.count('#') != 0 and a[1:][0] != '#' :
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Значек # стоит не на месте*' + str(i)
                elif a[0] == 'G' and a not in allow_Gfunc:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Недопустимая G функция*' + str(i)
                elif a == 'G41':
                    self.milling_mode = 'G41'
                elif a[0] == 'M' and a not in allow_M:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Недопустимая M функция*' + str(i)
                elif a[0] == 'F':
                    if a[1] == '#' and a[1:] in self.param:
                        if float(self.param[a[1:]]) > 5000:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Слишком высокая подача F > 5000*' + str(i)
                        elif float(self.param[a[1:]]) < 10:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Слишком медленная подача F < 10*' + str(i)                            
                    elif a[1] == '#' and a[1:] not in self.param:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Значение ' + a[1:] + ' для F не определено в этом кадре*' + str(i)                      
                    elif float(a[1:]) > 5000:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Слишком высокая подача F > 5000*' + str(i)
                    elif float(a[1:]) < 10:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Слишком медленная подача F < 10*' + str(i)
                elif a[0] == 'S':
                    if a[1] == '#' and a[1:] in self.param:
                        if float(self.param[a[1:]]) > 30000:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Слишком высокие обороты S! Отправиш шпиндель в мульду*' + str(i)                        
                        elif float(self.param[a[1:]]) < 10:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Слишком маленькие обороты S!*' + str(i)                        
                    elif a[1] == '#' and a[1:] not in self.param:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Значение данного номера # для S не определено в этом кадре*' + str(i)                      
                    elif float(a[1:]) > 30000:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Слишком высокие обороты S! Отправиш шпиндель в мульду*' + str(i)
                    elif float(a[1:]) < 10:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Слишком маленькиее обороты S!*' + str(i)
                elif a[0] == 'T':
                    if float(a[1:]) > 60 or float(a[1:]) < 1 :
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Номер инструмента вне диапазона магазина BUMOTEC 1<T<60*' + str(i)                        
        if '(' in stroka:
            if stroka.count('(') != stroka.count(')'):
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Внутри строки присутствуют незакрыте скобки*' + str(i)
            else:
                stroka1 = stroka.partition('(')[0]
                stroka2 = stroka.partition(')')[2]
                stroka3 = stroka1 + stroka2
                if (stroka3.count('X') > 1 or stroka3.count('Y') > 1
                    or stroka3.count('Z') > 1 or stroka3.count('R') > 1
                    or stroka3.count('F') > 1 or stroka3.count('N') > 1
                    or stroka3.count('T') > 1 or stroka3.count('H') > 1
                    or stroka3.count('B') > 1 or stroka3.count('S') > 1
                    or stroka3.count('A') > 1 or stroka3.count('B') > 1
                    or stroka3.count('I') > 1 or stroka3.count('J') > 1
                    or stroka3.count('V') > 1 or stroka3.count('W') > 1
                    or stroka3.count('K') > 1 or stroka3.count('E') > 1
                    or stroka3.count('U') > 1 or stroka3.count('Q') > 1
                    or stroka3.count('P') > 1 or stroka3.count('D') > 1
                    or stroka3.count('C') > 1):
                    povt_arg = 'XZFTBAIVKUPCYRNHSBJWEQD'
                    double_arg = ''
                    for k in povt_arg:
                        if stroka3.count(k) > 1:
                            double_arg = k        
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Повторяющийся аргумент ' + double_arg + ' в строке*' + str(i)
        elif stroka[0] != '#' and stroka[0] != 'I':
            if (stroka.count('X') > 1 or stroka.count('Y') > 1
                or stroka.count('Z') > 1 or stroka.count('R') > 1
                or stroka.count('F') > 1 or stroka.count('N') > 1
                or stroka.count('T') > 1 or stroka.count('H') > 1
                or stroka.count('B') > 1 or stroka.count('S') > 1
                or stroka.count('A') > 1 or stroka.count('B') > 1
                or stroka.count('I') > 1 or stroka.count('J') > 1
                or stroka.count('V') > 1 or stroka.count('W') > 1
                or stroka.count('K') > 1 or stroka.count('E') > 1
                or stroka.count('U') > 1 or stroka.count('Q') > 1
                or stroka.count('P') > 1 or stroka.count('D') > 1
                or stroka.count('C') > 1):
                povt_arg = 'XZFTBAIVKUPCYRNHSBJWEQD'
                double_arg = ''
                for k in povt_arg:
                    if stroka.count(k) > 1:
                        double_arg = k        
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Повторяющийся аргумент ' + double_arg + ' в строке*' + str(i)                
        return self.rude_mistakes        



    # Check string with # from GOTO_milling
    def check_IFstroka(self,stroka,num):
        numbers = '0123456789'
        if len(stroka) < 14:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Ошибки в строке с IF GOTO*' + str(num)
        else:
            if stroka[:4] != 'IF[#':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Неправильные символы в строке с IF GOTO*' + str(num)
            else:
                i = 4
                j = 4
                par = ''
                while i < len(stroka):
                    if stroka[i] in numbers:
                        par = par + stroka[i]
                    else:
                        j = i
                        i = len(stroka)
                    i += 1
                if par == '' :
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Нет имени # параметра в строке с IF GOTO*' + str(num)
                else:
                    par = '#' + par
                    if par not in self.param:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Параметр' + par + ' не задан предварительно для строки IF GOTO*' + str(num)
                if j + 7 >= len(stroka):
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Ошибки в строке с IF GOTO*' + str(num)
                else:
                    if stroka[j:(j+8)] != 'GT0]GOTO':
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Ошибки в строке с IF GOTO*' + str(num)
                    else:
                        j = j + 8
                        chislo = ''
                        while j < len(stroka):
                            if stroka[j] in numbers:
                                chislo = chislo + stroka[j]
                            else:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Неправильные символы в строке IF GOTO*' + str(num)
                                j = len(stroka)
                            j += 1
                        if chislo == '':
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Нет номера кадра для перехода GOTO*' + str(num)
        return None
                



    # Check string with # from GOTO_milling
    def check_parGOTO(self,stroka,num):
        numbers = '0123456789'
        numbers_2 = '0123456789.-'
        marker_total = self.rude_mistakes['total']
        if stroka.count('#') == 1:
            par = '#'
            j = 1
            while j < len(stroka):
                if stroka[j] in numbers:
                    par = par + stroka[j]
                elif stroka[j] == '=':
                    i = j + 1
                    j = len(stroka)
                    mean_par = ''
                    while i < len(stroka):
                        if stroka[i] in numbers_2:
                            mean_par = mean_par + stroka[i]
                        elif stroka[i] == '(' and stroka[len(stroka)-1] == ')':
                            i = len(stroka)
                        else:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Неправильный символ ' + stroka[i] + ' в значении присвоения параметра*' + str(num)
                            i = len(stroka)                            
                        i += 1
                    if mean_par.replace('-','').replace('.','') == '' :
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Неопределено значение для параметра*' + str(num)
                    if mean_par.count('.') > 1:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Слишком много точек в значении параметра*' + str(num)
                    if mean_par.count('-') > 1:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Знак "-" (минус) повторяется в значении параметра*' + str(num)
                    if mean_par.count('-') == 1 and len(mean_par) > 0 and mean_par[0] != '-':
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Знак "-" (минус) стоит не на месте*' + str(num)
                else:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Неправильный символ ' + stroka[j] + ' в имени параметра*' + str(num)
                    j = len(stroka)
                j += 1
            if par == '#' or par == '#0':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пустой параметр*' + str(num)
            if '=' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Параметру ' + par + ' не присваивается значение*' + str(num)
            if marker_total == self.rude_mistakes['total']:
                self.param_readerGOTO(stroka)
        elif stroka.count('#') == 2:
            par1 = '#'
            j = 1
            while j < len(stroka):
                if stroka[j] in numbers:
                    par1 = par1 + stroka[j]
                elif stroka[j] == '=':
                    i = j + 2
                    j = len(stroka)
                    par2 = '#'
                    if i >= len(stroka):
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Нет имени второго параметра*' + str(num)
                    if stroka[i - 1] != '#':
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Второй параметр должен стоять после знака "=" (равно)*' + str(num)
                        i = len(stroka)
                    while i < len(stroka):
                        if stroka[i] in numbers:
                            par2 = par2 + stroka[i]
                        elif stroka[i] == '(' and stroka[len(stroka)-1] == ')':
                            i = len(stroka)
                        elif stroka[i] == '(':
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Незакрытые скобки*' + str(num)
                            i = len(stroka)
                        else:
                            k = i + 1
                            if stroka[i] != '-' and stroka[i] != '+':
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Неправильный символ ' + stroka[i] + ' после второго параметра*' + str(num)
                                k = len(stroka)
                            i = len(stroka)
                            chislo = ''
                            while k < len(stroka):
                                if stroka[k] == '(' and stroka[len(stroka)-1] == ')':
                                    k = len(stroka)
                                elif stroka[k] not in numbers_2:
                                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                    mis = self.rude_mistakes['total']
                                    self.rude_mistakes[mis] = 'Неправильный символ ' + stroka[k] + ' в строке*' + str(num)
                                    k = len(stroka)
                                else:
                                    chislo = chislo + stroka[k]
                                k += 1
                            if chislo.replace('-','').replace('.','') == '':
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Нет значения после знака*' + str(num)
                            if chislo.count('.') > 1:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Слишком много точек в числе*' + str(num)
                            if chislo.count('-') > 0:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Знак "-" минус стоит не на месте*' + str(num)
                        i += 1
                else:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Неправильный символ ' + stroka[j] + ' в имени параметра*' + str(num)
                    j = len(stroka)
                j += 1
            if par1 == '#' or par1 == '#0':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пустой параметр*' + str(num)
            if '=' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Параметру ' + par1 + ' не присваивается значение*' + str(num)
            if par1 not in self.param:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Параметр ' + par1 + ' не задан предварительно в кадре*' + str(num)
        elif stroka.count('#') > 2:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Количество # параметров больше двух в строке. Программа DANI не может провести анализ*' + str(num)
        return None

               
    

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


    # Read parametrs from line
    def param_reader(self, stroka, num):
        numbers1 = '0123456789'
        numbers2 = '-.0123456789'
        par = '#'
        par_mean = ''
        i = 1
        j = len(stroka)
        mis_in_begin = self.rude_mistakes['total']
        while (i != '=' and i < len(stroka)):
            if stroka[i] in numbers1:
                par = par + stroka[i]
                i += 1
            elif stroka[i] == '=':
                self.param[par] = ''
                j = i + 1
                i = len(stroka)
            else:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Неправильные символы в имени параметра*' + str(num)
                i = len(stroka)
                j = len(stroka)
        if par == '#0' or par == '#':
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Пустое имя параметра*' + str(num)            
        if '=' not in stroka:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Пустой параметр*' + str(num)
        else:
            while j < len(stroka):
                if stroka[j] in numbers2:
                    par_mean = par_mean + stroka[j]
                elif stroka[j] == '(':
                    j = len(stroka)
                else:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Недопустимые символы в значении параметра*' + str(num)
                    j = len(stroka)
                j += 1
            if self.rude_mistakes['total'] == mis_in_begin:
                if len(par_mean.replace('-','').replace('.','')) == 0:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Нет значения для параметра*' + str(num)                    
                elif par_mean.count('.') > 1 or par_mean.count('-') > 1:
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Повторяющиеся знаки*' + str(num)
                elif par_mean.count('-') == 1 and par_mean[0] != '-':
                    self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                    mis = self.rude_mistakes['total']
                    self.rude_mistakes[mis] = 'Знак минус не на месте*' + str(num)                    
                else:
                    if par_mean != '' and mis_in_begin == self.rude_mistakes['total']:
                        self.param[par] = float(par_mean)
        if par in self.param and self.param[par] == '':
            del self.param[par]
        return None


    # Read parametrs from milling with GOTO
    def param_readerGOTO(self, stroka):
        numbers1 = '0123456789'
        numbers2 = '-.0123456789'
        par = stroka.partition('=')[0]
        mean_par = ''
        expres_par = stroka.partition('=')[2]
        i = 0
        while i < len(expres_par):
            if expres_par[i] in numbers2:
                mean_par = mean_par + expres_par[i]
            else:
                i = len(expres_par)
            i += 1
        self.param[par] = float(mean_par)
        return None
    

    # Check rude mistakes in Ren_150 measure program
    def mis_in_Ren150(self):
        allow_M = ('M0','M00','M30','%')
        allow_Gfunc = ('G65')
        allow_ren150 = ('P151','P150','P159')
        allow_letters = 'XYZCSBVWIJGMP'
        numbers = '0123456789.-'
        mark_slesh = 0
        i = 0
        while i < len(self.Myblock):
            if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%' and self.Myblock[i][0] != 'N' and self.Myblock[i][0] != ' ':
                self.Myblock[i] = self.Myblock[i].rstrip('\n')
                self.Myblock[i] = self.Myblock[i].replace(' ','')
                if self.Myblock[i][0] == '/':
                    mark_slesh = 1
                self.Myblock[i] = self.Myblock[i].lstrip('/')
                self.first_check(self.Myblock[i], allow_M, allow_Gfunc, allow_letters, numbers, i)
                self.Myblock[i] = self.Myblock[i] + '\n'
                if mark_slesh == 1:
                    self.Myblock[i] = '/' + self.Myblock[i]
                    mark_slesh = 0                
            i += 1
        if self.rude_mistakes['total'] == 0:
            kol_P150 = 0
            kol_P159 = 0
            i = 0
            while i < len(self.Myblock):
                if len(self.Myblock[i]) > 7 and 'G65P150' in self.Myblock[i] and self.Myblock[i][0] != '(':
                    kol_P150 += 1
                    if kol_P150 > 1:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Повторение подпрограммы P150. В одном блоке может быть только одна стартовая P150*'+ str(i)
                elif len(self.Myblock[i]) > 7 and 'G65P159' in self.Myblock[i] and self.Myblock[i][0] != '(':
                    kol_P159 += 1
                    if kol_P159 > 1:
                        self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                        mis = self.rude_mistakes['total']
                        self.rude_mistakes[mis] = 'Повторение P159. Подпрограмма P159 может быть только одна и ставится после всех измерений*'+ str(i)
                i += 1
            if kol_P159 == 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Отсутсвует G65P159 после циклов промерки*' + str(i)            
        if self.rude_mistakes['total'] == 0:
            i = 0
            old_P = ''
            now_P = ''
            all_arg = {}
            Bezopas_level = -100
            amount_of_P151 = 0
            switch_IJ = 0            
            while i < len(self.Myblock):
                if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%' and self.Myblock[i][0] != 'N':
                    if self.Myblock[i][0] == '/':
                        mark_slesh = 1
                    self.Myblock[i] = self.Myblock[i].lstrip('/')                    
                    arg_loop = self.arg_read(self.Myblock[i])
                    for j in arg_loop:
                        if 'G' in j[0] and self.Myblock[i].count(j) > 1:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Повторение функции '+j+'*'+ str(i)
                        if 'P' in j[0] and j not in allow_ren150:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Вызов неизвестной измерительной подпрограммы '+j+'*'+ str(i)
                        all_arg[j[0]] = float(j[1:])
                    old_P = now_P
                    if self.rude_mistakes['total'] == 0:
                        if 'P150' in arg_loop:
                            queue = 2
                            now_P = 'P150'
                            if 'P150' not in self.loops_names:
                                self.loops_names.append('P150')
                            if old_P != now_P:
                                queue = 1
                            Bezopas_level = self.P150_check(self.Myblock[i],all_arg,queue,i,arg_loop,Bezopas_level)
                        if 'P151' in arg_loop:
                            queue = 2
                            now_P = 'P151'
                            if 'P151' not in self.loops_names:
                                self.loops_names.append('P151')
                            if old_P != now_P:
                                queue = 1
                            switch_IJ = self.P151_check(self.Myblock[i],all_arg,queue,i,arg_loop,Bezopas_level,switch_IJ)
                            amount_of_P151 += switch_IJ
                            if amount_of_P151 > 14:
                                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                                mis = self.rude_mistakes['total']
                                self.rude_mistakes[mis] = 'Слишком много измерений в одном блоке. Максимум может быть 14 для BUMOTEC. Разбей этот блок на два блока*' + str(i)
                        if 'P159' in arg_loop:
                            queue = 2
                            now_P = 'P159'
                            if 'P159' not in self.loops_names:
                                self.loops_names.append('P159')
                            if old_P != now_P:
                                queue = 1
                            self.P159_check(arg_loop)
                    if mark_slesh == 1:
                        self.Myblock[i] = '/' + self.Myblock[i]
                        mark_slesh = 0                    
                i += 1
        return self.rude_mistakes



    # Check rude mistakes in Ren_150 measure program
    def mis_in_Ren200(self):
        allow_M = ('M0','M00','M30')
        allow_Gfunc = ('G65')
        allow_ren150 = ('P200','P201','P203','P208')
        allow_letters = 'ABXYVWIJGMPCDZ'
        numbers = '0123456789.-'
        mark_slesh = 0
        i = 0
        while i < len(self.Myblock):
            if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%' and self.Myblock[i][0] != 'N' and self.Myblock[i][0] != ' ':
                self.Myblock[i] = self.Myblock[i].rstrip('\n')
                self.Myblock[i] = self.Myblock[i].replace(' ','')
                if self.Myblock[i][0] == '/':
                    mark_slesh = 1
                self.Myblock[i] = self.Myblock[i].lstrip('/')
                self.first_check(self.Myblock[i], allow_M, allow_Gfunc, allow_letters, numbers, i)
                self.Myblock[i] = self.Myblock[i] + '\n'
                if mark_slesh == 1:
                    self.Myblock[i] = '/' + self.Myblock[i]
                    mark_slesh = 0                
            i += 1
        if self.rude_mistakes['total'] == 0:
            i = 0
            old_P = ''
            now_P = ''
            all_arg = {}
            while i < len(self.Myblock):
                if self.Myblock[i][0] != '(' and self.Myblock[i][0] != '\n' and self.Myblock[i][0] != '%' and self.Myblock[i][0] != 'N' and self.Myblock[i][0] != ' ':
                    if self.Myblock[i][0] == '/':
                        mark_slesh = 1
                    self.Myblock[i] = self.Myblock[i].lstrip('/')                    
                    arg_loop = self.arg_read(self.Myblock[i])
                    for j in arg_loop:
                        if 'G' in j[0] and self.Myblock[i].count(j) > 1:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Повторение функции '+j+'*'+ str(i)
                        if 'P' in j[0] and j not in allow_ren150:
                            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                            mis = self.rude_mistakes['total']
                            self.rude_mistakes[mis] = 'Вызов неизвестной измерительной подпрограммы '+j+'*'+ str(i)
                        all_arg[j[0]] = float(j[1:])
                    old_P = now_P
                    if self.rude_mistakes['total'] == 0:
                        if 'P200' in arg_loop:
                            now_P = 'P200'
                            if 'P200' not in self.loops_names:
                                self.loops_names.append('P200')
                            if old_P != now_P:
                                queue = 1
                            self.P200_check(self.Myblock[i],all_arg,queue,i,arg_loop)
                        if 'P201' in arg_loop:
                            queue = 2
                            now_P = 'P201'
                            if 'P201' not in self.loops_names:
                                self.loops_names.append('P201')
                            if old_P != now_P:
                                queue = 1
                            self.P201_check(self.Myblock[i],all_arg,queue,i,arg_loop)
                        if 'P203' in arg_loop:
                            queue = 2
                            now_P = 'P203'
                            if 'P203' not in self.loops_names:
                                self.loops_names.append('P203')
                            if old_P != now_P:
                                queue = 1
                            self.P203_check(self.Myblock[i],all_arg,queue,i,arg_loop)
                        if 'P208' in arg_loop:
                            queue = 2
                            now_P = 'P208'
                            if 'P208' not in self.loops_names:
                                self.loops_names.append('P208')
                            if old_P != now_P:
                                queue = 1
                            self.P208_check(self.Myblock[i],all_arg,queue,i,arg_loop)                            
                    if mark_slesh == 1:
                        self.Myblock[i] = '/' + self.Myblock[i]
                        mark_slesh = 0                    
                i += 1
        return self.rude_mistakes



    #Check P200 measure programm
    def P200_check(self, stroka, arguments, queue, i, arg_loop):
        for j in arg_loop:
            if j[0] not in 'GPIJZC':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список допустимых аргументов P200*' + str(i)
        if 'C' in stroka and arguments['C'] < -360:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
        elif 'C' in stroka and arguments['C'] > 360:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
        return None



    #Check P201 measure programm
    def P201_check(self, stroka, arguments, queue, i, arg_loop):
        for j in arg_loop:
            if j[0] not in 'GPXYABVWIJC':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список допустимых аргументов P201*' + str(i)
        if 'C' in stroka and arguments['C'] < -360:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
        elif 'C' in stroka and arguments['C'] > 360:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
        if 'A' in stroka or 'B' in stroka:
            if 'A' in stroka and arguments['A'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Длинна фланца A должна быть задана положительным числом*'+ str(i)
            if 'B' in stroka and arguments['B'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Ширина фланца B должна быть задана положительным числом*'+ str(i)                
            if 'V' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил безопасный уровень V при измерении величин AB фланца в P201*'+ str(i)
            if 'W' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил уровень измерений W в P201*'+ str(i)
            if 'V' in stroka and 'W' in stroka and arguments['W'] >= arguments['V']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня касания W в P201*'+ str(i)
        if 'A' not in stroka and 'B' not in stroka:
            if 'V' in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V - лишний аргумент, если не измеряешь величины B или A в P201*'+ str(i)
            if 'W' in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Уровень касания W - лишний аргумент, если не измеряешь величины B или A в P201*'+ str(i)
        if 'I' in stroka and 'J' in stroka:
            I_pos = stroka.index('I')
            J_pos = stroka.index('J')
            if J_pos < I_pos:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент I должен стоять перед аргументом J в P201*'+ str(i)
        return None
    


    #Check P203 measure programm
    def P203_check(self, stroka, arguments, queue, i, arg_loop):
        for j in arg_loop:
            if j[0] not in 'GPXYVWIJCD':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список допустимых аргументов P203*' + str(i)
        if 'C' in stroka and arguments['C'] < -360:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
        elif 'C' in stroka and arguments['C'] > 360:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
        if 'V' not in stroka:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Пропустил безопасный уровень V в P203*'+ str(i)
        if 'W' not in stroka:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Пропустил уровень измерений W в P203*'+ str(i)
        if 'V' in stroka and 'W' in stroka and arguments['W'] >= arguments['V']:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня касания W в P203*'+ str(i)
        if 'D' not in stroka:
            self.warning_m['total'] = self.warning_m['total'] + 1
            mis = self.warning_m['total']
            self.warning_m[mis] = 'Не задан диаметр промеряемого отверстия. По умолчанию будет установлен D=50 в P203*'+ str(i)
        if 'I' in stroka and 'J' in stroka:
            I_pos = stroka.index('I')
            J_pos = stroka.index('J')
            if J_pos < I_pos:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент I должен стоять перед аргументом J в P203*'+ str(i)
        return None



    #Check P208 measure programm
    def P208_check(self, stroka, arguments, queue, i, arg_loop):
        for j in arg_loop:
            if j[0] not in 'GPXYVWIJCAB':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список допустимых аргументов P208*' + str(i)
        if 'C' in stroka and arguments['C'] < -360:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
        elif 'C' in stroka and arguments['C'] > 360:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
        if 'A' in stroka and arguments['A'] <= 0:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Длинна паза A должна быть задана положительным числом*'+ str(i)
        if 'B' in stroka and arguments['B'] <= 0:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Ширина паза B должна быть задана положительным числом*'+ str(i)                
        if 'V' not in stroka:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Пропустил безопасный уровень V в P208*'+ str(i)
        if 'W' not in stroka:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Пропустил уровень измерений W в P208*'+ str(i)
        if 'V' in stroka and 'W' in stroka and arguments['W'] >= arguments['V']:
            self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
            mis = self.rude_mistakes['total']
            self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня касания W в P208*'+ str(i)
        if 'I' in stroka and 'J' in stroka:
            I_pos = stroka.index('I')
            J_pos = stroka.index('J')
            if J_pos < I_pos:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент I должен стоять перед аргументом J в P208*'+ str(i)
        return None    

    

    #Check P150 measure programm
    def P150_check(self, stroka, arguments, queue, i, arg_loop, Bezopas_level):
        for j in arg_loop:
            if j[0] not in 'GPXYZCSB':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список допустимых аргументов стартовой измерительной P150*' + str(i)
        if queue == 1:
            if 'X' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент X при задании P150*'+ str(i)
            if 'Y' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Y при задании P150*'+ str(i)
            if 'Z' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Z при задании P150*'+ str(i)
            if 'C' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент C (поворот стола) при задании P150*'+ str(i)
            elif 'C' in stroka and arguments['C'] < -360:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
            elif 'C' in stroka and arguments['C'] > 360:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Угол поворота стола должен быть в диапазоне -360<=C<=360 градусов*'+ str(i)
            if 'S' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент S (страница параметров) при задании P150*'+ str(i)
            elif 'S' in stroka and arguments['S'] != 1 and arguments['S'] != 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент S (страница параметров) может быть задан либо S=1 либо S=2 для BUMOTEC*'+ str(i)
            if 'B' not in stroka:
                self.warning_m['total'] = self.warning_m['total'] + 1
                mis = self.warning_m['total']
                self.warning_m[mis] = 'Пропущен аргумент B (угол поворота головы) при задании P150. По умолчанию P150 установит B=0*'+ str(i)
            elif 'B' in stroka and arguments['B'] < -25:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент B (угол поворота головы) должен быть в диапазоне -25<=B<=115 градусов**'+ str(i)
            elif 'B' in stroka and arguments['B'] > 115:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент B (угол поворота головы) должен быть в диапазоне -25<=B<=115 градусов**'+ str(i)
            if  'Z' in stroka:
                Bezopas_level = arguments['Z']
        return Bezopas_level


    #Check P151 measure programm
    def P151_check(self, stroka, arguments, queue, i, arg_loop, Bezopas_level,switch_IJ):
        for j in arg_loop:
            if j[0] not in 'GPXYVWIJ':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список допустимых аргументов для P151*' + str(i)
        possible_I = (1,2,3,4,5,6,7,8,9,10,11,12,13,14)                
        if queue == 1:
            if 'X' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент X при первом задании P151*'+ str(i)
            if 'Y' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Y при первом задании P151*'+ str(i)
            if 'V' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент V (безопасный уровень) при первом задании P151*'+ str(i)
            if 'W' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент W (уровень касания щупа) при первом задании P151*'+ str(i)
            if 'V' in stroka and arguments['V'] >= Bezopas_level:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V в P151 не должен быть выше уровня Z стартовой P150*'+ str(i)
            if 'W' in stroka and arguments['W'] >= Bezopas_level:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Уровень касания щупа W в P151 не должен быть выше уровня Z стартовой P150*'+ str(i)
            if 'V' in stroka and 'W' in stroka and arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня касания щупа W для P151*'+ str(i)
            if 'I' not in stroka and 'J' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Отсутсвует аргумент I или J при первом задании P151*'+ str(i)
            elif 'I' in stroka and arguments['I'] not in possible_I:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Aргумент I может быть задан только целым числом в диапазоне 1<=I<=14 для P151*'+ str(i)
            elif 'J' in stroka and arguments['J'] not in possible_I:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Aргумент J может быть задан только целым числом в диапазоне 1<=J<=14 для P151*'+ str(i)
            if 'I' in stroka and 'J' in stroka :
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Нельзя одновременно задавать аргумент I и аргумент J в одной P151*'+ str(i)
        else:
            if 'V' in arguments and 'W' in arguments and arguments['W'] >= arguments['V']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня касания щупа W для P151*'+ str(i)
            if 'V' in arguments and arguments['V'] >= Bezopas_level:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V в P151 должен быть ниже уровня Z стартовой P150*'+ str(i)
            if 'W' in arguments and arguments['W'] >= Bezopas_level:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Уровень касания щупа W должен быть ниже уровня Z стартовой P150*'+ str(i)
            if 'I' in stroka and arguments['I'] not in possible_I:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Aргумент I может быть задан только целым числом в диапазоне 1<=I<=14 для P151*'+ str(i)
            elif 'J' in stroka and arguments['J'] not in possible_I:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Aргумент J может быть задан только целым числом в диапазоне 1<=J<=14 для P151*'+ str(i)
            if 'I' in stroka and 'J' in stroka :
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Нельзя одновременно задавать аргумент I и аргумент J в одной P151*'+ str(i)
            if 'J' in stroka:
                switch_IJ = 1
            elif 'I' in stroka:
                switch_IJ = 0
        return switch_IJ


    #Check P159 measure programm
    def P159_check(self, arg_loop):
        for j in arg_loop:
            if j[0] not in 'GP':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'В подпрограмме G65P159 не должно присутствовать никаких аргументов для BUMOTEC*' + str(i)
        return None


    #Check P43 arguments
    def P43_check(self,stroka,arguments,queue,i,Rad_f,arg_loop):
        all_p43arguments = arguments
        for j in arg_loop:
            if j[0] not in 'GPXYVZWDQUF':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список аргументов макропрограммы P43*' + str(i)
        if queue == 1:
            if 'X' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент X при первом задании P43*'+ str(i)
            if 'Y' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Y при первом задании P43*'+ str(i)
            if 'V' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент V при первом задании P43*'+ str(i)
            if 'Z' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Z при первом задании P43*'+ str(i)
            if 'W' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент W при первом задании P43*'+ str(i)
            if 'Z' in stroka and 'W' in stroka and arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P43!*'+ str(i)
            if 'V' in stroka and 'Z' in stroka and arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала расточки Z в P43!*'+ str(i)
            if 'V' in stroka and 'W' in stroka and arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P43!*'+ str(i)
            if 'D' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент D при первом задании P43*'+ str(i)
            elif 'D' in stroka and arguments['D'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Диаметр отверстия D должен быть положительным числом*'+ str(i)
            if 'D' in stroka and arguments['D'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Диаметр фрезы слишком большой для расточки отверстия в P43*'+ str(i)                            
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P43*'+ str(i)
            if 'Q' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропущено значение Q при первом вызове P43*'+ str(i)
                all_p43arguments['Q'] = 0.1
            elif 'Q' in stroka and arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q должен быть положительным числом!*'+ str(i)
            if 'F' not in stroka:
                self.warning_m['total'] = self.warning_m['total'] + 1
                mis = self.warning_m['total']
                self.warning_m[mis] = 'Пропущено значение F при первом вызове P43. По умолчанию P43 установит F=150*'+ str(i)
        else:
            if arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P43!*'+ str(i)
            if arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала расточки Z в P43!*'+ str(i)
            if arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P43!*'+ str(i)
            if arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q должен быть положительным числом!*'+ str(i)
            if arguments['D'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Диаметр отверстия D должен быть положительным числом*'+ str(i)
            if  arguments['D'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Диаметр фрезы слишком большой для расточки отверстия в P43*'+ str(i)                                            
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P43*'+ str(i)
        return all_p43arguments


    #Check P80 arguments
    def P80_check(self,stroka,arguments,queue,i,arg_loop):
        for j in arg_loop:
            if j[0] not in 'GPABXYVZWEFJUQ':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список аргументов макропрограммы P80*' + str(i)        
        if queue == 1:
            if 'X' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент X при первом задании P80*'+ str(i)
            if 'Y' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Y при первом задании P80*'+ str(i)
            if 'V' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент V при первом задании P80*'+ str(i)
            if 'Z' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Z при первом задании P80*'+ str(i)
            if 'W' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент W при первом задании P80*'+ str(i)
            if 'Z' in stroka and 'W' in stroka and arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P80!*'+ str(i)
            if 'V' in stroka and 'Z' in stroka and arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала циковки Z в P80!*'+ str(i)
            if 'V' in stroka and 'W' in stroka and arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P80!*'+ str(i)                
            if 'A' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент A при первом задании P80*'+ str(i)
            elif 'A' in stroka and arguments['A'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Длинна рамки A должна быть задана положительным числом*'+ str(i)
            if 'B' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент B при первом задании P80*'+ str(i)
            elif 'B' in stroka and arguments['B'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Ширина рамки B должна быть задана положительным числом*'+ str(i)                
            if 'Q' not in stroka and 'U' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Q при первом задании P80*'+ str(i)
            elif 'Q' in stroka and arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q за один проход должен быть задан положительным числом*'+ str(i)
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P80*'+ str(i)
            if 'J' in stroka and arguments['J'] != 2 and arguments['J'] != 1:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Тип движения фрезы на плоскости J может быть либо =1 либо =2 для P80*'+ str(i)
            if 'E' in stroka and (arguments['E'] <= 9 or arguments['E'] > 100):
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Процент перекрытия фрезы E должен быть в диапазоне 9<E<=100 для P80*'+ str(i)
            if 'F' not in stroka:
                self.warning_m['total'] = self.warning_m['total'] + 1
                mis = self.warning_m['total']
                self.warning_m[mis] = 'Пропущено значение F при первом вызове P80. По умолчанию P80 установит F=1000*'+ str(i)
        else:
            if arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P80!*'+ str(i)
            if arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала циковки Z в P80!*'+ str(i)
            if arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P80!*'+ str(i)
            if arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q должен быть положительным числом!*'+ str(i)
            if arguments['A'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Длинна рамки A должна быть задана положительным числом*'+ str(i)
            if arguments['B'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Ширина рамки B должна быть задана положительным числом*'+ str(i)
            if 'J' in stroka and arguments['J'] != 2 and arguments['J'] != 1:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Тип движения фрезы на плоскости J может быть либо =1 либо =2 для P80*'+ str(i)
            if 'E' in stroka and (arguments['E'] <= 9 or arguments['E'] > 100):
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Процент перекрытия фрезы E должен быть в диапазоне 9<E<=100 для P80*'+ str(i)
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P80*'+ str(i)
        return None   


    #Check P64 arguments
    def P64_check(self,stroka,arguments,queue,i,arg_loop):
        for j in arg_loop:
            if j[0] not in 'GPIJABXYVZWERFKUQ':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список аргументов макропрограммы P64*' + str(i)
        if queue == 1:
            if 'X' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент X при первом задании P64*'+ str(i)
            if 'Y' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Y при первом задании P64*'+ str(i)
            if 'V' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент V при первом задании P64*'+ str(i)
            if 'Z' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Z при первом задании P64*'+ str(i)
            if 'W' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент W при первом задании P64*'+ str(i)
            if 'Z' in stroka and 'W' in stroka and arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P64!*'+ str(i)
            if 'V' in stroka and 'Z' in stroka and arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала циковки Z в P64!*'+ str(i)
            if 'V' in stroka and 'W' in stroka and arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P64!*'+ str(i)                
            if 'A' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент A при первом задании P64*'+ str(i)
            elif 'A' in stroka and arguments['A'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Длинна фланца A должна быть задана положительным числом*'+ str(i)
            if 'B' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент B при первом задании P64*'+ str(i)
            elif 'B' in stroka and arguments['B'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Ширина фланца B должна быть задана положительным числом*'+ str(i)                
            if 'Q' not in stroka and 'U' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Q при первом задании P64*'+ str(i)
            elif 'Q' in stroka and arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q за один проход должен быть задан положительным числом*'+ str(i)
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P64*'+ str(i)
            if 'J' in stroka and arguments['J'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Начальный размер фланца J должен быть задан положительным числом в P64*'+ str(i)
            if 'I' in stroka and arguments['I'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Начальный размер фланца I должен быть задан положительным числом в P64*'+ str(i)
            if 'J' in stroka and 'B' in stroka and arguments['J'] <= arguments['B']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Начальный размер J должен быть больше конечного размера B для P64*'+ str(i)
            if 'I' in stroka and 'A' in stroka and arguments['I'] <= arguments['A']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Начальный размер I должен быть больше конечного размера A для P64*'+ str(i)
            if 'K' in stroka and arguments['K'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Расстояние бокового подхода K до фланца должно быть задано положительным числом в P64*'+ str(i)
            if 'E' in stroka and arguments['E'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Фаски E должны быть заданы положительным числом в P64*'+ str(i)
            if 'R' in stroka and arguments['R'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Радиуса на углах фланца R должны задаваться положительным числом в P64*'+ str(i)
            if 'R' in stroka and 'E' in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Нельзя одновременно задавать фаски E и радиуса в углах R для P64*'+ str(i)
            if 'F' not in stroka:
                self.warning_m['total'] = self.warning_m['total'] + 1
                mis = self.warning_m['total']
                self.warning_m[mis] = 'Пропущено значение F при первом вызове P64. По умолчанию P64 установит F=1000*'+ str(i)
        else:
            if arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P64!*'+ str(i)
            if arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала циковки Z в P64!*'+ str(i)
            if arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P64!*'+ str(i)
            if arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q должен быть положительным числом!*'+ str(i)
            if arguments['A'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Длинна фланца A должна быть задана положительным числом*'+ str(i)
            if arguments['B'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Ширина фланца B должна быть задана положительным числом*'+ str(i)
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P64*'+ str(i)
        return None


    #Check P47 arguments
    def P47_check(self,stroka,arguments,queue,i,Rad_f,arg_loop):
        for j in arg_loop:
            if j[0] not in 'GPXYDRVZWQFJ':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список аргументов макропрограммы P47*' + str(i)
        if queue == 1:
            if 'X' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент X при первом задании P47*'+ str(i)
            if 'Y' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Y при первом задании P47*'+ str(i)
            if 'V' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент V при первом задании P47*'+ str(i)
            if 'Z' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Z при первом задании P47*'+ str(i)
            if 'W' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент W при первом задании P47*'+ str(i)
            if 'Z' in stroka and 'W' in stroka and arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P47!*'+ str(i)
            if 'V' in stroka and 'Z' in stroka and arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала расточки Z в P47!*'+ str(i)
            if 'V' in stroka and 'W' in stroka and arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P47!*'+ str(i)
            if 'D' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент D (верхний диаметр конуса) при первом задании P47*'+ str(i)
            elif 'D' in stroka and arguments['D'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний диаметр конуса D должен быть положительным числом в P47*'+ str(i)
            if 'R' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент R (нижний диаметр конуса) при первом задании P47*'+ str(i)
            elif 'R' in stroka and arguments['R'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Нижний диаметр конуса R должен быть положительным числом в P47*'+ str(i)
            if 'R' in stroka and arguments['R'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Диаметр фрезы слишком большой для расточки конуса в P47*'+ str(i)            
            if 'D' in stroka and 'R' in stroka and arguments['D'] <= arguments['R']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний диаметр конуса D должен быть шире нижнего диаметра конуса R в P47*'+ str(i)                
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P47*'+ str(i)
            if 'Q' not in stroka:
                self.warning_m['total'] = self.warning_m['total'] + 1
                mis = self.warning_m['total']
                self.warning_m[mis] = 'Пропущено значение Q при первом вызове P47. По умолчанию P47 установит Q=0.01*'+ str(i)
            elif 'Q' in stroka and arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q должен быть положительным числом!*'+ str(i)
            if 'F' not in stroka:
                self.warning_m['total'] = self.warning_m['total'] + 1
                mis = self.warning_m['total']
                self.warning_m[mis] = 'Пропущено значение F при первом вызове P47. По умолчанию P47 установит F=500*'+ str(i)
            if 'J' not in stroka:
                self.warning_m['total'] = self.warning_m['total'] + 1
                mis = self.warning_m['total']
                self.warning_m[mis] = 'Пропущено J (направление спирали) при первом вызове P47. По умолчанию P47 установит J=1*'+ str(i)
            elif 'J' in stroka and arguments['J'] != 1 and arguments['J'] != 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Направление движения спирали может быть либо J=1 либо J=2 в P47*'+ str(i)                
        else:
            if arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P47!*'+ str(i)
            if arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала расточки Z в P47!*'+ str(i)
            if arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P47!*'+ str(i)
            if arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q должен быть положительным числом в P47!*'+ str(i)
            if arguments['D'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний диаметр конуса D должен быть положительным числом в P47*'+ str(i)
            if arguments['R'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Нижний диаметр конуса R должен быть положительным числом в P47*'+ str(i)
            if  arguments['R'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Диаметр фрезы слишком большой для расточки конуса в P47*'+ str(i)                 
            if arguments['D'] <= arguments['R']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний диаметр конуса D должен быть шире нижнего диаметра конуса R в P47!*'+ str(i)                
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P47*'+ str(i)
            if  arguments['J'] != 1 and arguments['J'] != 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Направление движения спирали может быть либо J=1 либо J=2 в P47*'+ str(i)
        return None


    #Check P62 arguments
    def P62_check(self,stroka,arguments,queue,i,Rad_f,arg_loop):
        for j in arg_loop:
            if j[0] not in 'GPABXYVZWRFIUQ':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список аргументов макропрограммы P62*' + str(i)
        if queue == 1:
            if 'X' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент X при первом задании P62*'+ str(i)
            if 'Y' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Y при первом задании P62*'+ str(i)
            if 'V' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент V при первом задании P62*'+ str(i)
            if 'Z' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Z при первом задании P62*'+ str(i)
            if 'W' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент W при первом задании P62*'+ str(i)
            if 'Z' in stroka and 'W' in stroka and arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P62!*'+ str(i)
            if 'V' in stroka and 'Z' in stroka and arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала циковки Z в P62!*'+ str(i)
            if 'V' in stroka and 'W' in stroka and arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P62!*'+ str(i)                
            if 'A' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент A при первом задании P62*'+ str(i)
            elif 'A' in stroka and arguments['A'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Длинна окна A должна быть задана положительным числом в P62*'+ str(i)
            if 'A' in stroka and arguments['A'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленькая длинна окна А для этого радиуса фрезы в P62*'+ str(i)
            if 'B' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент B при первом задании P62*'+ str(i)
            elif 'B' in stroka and arguments['B'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Ширина окна B должна быть задана положительным числом в P62*'+ str(i)
            if 'B' in stroka and arguments['B'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленькая ширина окна B для этого радиуса фрезы в P62*'+ str(i)                
            if 'Q' not in stroka and 'U' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Q при первом задании P62*'+ str(i)
            elif 'Q' in stroka and arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q за один проход должен быть задан положительным числом в P62*'+ str(i)
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P62*'+ str(i)
            if 'I' in stroka and arguments['I'] < 1:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленький процент снижения I для трехкоординатного врезания. Должен быть 1<I<100 для P62*'+ str(i)
            elif 'I' in stroka and arguments['I'] > 99:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком высокий процент снижения I для трехкоординатного врезания. Должен быть 1<I<100 для P62*'+ str(i)                
            if 'R' in stroka and arguments['R'] < Rad_f:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Радиуса R в углах окна не должны быть меньше радиуса фрезы для P62*'+ str(i)
            if 'F' not in stroka:
                self.warning_m['total'] = self.warning_m['total'] + 1
                mis = self.warning_m['total']
                self.warning_m[mis] = 'Пропущено значение F при первом вызове P62. По умолчанию P62 установит F=1000*'+ str(i)
        else:
            if arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P62!*'+ str(i)
            if arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала циковки Z в P62!*'+ str(i)
            if arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P62!*'+ str(i)
            if arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q должен быть положительным числом для P62*'+ str(i)
            if arguments['A'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Длинна окна A должна быть задана положительным числом для P62*'+ str(i)
            if arguments['A'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленькая длинна окна А для этого радиуса фрезы в P62*'+ str(i)                
            if arguments['B'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Ширина окна B должна быть задана положительным числом для P62*'+ str(i)
            if arguments['B'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленькая ширина окна B для этого радиуса фрезы в P62*'+ str(i)
            if 'I' in stroka and (arguments['I'] < 1 or arguments['I'] > 99):
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Некорректный процент снижения I для трехкоординатного врезания. Должен быть 1<I<100 для P62*'+ str(i)
            if 'R' in stroka and arguments['R'] < Rad_f:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Радиуса R в углах окна не должны быть меньше радиуса фрезы для P62*'+ str(i)
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P62*'+ str(i)
        return None    
  

    #Check P44 arguments
    def P44_check(self,stroka,arguments,i,Rad_f):
        if 'G66P44' in stroka:
            if 'Z' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Z при первом задании P44*'+ str(i)
            if 'W' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент W при первом задании P44*'+ str(i)
            if 'Z' in stroka and 'W' in stroka and arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P44!*'+ str(i)
            if 'V' in stroka and 'Z' in stroka and arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала расточки Z в P44!*'+ str(i)
            if 'V' in stroka and 'W' in stroka and arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P44!*'+ str(i)
            if 'M' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент M (тип резьбы) при первом задании P44*'+ str(i)
            elif 'M' in stroka and arguments['M'] <= Rad_f*2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком большой диаметр резьбовой фрезы. Аргумент M в P44 задан меньше!*'+ str(i)
        else:
            if arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P44!*'+ str(i)
        return None


    #Check P63 arguments
    def P63_check(self,stroka,arguments,queue,i,Rad_f,arg_loop):
        for j in arg_loop:
            if j[0] not in 'GPABXYVZWRFKUQ':
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Аргумент ' + j[0] +' не входит в список аргументов макропрограммы P63*' + str(i)
        if queue == 1:
            if 'X' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент X при первом задании P63*'+ str(i)
            if 'Y' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Y при первом задании P63*'+ str(i)
            if 'V' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент V при первом задании P63*'+ str(i)
            if 'Z' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Z при первом задании P63*'+ str(i)
            if 'W' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент W при первом задании P63*'+ str(i)
            if 'Z' in stroka and 'W' in stroka and arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P63!*'+ str(i)
            if 'V' in stroka and 'Z' in stroka and arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала циковки Z в P63!*'+ str(i)
            if 'V' in stroka and 'W' in stroka and arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P63!*'+ str(i)                
            if 'A' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент A при первом задании P63*'+ str(i)
            elif 'A' in stroka and arguments['A'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Длинна рамки A должна быть задана положительным числом в P63*'+ str(i)
            if 'A' in stroka and arguments['A'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленькая длинна рамки А для этого радиуса фрезы в P63*'+ str(i)
            if 'B' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент B при первом задании P63*'+ str(i)
            elif 'B' in stroka and arguments['B'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Ширина рамки B должна быть задана положительным числом в P63*'+ str(i)
            if 'B' in stroka and arguments['B'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленькая рамки B для этого радиуса фрезы в P63*'+ str(i)                
            if 'Q' not in stroka and 'U' not in stroka:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Пропустил аргумент Q при первом задании P63*'+ str(i)
            elif 'Q' in stroka and arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q за один проход должен быть задан положительным числом в P63*'+ str(i)
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P63*'+ str(i)
            if 'K' in stroka and arguments['K'] < 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Подход фрезы K до стенки паза должен быть задан положительным числом для P63*'+ str(i)
            elif 'K' in stroka and 'A' in stroka and (arguments['A'] <= Rad_f * 2 + arguments['K']):
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленькая длинна рамки A по отношению к подходу K и текущего радиуса фрезы в P63*'+ str(i) 
            if 'R' in stroka and arguments['R'] < Rad_f:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Радиуса R в углах рамки не должны быть меньше радиуса фрезы для P63*'+ str(i)
            if 'F' not in stroka:
                self.warning_m['total'] = self.warning_m['total'] + 1
                mis = self.warning_m['total']
                self.warning_m[mis] = 'Пропущено значение F при первом вызове P63. По умолчанию P63 установит F=1000*'+ str(i)
        else:
            if arguments['Z'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Верхний уровень Z должен быть выше нижнего W в P63!*'+ str(i)
            if arguments['V'] <= arguments['Z']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше уровня начала циковки Z в P63!*'+ str(i)
            if arguments['V'] <= arguments['W']:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Безопасный уровень V должен быть выше нижней границы W в P63!*'+ str(i)
            if arguments['Q'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Съем Q должен быть положительным числом для P63*'+ str(i)
            if arguments['A'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Длинна рамки A должна быть задана положительным числом для P63*'+ str(i)
            if arguments['A'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленькая длинна рамки А для этого радиуса фрезы в P63*'+ str(i)                
            if arguments['B'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Ширина рамки B должна быть задана положительным числом для P63*'+ str(i)
            if arguments['B'] <= Rad_f * 2:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Слишком маленькая ширина рамки B для этого радиуса фрезы в P63*'+ str(i)
            if 'R' in stroka and arguments['R'] < Rad_f:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Радиуса R в углах рамки не должны быть меньше радиуса фрезы для P63*'+ str(i)
            if 'U' in stroka and arguments['U'] <= 0:
                self.rude_mistakes['total'] = self.rude_mistakes['total'] + 1
                mis = self.rude_mistakes['total']
                self.rude_mistakes[mis] = 'Количество проходов U должно быть задано положительным числом в P63*'+ str(i)
        return None    
