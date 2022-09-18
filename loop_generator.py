"""This module searches for duplicate blocks and creates loops based on them.
"""

class Loops_body:
    def __init__(self,main_text):
        self.main_text = main_text
        self.head_ofText = []
        self.end_ofText = []
        self.cast_GXYRF = []
        self.cast_Z = []
        self.rep_block = []
        self.rep_Z = []
        self.top_levelZ = []
        self.bottom_levelZ = []
        self.amount_loop = 0
        self.number_b = ''


    def double_Separation(self):
        # Create head of text
        j = 0
        while j < len(self.main_text):
            if self.main_text[j][0] == '(':
                self.head_ofText.append(self.main_text[j])
                j += 1
            elif len(self.main_text[j].rstrip('\n').rstrip(' ')) == 0:
                self.head_ofText.append(self.main_text[j])
                j += 1
            else:
                break
        self.main_text = self.main_text[j:]

        # Create two arrays (for GXYRF and for Z)
        str_arguments = {}
        for i in self.main_text:
            str_arguments = make_arguments(i)
            if 'Z' in str_arguments.keys():
                self.cast_Z.append(str_arguments['Z'])
            else:
                self.cast_Z.append('None')
            stroka = Make_cast_x(str_arguments)
            self.cast_GXYRF.append(stroka)
        return None


    # Function searsh the repetition block self.rep_block
    def repetition_searsh(self):
        self.rep_block = []
        i = 0
        while i < len(self.cast_GXYRF) and len(self.rep_block) == 0:
            if len(self.cast_GXYRF[i]) > 0 and self.cast_GXYRF[i][0] != '(':
                k = i + 1
                while k < len(self.cast_GXYRF):
                    if self.cast_GXYRF[k] == self.cast_GXYRF[i] and \
                                    ((self.cast_Z[k] != 'None' and self.cast_Z[i] != 'None') or (self.cast_Z[k] == 'None' and self.cast_Z[i] == 'None')):
                        smesh = 0
                        while (i + smesh) < k:
                            if (k + smesh) < len(self.cast_GXYRF) and self.cast_GXYRF[i + smesh] == self.cast_GXYRF[k + smesh] and \
                                    ((self.cast_Z[i + smesh] != 'None' and self.cast_Z[k + smesh] != 'None') or (self.cast_Z[i + smesh] == 'None' and self.cast_Z[k + smesh] == 'None')):
                                self.rep_block.append(self.cast_GXYRF[i + smesh])
                                #print('ALL:',self.cast_GXYRF[i + smesh],self.cast_GXYRF[k + smesh],self.cast_Z[i + smesh],self.cast_Z[k + smesh],'i=',i,i + smesh,k + smesh,smesh,'REP=',len(self.rep_block))
                            else:
                                break
                            smesh += 1
                        if len(self.rep_block) != 0 and len(self.rep_block) <= 2:
                            #print('rep block was delete')
                            self.rep_block.clear()
                        if len(self.rep_block) != 0 and len(self.rep_block) == (k - i):
                            #print('WE FINISHED')
                            break
                        elif len(self.rep_block) != 0 and len(self.rep_block) != (k - i):
                            self.rep_block.clear()
                            #print('rep block was delete')
                    k += 1
            i += 1
        # Correct val i
        i -= 1
        # Check if I need to increase my head text
        if i > 0:
            j = 0
            while j < i:
                stroka = glue_end_string(self.cast_GXYRF[j],self.cast_Z[j])
                self.head_ofText.append(stroka)
                j += 1
            self.cast_GXYRF = self.cast_GXYRF[i:]
            self.cast_Z = self.cast_Z[i:]
        k = 0
        # Create repetition for Z levels - we need it in "replace_block()" module
        while k < len(self.rep_block):
            self.rep_Z.append(self.cast_Z[k])
            k += 1
        return None

    # Function counts the number of repetitions self.amount_loop
    # Function searches of the top and the bottom level Z
    # Function makes END of text
    def cut_repetit(self):
        k = 0
        while k < len(self.rep_block):
            if ((k+len(self.rep_block)) < len(self.cast_GXYRF)) and self.cast_Z[k] != 'None' and \
                    self.cast_Z[k+len(self.rep_block)] != 'None' and \
                    round((float(self.cast_Z[k]) - float(self.cast_Z[k+len(self.rep_block)])),4) != 0:
                self.top_levelZ.append(self.cast_Z[k])
                self.bottom_levelZ.append(self.cast_Z[k])
            k += 1
        self.amount_loop += 1
        i = 0
        t = 0
        amount_z = 0
        while i < len(self.cast_GXYRF):
            if t < len(self.rep_block) and self.rep_block[t] == self.cast_GXYRF[i]:
                if self.cast_Z[t] != 'None' and self.cast_Z[t] in self.top_levelZ and self.cast_Z[i] != 'None':
                    self.bottom_levelZ.insert(amount_z,self.cast_Z[i])
                    del self.bottom_levelZ[amount_z + 1]
                    amount_z += 1
                t += 1
                if t == len(self.rep_block):
                    t = 0
                    amount_z = 0
                    self.amount_loop += 1
            else:
                self.cast_GXYRF = self.cast_GXYRF[i:]
                self.cast_Z = self.cast_Z[i:]
                break
            i += 1
        j = 0
        while j < len(self.cast_GXYRF):
            stroka = glue_end_string(self.cast_GXYRF[j], self.cast_Z[j])
            self.end_ofText.append(stroka)
            j += 1
        return None


    # Create repetition block instead we had in main program
    def replace_block(self):
        rep_text = ['\n']
        num_par = []
        numer = 105
        Feed = '1000'
        str_arguments = []
        for i in self.rep_block:
            str_arguments = make_arguments(i)
            if 'F' in str_arguments.keys() and len(str_arguments) > 1:
                Feed = str_arguments['F']
                break
        rep_text.append('#100=' + Feed + '\n')
        rep_text.append('#106=' + str(self.amount_loop) + '\n')
        j = 0
        k = 0
        for i in self.top_levelZ:
            num_par.append('#' + str(numer + j))
            stroka = ''
            if (float(self.top_levelZ[k]) - float(self.bottom_levelZ[k])) > 0:
                #stroka = str(round((float(self.top_levelZ[k]) + ((float(self.top_levelZ[k]) - float(self.bottom_levelZ[k])) / self.amount_loop)),4))
                # shem_z - съем по Z за один проход
                shem_z = round(((float(self.top_levelZ[k]) - float(self.bottom_levelZ[k])) / self.amount_loop),4)
                new_top_z = round((float(self.bottom_levelZ[k]) + shem_z * self.amount_loop),4)
                stroka = str(new_top_z)
            elif (float(self.top_levelZ[k]) - float(self.bottom_levelZ[k])) <= 0:
                #stroka = str(round((float(self.top_levelZ[k]) - ((float(self.top_levelZ[k]) - float(self.bottom_levelZ[k])) / self.amount_loop)),4))
                shem_z = round(((float(self.top_levelZ[k]) - float(self.bottom_levelZ[k])) / self.amount_loop), 4)
                new_top_z = round((float(self.bottom_levelZ[k]) - shem_z * self.amount_loop),4)
                stroka = str(new_top_z)
            rep_text.append('#' + str(numer + j) + '=' + stroka + '\n')
            j += 2
            k += 1
        rep_text.append('\n')
        rep_text.append('N' + self.number_b + '\n')
        j = 0
        for i in num_par:
            stroka = ''
            if (float(self.top_levelZ[j]) - float(self.bottom_levelZ[j])) > 0:
                stroka = stroka + i + '=' + i + '-' + str(round((float(self.top_levelZ[j]) - float(self.bottom_levelZ[j])) / self.amount_loop, 4))
            elif (float(self.top_levelZ[j]) - float(self.bottom_levelZ[j])) <= 0:
                stroka = stroka + i + '=' + i + '+' + str(-1*(round((float(self.top_levelZ[j]) - float(self.bottom_levelZ[j])) / self.amount_loop, 4)))
            rep_text.append(stroka + '\n')
            j += 1
        k = 0
        t = 0
        str_arguments = []
        while k < len(self.rep_block):
            Z_string = ''
            str_arguments = make_arguments(self.rep_block[k])
            if self.rep_Z[k] != 'None':
                if self.rep_Z[k] in self.top_levelZ:
                    Z_string = 'Z#' + str(105 + t*2)
                    t += 1
                else:
                    Z_string = 'Z' + self.rep_Z[k]
            stroka = ''
            for i in str_arguments.keys():
                if i != 'F':
                    if i == 'G_stroka':
                        stroka = stroka + str_arguments[i]
                    elif i == 'other':
                        stroka = stroka + str_arguments[i]
                    else:
                        stroka = stroka + i + str_arguments[i]
            stroka = stroka + Z_string
            if 'F' in str_arguments.keys() and str_arguments['F'] == Feed:
                stroka = stroka + 'F#100'
            elif 'F' in str_arguments.keys():
                stroka = stroka + i + str_arguments[i]
            stroka = stroka + '\n'
            rep_text.append(stroka)
            k += 1
        if len(self.top_levelZ) == 1 and '#105' in rep_text[len(rep_text)-1]:
            rep_text.insert(7,rep_text[len(rep_text)-1])
            del rep_text[len(rep_text)-1]
        rep_text.append('\n')
        rep_text.append('G31\n')
        rep_text.append('#106=#106-1\n')
        rep_text.append('IF[#106GT0]GOTO' + self.number_b + '\n')
        rep_text.append('\n')
        return rep_text

    # Create number for our repetition section
    def make_numbers(self,stroka):
        number_k = ''
        if 'N' in stroka:
            number_k = stroka.lstrip('N').rstrip('\n')
            self.number_b = (str(int(number_k) + 1))
        else:
            self.number_b = (str(int(stroka) + 1))
        return self.number_b


def glue_string(XY_string,Z_string):
    stroka = ''
    feed = ''
    all_arguments = make_arguments(XY_string)
    all_arguments['Z'] = make_arguments(Z_string)['other']
    for i in all_arguments:
        if i == 'G_stroka':
            stroka = stroka + all_arguments[i]
        elif i == 'other':
            stroka = stroka + all_arguments[i]
        elif i == 'Z':
            if all_arguments['Z'] != None:
                stroka = stroka + 'Z'+ all_arguments[i]
        elif i == 'F':
            feed = 'F' + all_arguments[i]
        else:
            stroka = stroka + i + all_arguments[i]
    stroka = stroka + feed + '\n'
    return stroka


def glue_end_string(XY_string,Z_string):
    stroka = ''
    feed = ''
    all_arguments = make_arguments(XY_string)
    all_arguments['Z'] = make_arguments(Z_string)['other']
    if all_arguments['Z'] == 'None':
        del all_arguments['Z']
    for i in all_arguments:
        if i == 'G_stroka':
            stroka = stroka + all_arguments[i]
        elif i == 'other':
            stroka = stroka + all_arguments[i]
        elif i == 'Z':
            if all_arguments['Z'] != None:
                stroka = stroka + 'Z'+ all_arguments[i]
        elif i == 'F':
            feed = 'F' + all_arguments[i]
        else:
            stroka = stroka + i + all_arguments[i]
    stroka = stroka + feed + '\n'
    return stroka


def Make_cast_x(arguments):
    stroka = ''
    for k in arguments:
        if k != 'Z':
            if k == 'G_stroka':
                stroka = stroka + str(arguments[k])
            elif k == 'other':
                stroka = stroka + str(arguments[k])
            else:
                stroka = stroka + k + str(arguments[k])
    return stroka


def make_arguments(stroka):
    stroka = stroka.rstrip('\n')
    letters = 'XYZRF'
    numbers = '0123456789-.'
    G_numbers = 'G0123456789'
    G_stroka = ''
    str_arguments = {}
    i = 0
    if len(stroka) > 0:
        if stroka[0] == 'G':
            while i < len(stroka):
                if stroka[i] in G_numbers:
                    G_stroka = G_stroka + stroka[i]
                    i += 1
                else:
                    break
        if G_stroka != '':
            str_arguments['G_stroka'] = G_stroka
        while i < len(stroka):
            if stroka[i] in letters:
                j = i+1
                key_stroka = stroka[i]
                key_mean = ''
                while j < len(stroka):
                    if stroka[j] in numbers:
                        key_mean = key_mean + stroka[j]
                        j += 1
                    else:
                        i = j - 1
                        str_arguments[key_stroka] = key_mean
                        break
                    if j == len(stroka):
                        str_arguments[key_stroka] = key_mean
            elif i == 0 and stroka[i] not in letters:
                str_arguments['other'] = stroka[i:]
                break
            i += 1
    else:
        str_arguments['other'] = ''
    return str_arguments