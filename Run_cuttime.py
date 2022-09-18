"""This modul can count time of cutting and drilling for blocks
"""
import decimal
import math
from decimal import Decimal


class Run_timer:
    def __init__(self,Myblock, title, parametrs, diametr_f = 0):
        self.Myblock = Myblock
        self.title = title
        self.time_cutting = 0.46
        self.radius_f = diametr_f / 2
        self.param = parametrs
        


    # Count cutting time
    def first_time(self):
        if self.title == 'milling':
            self.time_cutting = self.milling_time()
        elif self.title == 'Drill':
            self.time_cutting = self.drill_time()
        elif self.title == 'Loop':
            self.time_cutting = self.loop_time()
        elif self.title == 'milling_GOTO':
            self.time_cutting = self.millingGOTO_time()
        elif self.title == 'Ren_150':
            self.time_cutting = self.Ren_150time()
        return self.time_cutting


    # Count time for milling 
    def Ren_150time(self):
        numbers = '-0123456789.'        
        X1 = 0.0 #old X
        X2 = 0.0 #new X
        Y1 = 0.0
        Y2 = 0.0
        V = 0.0
        W = 0.0
        i = 0
        time_comp = 0.114 #Time compensation for Ren_150
        arguments = []
        while i < len(self.Myblock)-2:
            if self.Myblock[i] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(' or self.Myblock[i][0] == 'N':
                i += 1
            else:
                X1 = X2
                Y1 = Y2
                arguments = self.arg_read(self.Myblock[i])
                for j in arguments:
                    if 'X' in j:
                        X2 = float(j[1:])
                    elif 'Y' in j:
                        Y2 = float(j[1:])
                    elif 'V' in j:
                        V = float(j[1:])
                    elif 'W' in j:
                        W = float(j[1:])
                try:
                    if len(self.Myblock[i]) > 3 and 'P151' in self.Myblock[i]:
                        #G1Z#961F1000(MOVE TO V)
                        distance = 2*(math.sqrt(pow((V-W),2)))
                        self.time_cutting = self.time_cutting + (distance / 1000)
                        #G1X#959Y#960F2000(MOVE TO XY)
                        distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2))
                        self.time_cutting = self.time_cutting + (distance / 2000)
                        self.time_cutting = self.time_cutting + time_comp
                except:
                    self.time_cutting = self.time_cutting + 0                
                i += 1
        return self.time_cutting



    # Count time for milling 
    def milling_time(self):
        numbers = '-0123456789.'        
        mode_g = 'G1'
        group_07 = 'G40'
        old_group_07 = 'G40'
        X1 = 0.0 #old X
        X2 = 0.0 #new X
        X3 = 0.0 #will be in next position
        Y1 = 0.0
        Y2 = 0.0
        Y3 = 0.0
        Z1 = 0.0
        Z2 = 0.0
        F = 0.0
        R = 0.0
        i = 0
        arguments_1 = []
        arguments_2 = []
        arguments_3 = []
        marker = 0
        while marker == 0:
            if 'G201' in self.Myblock[i]:
                marker = 1
            i += 1
        while i < len(self.Myblock)-2:
            if self.Myblock[i] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(':
                i += 1
            else:
                X1 = X2
                Y1 = Y2
                Z1 = Z2
                old_group_07 = group_07
                if 'G1' in self.Myblock[i]:
                    mode_g = 'G1'
                elif 'G2' in self.Myblock[i]:
                    mode_g = 'G2'
                elif 'G3' in self.Myblock[i]:
                    mode_g = 'G3'
                elif 'G0' in self.Myblock[i]:
                    mode_g = 'G0'
                if 'G41' in self.Myblock[i] or 'G42'in self.Myblock[i]:
                    group_07 = 'G41'
                elif 'G40' in self.Myblock[i]:
                    group_07 = 'G40'
                arguments_2 = self.arg_read(self.Myblock[i])
                for j in arguments_2:
                    if 'X' in j:
                        X2 = float(j[1:])
                    elif 'Y' in j:
                        Y2 = float(j[1:])
                    elif 'Z' in j:
                        Z2 = float(j[1:])
                    elif 'R' in j:
                        R = float(j[1:])
                    elif 'F' in j:
                        F = float(j[1:])
                try:
                    if (old_group_07 == group_07) and group_07 == 'G40':
                        if mode_g == 'G1':
                            distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))
                            self.time_cutting = self.time_cutting + (distance / F)
                        if mode_g == 'G2' or mode_g == 'G3':
                            distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))
                            angle = ((math.acos(distance / (2 * R))) * 180) / math.pi
                            dis_angl = (math.pi * R * (180 - 2 * angle) )/ 180
                            self.time_cutting = self.time_cutting + (dis_angl / F)                        
                    elif (old_group_07 != group_07) and group_07 == 'G41':
                        distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))-self.radius_f
                        self.time_cutting = self.time_cutting + (distance / F)
                    elif (old_group_07 == group_07) and group_07 == 'G41':
                        add_distanse = 0
                        if 'G40' not in self.Myblock[i+1]:
                            if 'X' in self.Myblock[i+1] or 'Y' in self.Myblock[i+1] and self.Myblock[i+1][0] != '(':
                                arguments_3 = self.arg_read(self.Myblock[i+1])
                                for j in arguments_3:
                                    if 'X' in j:
                                        X3 = float(j[1:])
                                    elif 'Y' in j:
                                        Y3 = float(j[1:])
                                    elif 'Z' in j:
                                        Z3 = float(j[1:])
                                if 'X' in self.Myblock[i+1] and X3 < X2:
                                    betta = 180.0 - (self.count_alfa(X1,X2,X3,Y1,Y2,Y3))
                                    add_distance = (1/(360 / betta)) * 2 * math.pi * self.radius_f
                                elif 'X' in self.Myblock[i+1] and X3 > X2:
                                    alfa = self.count_alfa(X1,X2,X3,Y1,Y2,Y3)
                                    if alfa < 180:
                                        add_distanse = -2 * (self.radius_f / (math.atan(alfa / 2)))
                        distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))
                        distance = distance + add_distanse
                        self.time_cutting = self.time_cutting + (distance / F)
                    else:
                        distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))-self.radius_f
                        self.time_cutting = self.time_cutting + (distance / F)                        
                except:
                    self.time_cutting = self.time_cutting + 0                
                i += 1
        return self.time_cutting
        


    # Count time for drill G83 G81
    def drill_time(self):
        numbers = '-0123456789.'
        mode_g = 'G1'
        X1 = 0.0 #old X
        X2 = 0.0 #new X
        Y1 = 0.0
        Y2 = 0.0
        Z1 = 0.0
        Z2 = 0.0
        F = 0.0
        R = 0.0
        Q = 0.1
        i = 0
        time_comp = 0.007275 #Magic time compensation for each short distance, if feed F = 5000 and we change way by Z
        marker = 0
        while marker == 0:
            if 'G201' in self.Myblock[i]:
                marker = 1
            i += 1
        while i < len(self.Myblock):
            while self.Myblock[i][0] == '/':
                i += 1            
            arguments = []
            X1 = X2
            Y1 = Y2
            Z1 = Z2
            arguments = self.arg_read(self.Myblock[i])
            for j in arguments:
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
            if 'G1' in arguments:
                mode_g = 'G1'
            elif 'G81' in arguments:
                mode_g = 'G81'
            elif 'G83' in arguments:
                mode_g = 'G83'
            elif 'G80' in arguments:
                Z1 = Z2
                mode_g = 'G1'
            distance = 0
            try:
                if mode_g == 'G1':
                    distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                elif mode_g == 'G81':
                    # Move to position X Y, feed rate = 5000
                    old_f = F
                    F = 5000
                    distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Move down to position R - Z, feed rate = actual from loop G81
                    Z1 = R
                    F = old_f
                    distance = math.sqrt(pow((Z2-Z1),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Move back to top posisiton R, feed rate = 5000
                    F = 5000
                    self.time_cutting = self.time_cutting + (distance / F) + time_comp
                    F = old_f
                elif mode_g == 'G83':
                    # Move to position X Y, feed rate = 5000
                    old_f = F
                    F = 5000
                    distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Move down to position R - 1*Q, feed rate = actual from loop G83
                    new_top = R - Q
                    niz = Z2
                    F = old_f
                    distance = math.sqrt(pow((R-new_top),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Move back to top posisiton R, feed rate = 5000
                    F = 5000
                    self.time_cutting = self.time_cutting + (distance / F) + time_comp
                    F = old_f
                    while niz < new_top:
                        # Move down to actial level R - n*Q, feed rate = 5000
                        old_f = F
                        F = 5000
                        new_top = new_top + 0.05
                        distance = math.sqrt(pow((R-new_top),2))
                        self.time_cutting = self.time_cutting + (distance / F)
                        # Move down to position R - n*Q, feed rate = actual from loop G83
                        new_top = new_top - Q - 0.05
                        F = old_f
                        distance = math.sqrt(pow((Q + 0.05),2))
                        self.time_cutting = self.time_cutting + (distance / F)
                        # Move back to top posisiton R, feed rate = 5000
                        F = 5000
                        distance = math.sqrt(pow((R-new_top),2))
                        self.time_cutting = self.time_cutting + (distance / F) + time_comp
                        F = old_f
            except:
                self.time_cutting = self.time_cutting + 0
            i += 1
        return self.time_cutting


    # Count time for Loop P43 P44 P47 P62 P63 P64 P71 P80
    def loop_time(self):
        numbers = '-0123456789.'
        mode_g = 'G1'
        X1 = 0.0 #old X
        X2 = 0.0 #new X
        Y1 = 0.0
        Y2 = 0.0
        Z1 = 0.0
        Z2 = 0.0
        V = 0.0
        W = 0.0
        V = 0.0
        M = 0.0
        P = 0.0
        K = 0.0
        E = 0.0
        A = 0.0
        B = 0.0
        Ii= 0.0
        Jj = 0.0
        U = 0.0
        Q = 0.1
        D = 0.0
        R = 0.0
        F = 5000.0
        T = 0.0
        S = 0.0
        i = 0
        X_Y_point_P80 = {}
        X_Y_point_P64 = {}
        X_Y_point_P47 = {}
        X_Y_point_P62 = {}
        X_Y_point_P63 = {}
        X_Y_point_P44 = {}
        time_comp = 0.007275 #Magic time compensation for each short distance, if feed F = 5000 and we change way by Z
        marker = 0
        old_P = ''
        now_P = ''        
        while marker == 0:
            if 'S' in self.Myblock[i]:
                arguments = self.arg_read(self.Myblock[i])
                for j in arguments:
                    if 'S' in j:
                        if j[1] == '#' and j[1:] in self.param:
                            S = self.param[j[1:]]
                        else:
                            S = float(j[1:]) 
            if 'G201' in self.Myblock[i]:
                marker = 1
            i += 1
        while i < len(self.Myblock):
            while self.Myblock[i][0] == '/':
                i += 1            
            arguments = []
            X1 = X2
            Y1 = Y2
            Z1 = Z2
            arguments = self.arg_read(self.Myblock[i])
            for j in arguments:
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
                elif 'W' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        W = self.param[j[1:]]
                    else:
                        W = float(j[1:])                    
                elif 'M' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        M = self.param[j[1:]]
                    else:
                        M = float(j[1:])                    
                elif 'V' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        V = self.param[j[1:]]
                    else:
                        V = float(j[1:])                    
                elif 'K' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        K = self.param[j[1:]]
                    else:
                        K = float(j[1:])                    
                elif 'E' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        E = self.param[j[1:]]
                    else:
                        E = float(j[1:])                    
                elif 'A' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        A = self.param[j[1:]]
                    else:
                        A = float(j[1:])                    
                elif 'B' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        B = self.param[j[1:]]
                    else:
                        B = float(j[1:])                    
                elif 'J' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        Jj = self.param[j[1:]]
                    else:
                        Jj = float(j[1:])                    
                elif 'I' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        Ii = self.param[j[1:]]
                    else:
                        Ii = float(j[1:])                    
                elif 'U' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        U = self.param[j[1:]]
                    else:
                        U = float(j[1:])                    
                elif 'Q' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        Q = self.param[j[1:]]
                    else:
                        Q = float(j[1:])                    
                elif 'D' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        D = self.param[j[1:]]
                    else:
                        D = float(j[1:])                    
                elif 'T' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        T = self.param[j[1:]]
                    else:
                        T = float(j[1:])                    
                elif 'S' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        S = self.param[j[1:]]
                    else:
                        S = float(j[1:])                    
                elif 'P' in j:
                    if j[1] == '#' and j[1:] in self.param:
                        P = self.param[j[1:]]
                    else:
                        P = float(j[1:])
            if 'G1' in arguments:
                mode_g = 'G1'
            elif 'G65' in arguments:
                mode_g = 'G65'
            elif 'G66' in arguments:
                mode_g = 'G66'
            elif 'G67' in arguments:
                mode_g = 'G1'
            distance = 0
            old_P = now_P
            if mode_g == 'G1':
                distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))
                self.time_cutting = self.time_cutting + (distance / F)
            elif mode_g == 'G65' and 'P43' in arguments:
                # Q=0.1 U=0 F=150 by default for P43
                now_P = 'P43'
                if now_P != old_P and 'F' not in self.Myblock[i]:
                    F = 150.0
                if now_P != old_P and 'Q' not in self.Myblock[i]:
                    Q = 0.1
                u_in = 0
                for j in arguments:
                    if 'U' in j:
                        u_in = 1
                if u_in == 0:
                    U = 0.0
                V = self.P43_loop(X1,X2,Y1,Y2,Z1,Z2,V,W,D,Q,U,F,self.radius_f)
            elif mode_g == 'G65' and 'P80' in arguments:
                # E=50 J=1 U=0 F=1000 by default for P80
                now_P = 'P80'
                if now_P != old_P and 'F' not in self.Myblock[i]:
                    F = 1000.0
                if now_P != old_P and 'E' not in self.Myblock[i]:
                    E = 50.0
                if now_P != old_P and 'J' not in self.Myblock[i]:
                    Jj = 2.0
                u_in = 0
                for j in arguments:
                    if 'U' in j:
                        u_in = 1
                if u_in == 0:
                    U = 0.0
                if len(X_Y_point_P80) != 0:
                    X1 = X_Y_point_P80['X']
                    Y1 = X_Y_point_P80['Y']
                    Z1 = X_Y_point_P80['Z1']
                X_Y_point_P80 = self.P80_loop(X1,X2,Y1,Y2,Z1,Z2,V,W,A,B,E,F,Jj,Q,U,self.radius_f)
            elif mode_g == 'G65' and 'P64' in arguments:
                # K=5 J=0 I=0 U=0 E=0 R=0.01 F=1000 by default for P64
                now_P = 'P64'
                if now_P != old_P and 'F' not in self.Myblock[i]:
                    F = 1000.0
                if now_P != old_P and 'K' not in self.Myblock[i]:
                    K = 5.0
                if now_P != old_P and 'J' not in self.Myblock[i]:
                    Jj = 0.0
                if now_P != old_P and 'I' not in self.Myblock[i]:
                    Ii = 0.0
                if now_P != old_P and ('R' not in self.Myblock[i] and 'E' not in self.Myblock[i]):
                    R = 0.01
                if 'R' in self.Myblock[i]:
                    E = 0.0
                if 'E' in self.Myblock[i]:
                    R = 0.0                    
                u_in = 0
                for j in arguments:
                    if 'U' in j:
                        u_in = 1
                if u_in == 0:
                    U = 0.0
                if len(X_Y_point_P64) != 0:
                    X1 = X_Y_point_P64['X']
                    Y1 = X_Y_point_P64['Y']
                    Z1 = X_Y_point_P64['Z1']
                X_Y_point_P64 = self.P64_loop(X1,X2,Y1,Y2,Z1,Z2,V,W,A,B,Ii,Jj,Q,U,E,R,K,F,self.radius_f)
            elif mode_g == 'G65' and 'P47' in arguments:
                # Q=0.01 J=1 U=0 F=500 by default for P47
                now_P = 'P47'
                if now_P != old_P and 'F' not in self.Myblock[i]:
                    F = 500.0
                if now_P != old_P and 'Q' not in self.Myblock[i]:
                    Q = 0.01
                if now_P != old_P and 'J' not in self.Myblock[i]:
                    Jj = 1
                u_in = 0
                for j in arguments:
                    if 'U' in j:
                        u_in = 1
                if u_in == 0:
                    U = 0.0
                if len(X_Y_point_P47) != 0:
                    X1 = X_Y_point_P47['X']
                    Y1 = X_Y_point_P47['Y']
                    Z1 = X_Y_point_P47['Z1']
                X_Y_point_P47 = self.P47_loop(X1,X2,Y1,Y2,Z1,Z2,V,W,D,R,F,Jj,Q,U,self.radius_f)
            elif mode_g == 'G65' and 'P62' in arguments:
                # R=radius_f I=40 U=0 F=1000 by default for P62
                now_P = 'P62'
                if now_P != old_P and 'F' not in self.Myblock[i]:
                    F = 1000.0
                if now_P != old_P and 'R' not in self.Myblock[i]:
                    R = self.radius_f
                if now_P != old_P and 'I' not in self.Myblock[i]:
                    Ii = 40
                u_in = 0
                for j in arguments:
                    if 'U' in j:
                        u_in = 1
                if u_in == 0:
                    U = 0.0
                if len(X_Y_point_P62) != 0:
                    X1 = X_Y_point_P62['X']
                    Y1 = X_Y_point_P62['Y']
                    Z1 = X_Y_point_P62['Z1']
                X_Y_point_P62 = self.P62_loop(X1,X2,Y1,Y2,Z1,Z2,V,W,A,B,R,F,Ii,Q,U,self.radius_f)
            elif mode_g == 'G66' and 'P44' not in self.Myblock[i]:
                # V=Z+10 E=3 F=mean from table, by default for P44
                now_P = 'P44'
                if now_P != old_P and 'V' not in self.Myblock[i]:
                    V = Z2+10
                if now_P != old_P and 'E' not in self.Myblock[i]:
                    E = 3
                if len(X_Y_point_P44) != 0:
                    X1 = X_Y_point_P44['X']
                    Y1 = X_Y_point_P44['Y']
                    Z1 = X_Y_point_P44['Z1']
                X_Y_point_P44 = self.P44_loop(X1,X2,Y1,Y2,Z1,Z2,V,W,M,K,E,S,self.radius_f)
            elif mode_g == 'G65' and 'P63' in arguments:
                # R=radius_f K=0.2 U=0 F=1000 by default for P63
                now_P = 'P63'
                if now_P != old_P and 'F' not in self.Myblock[i]:
                    F = 1000.0
                if now_P != old_P and 'R' not in self.Myblock[i]:
                    R = self.radius_f
                if now_P != old_P and 'K' not in self.Myblock[i]:
                    K = 0.2
                u_in = 0
                for j in arguments:
                    if 'U' in j:
                        u_in = 1
                if u_in == 0:
                    U = 0.0
                if len(X_Y_point_P63) != 0:
                    X1 = X_Y_point_P63['X']
                    Y1 = X_Y_point_P63['Y']
                    Z1 = X_Y_point_P63['Z1']
                X_Y_point_P63 = self.P63_loop(X1,X2,Y1,Y2,Z1,Z2,V,W,A,B,R,F,K,Q,U,self.radius_f)
            i += 1
        return self.time_cutting


    # Help count angle
    def count_angle41(self, X1, X2, X3, Y1, Y2, Y3):
        ang = 0
        return ang


    def P43_loop(self,X1,X2,Y1,Y2,Z1,Z2,V,W,D,Q,U,F,Rad_fr):
        # Count parametrs from P43 (p28 = #28 and e.g.)
        n = 1           # amount of spiral
        t = abs(W - Z2) # K (steep)
        ds = (D / 2) - Rad_fr
        if U != 0:
            n = U
            t = (abs(W - Z2)) / U
        else:
            n = (abs(W - Z2)) / Q
            t = Q
        # Code G40G1Z#22F4000M8 from P43
        distance = math.sqrt(pow((V-Z1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        Z1 = V
        # Code X#24Y#25
        distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        # Code Z[#28+1]F1000
        distance = math.sqrt(pow((Z2 + 1 - Z1),2))
        self.time_cutting = self.time_cutting + (distance / 1000)
        Z1 = Z2 + 1
        # Code G1Z#28F500 
        distance = math.sqrt(pow((Z2 - Z1),2))
        self.time_cutting = self.time_cutting + (distance / 500)
        # Code G1G41X[#24+[#7/2]]F#9 and G1G40X#24
        distance = 2 * (math.sqrt(pow((D / 2 - Rad_fr),2)))
        self.time_cutting = self.time_cutting + (distance / F)
        # Code G3I[-1*[#7/2]]Z#23K[-1*#17]
        distance = n * math.sqrt(pow((math.pi * ((D / 2 - Rad_fr))*2),2) + pow(t,2))
        self.time_cutting = self.time_cutting + (distance / F)
        # Code G3I[-1*[#7/2]] twice
        distance = 2 * (2 * math.pi * (D / 2 - Rad_fr))
        self.time_cutting = self.time_cutting + (distance / F)
        # Code Z#28F1000
        distance = math.sqrt(pow((W - Z2),2))
        self.time_cutting = self.time_cutting + (distance / 1000)
        # Code Z#22F1000
        distance = math.sqrt(pow((Z2 - V),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        return V


    def P80_loop(self,X1,X2,Y1,Y2,Z1,Z2,V,W,A,B,E,F,J,Q,U,Rad_fr):
        if U != 0:
            Q = (abs(W - Z2)) / U
        X_Y_point ={}
        # p12 -> #12 KOL-VO PROHODOV
        p12 = math.ceil((abs(Z2-W))/Q)
        # p28 -> #28 VERHNIY UROVEN PO Z - NACHALO SJEMA
        p28 = Q * p12 + W
        # p13 -> #13 KOORDINATA X PODHODA FREZI. PODHOD ZA 5MM DO ZAGOTOVKI
        p13 = (X2 - (A / 2)) - Rad_fr - 5
        # p7 -> #7 PEREKRITIA FREZI - SJEM V PLOSKOSTI XY
        p7 = ((Rad_fr*2)/100)*E
        # p29 -> #29 KOORDINATA Y PODHODA FREZI
        p29 = (Y2 + (B / 2)) + Rad_fr - p7
        # Code G40G1X#13Y#29F4000M8M138
        distance = math.sqrt(pow((p13-X1),2) + pow((p29-Y1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        distance = math.sqrt(pow((V-Z1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)        
        if J == 1:
            while p12 >= 1:
                p28 = p28 - Q
                p12 -= 1
                # Code G1Z[#28+1]F2000
                distance = math.sqrt(pow((p28 + 1 - V),2))
                self.time_cutting = self.time_cutting + (distance / 2000)
                # Code Z#28F#9
                self.time_cutting = self.time_cutting + (1 / F)
                p13 = p13 + p7 + 5
                distance = math.sqrt(pow((p7 + 5),2))
                self.time_cutting = self.time_cutting + (distance / F)                
                while (p29 > (Y2 - B / 2)):
                    p13 += A
                    distance = math.sqrt(pow(A,2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    p29 -= p7
                    distance = math.sqrt(pow(p7,2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    p13 -= A
                    distance = math.sqrt(pow(A,2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    p29 -= p7
                    distance = math.sqrt(pow(p7,2))
                    self.time_cutting = self.time_cutting + (distance / F)
                # Code G1Z#22F4000
                distance = math.sqrt(pow((V - p28),2))
                self.time_cutting = self.time_cutting + (distance / 4000)
                # Code X#13Y#29
                distance = math.sqrt(pow(((X2 - A/2 - Rad_fr - 5) - p13),2) + pow(((Y2 + B/2 + Rad_fr - p7) - p29),2))
                self.time_cutting = self.time_cutting + (distance / 4000)
                p13 = X2 - A/2 - Rad_fr - 5
                p29 = Y2 + B/2 + Rad_fr - p7
            X_Y_point['X'] = p13
            X_Y_point['Y'] = p29
            X_Y_point['Z1'] = V
        else:
            while p12 >= 1:
                p28 = p28 - Q
                p12 -= 1
                # Code G1Z[#28+1]F2000
                distance = math.sqrt(pow((p28 + 1 - V),2))
                self.time_cutting = self.time_cutting + (distance / 2000)
                # Code Z#28F#9
                self.time_cutting = self.time_cutting + (1 / F)
                p14 = X2 + A / 2 + Rad_fr
                p15 = Y2 - B / 2 - Rad_fr
                p16 = X2 - A / 2 - Rad_fr
                p19 = Y2 + B / 2 + Rad_fr - p7
                distance = math.sqrt(pow((p16-p13),2))
                self.time_cutting = self.time_cutting + (distance / F)                
                while (p19 > Y2 and p14 > X2):
                    p14 -= p7
                    distance = math.sqrt(pow((p14 - p16),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    p15 += p7
                    distance = math.sqrt(pow((p15 - p19),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    p16 += p7
                    distance = math.sqrt(pow((p16 - p14),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    p19 -= p7
                    distance = math.sqrt(pow((p19 - p15),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                # Code Y#25
                distance = math.sqrt(pow((Y2 - p19),2))
                self.time_cutting = self.time_cutting + (distance / F)
                # Code X#14
                distance = math.sqrt(pow((p14 - p16),2))
                self.time_cutting = self.time_cutting + (distance / F)                    
                # Code G1Z#22F4000
                distance = math.sqrt(pow((V - p28),2))
                self.time_cutting = self.time_cutting + (distance / 4000)
                # Code X#13Y#29
                distance = math.sqrt(pow((p13 - p14),2) + pow((p29 - Y2),2))
                self.time_cutting = self.time_cutting + (distance / 4000)
            X_Y_point['X'] = p13
            X_Y_point['Y'] = p29
            X_Y_point['Z1'] = V
        return X_Y_point    


    def P64_loop(self,X1,X2,Y1,Y2,Z1,Z2,V,W,A,B,I,J,Q,U,E,R,K,F,Rad_fr):
        X_Y_point ={}
        if U != 0:
            Q = (abs(W - Z2)) / U
        # p12 -> #12 KOL-VO PROHODOV
        p12 = math.ceil((abs(W-Z2))/Q)
        # p28 -> #28 VERHNIY UROVEN PO Z - NACHALO SJEMA
        p28 = Q * p12 + W
        A = A / 2
        B = B / 2
        p14 = A
        p15 = B
        I = I / 2
        J = J / 2
        if I > 0:
            p14 = I
        if J > 0:
            p15 = J
        p29 = p14
        p30 = p15
        p19 = (X2 - p14) - Rad_fr - K
        # Code G40G1X#19Y#25F4000M8M138
        distance = math.sqrt(pow((p19-X1),2) + pow((Y2-Y1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        # Code G1Z#22F4000
        distance = math.sqrt(pow((V-Z1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        # Code G1Z#28F1000
        distance = math.sqrt(pow((p28-V),2))
        self.time_cutting = self.time_cutting + (distance / 1000)
        if R != 0 :
            if (B - R) <= Rad_fr:
                p3 = Y2 + B - R
            else:
                p3 = Y2 + Rad_fr
            while (p12 >= 1):
                p12 -= 1
                p28 -= Q
                # Code G1Z#28F[#9/5]
                distance = math.sqrt(pow(Q,2))
                self.time_cutting = self.time_cutting + (distance / (F / 5))
                p14 = p29
                p15 = p30
                p20 = 1
                while((p14 > A) or (p15 > B) or (p20 == 1)):
                    p14 -= Rad_fr
                    if p14 < A:
                        p14 = A
                    p15 -= Rad_fr
                    if p15 < B:
                        p15 = B
                    p20 = 0
                    # Code G41X[#24-#14]
                    tek_pos = X2-p14
                    distance = math.sqrt(pow(K,2))
                    self.time_cutting = self.time_cutting + (distance / (F / 5))
                    # distace = 2pR
                    distance = 2*math.pi*(R+Rad_fr)
                    self.time_cutting = self.time_cutting + (distance / F)
                    # distace = 2*width + 2*hight
                    distance = 4*p15+4*p14+Rad_fr
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Code X#19Y#25
                    distance = math.sqrt(pow((p19-tek_pos),2)+pow(Rad_fr,2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Code X#19Y#25
            distance = math.sqrt(pow((W-V),2))
            self.time_cutting = self.time_cutting + (distance / 4000)
            X_Y_point['X'] = p19
            X_Y_point['Y'] = Y2
            X_Y_point['Z1'] = V
        else:
            if (B - E) <= Rad_fr:
                p3 = Y2 + B - E
            else:
                p3 = Y2 + Rad_fr
            while (p12 >= 1):
                p12 -= 1
                p28 -= Q
                # Code G1Z#28F[#9/5]
                distance = math.sqrt(pow(Q,2))
                self.time_cutting = self.time_cutting + (distance / (F / 5))
                p14 = p29
                p15 = p30
                p20 = 1
                while((p14 > A) or (p15 > B) or (p20 == 1)):
                    p14 -= Rad_fr
                    if p14 < A:
                        p14 = A
                    p15 -= Rad_fr
                    if p15 < B:
                        p15 = B
                    p20 = 0
                    # Code G41X[#24-#14]
                    tek_pos = X2-p14
                    distance = math.sqrt(pow(K,2))
                    self.time_cutting = self.time_cutting + (distance / (F / 5))
                    # distace for faski E
                    distance = (math.sqrt(pow(E,2)+pow(E,2)))*4
                    self.time_cutting = self.time_cutting + (distance / F)
                    # distace = 2*width + 2*hight
                    distance = 4*p15+4*p14+Rad_fr-8*E
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Code X#19Y#25
                    distance = math.sqrt(pow((p19-tek_pos),2)+pow(Rad_fr,2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Code X#19Y#25
            distance = math.sqrt(pow((W-V),2))
            self.time_cutting = self.time_cutting + (distance / 4000)
            X_Y_point['X'] = p19
            X_Y_point['Y'] = Y2
            X_Y_point['Z1'] = V            
        return X_Y_point

                     
    def P47_loop(self,X1,X2,Y1,Y2,Z1,Z2,V,W,D,R,F,J,Q,U,Rad_fr):
        X_Y_point ={}
        if U != 0:
            Q = (abs(W - Z2)) / U
        # p12 -> #12 KOL-VO PROHODOV
        p12 = math.ceil((abs(W-Z2))/Q)
        # Code G40G1Z#22F4000M8M138
        distance = math.sqrt(pow((V-Z1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        # Code X#24Y#25
        distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        # Code Z[#28+1]F1000
        distance = math.sqrt(pow((Z2 + 1 - Z1),2))
        self.time_cutting = self.time_cutting + (distance / 1000)
        Z1 = Z2 + 1
        if J == 1:
            # Code Z#28F500
            distance = 1
            self.time_cutting = self.time_cutting + (distance / 500)
            # Code Z#28F1000
            distance = math.sqrt(pow((W-Z1-1),2))
            self.time_cutting = self.time_cutting + (distance / 1000)
            # Code Z#22F4000
            distance = math.sqrt(pow((Z2-V),2))
            self.time_cutting = self.time_cutting + (distance / 4000)
        else:
            # Code Z#23F500
            distance = math.sqrt(pow((W - Z1),2))
            self.time_cutting = self.time_cutting + (distance / 500)
            # Code Z#28F1000
            distance = math.sqrt(pow((W-Z1-1),2))
            self.time_cutting = self.time_cutting + (distance / 1000)
            # Code Z#22F4000
            distance = math.sqrt(pow((Z2-V),2))
            self.time_cutting = self.time_cutting + (distance / 4000)            
        # Code G1G41X[#24+[#7/2]]F#9 twice
        distance = 2*(math.sqrt(pow((D / 2 - Rad_fr),2)))
        self.time_cutting = self.time_cutting + (distance / F)
        # Code G3I[-1*[#7/2]]
        distance = 4 * math.pi * (D/2 - Rad_fr)
        self.time_cutting = self.time_cutting + (distance / F)
        # Code G3X[#24+[#18/2]]Y#25Z#23I[-1*[#7/2]]J0K[-1*#17]F#9
        distance = (math.pi * p12 * (D + R - 4*Rad_fr)) / 2
        self.time_cutting = self.time_cutting + (distance / F)
        # Code G3I[-1*[#18/2]]
        distance = 4 * math.pi * (R/2 - Rad_fr)
        self.time_cutting = self.time_cutting + (distance / F)
        X_Y_point['X'] = X2
        X_Y_point['Y'] = Y2
        X_Y_point['Z1'] = V            
        return X_Y_point


    def P62_loop(self,X1,X2,Y1,Y2,Z1,Z2,V,W,A,B,R,F,I,Q,U,Rad_fr):
        X_Y_point ={}
        if U != 0:
            Q = (abs(W - Z2)) / U
        # p12 -> #12 KOL-VO PROHODOV
        p12 = math.ceil((abs(W-Z2))/Q)
        p3 = I * 0.01 * F
        p28 = Q * p12 + W
        p5 = math.floor(A / (Rad_fr * 2))
        p7 = math.floor(B / (Rad_fr * 2))
        p6 = 1
        A = A / 2
        B = B / 2
        p19 = 0
        p27 = R
        if R == Rad_fr:
            p19 = 1
        # Code G40G1Z#22F4000M8M138
        distance = math.sqrt(pow((V-Z1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        if p5 >= p7:
            p16 = p7
            # Code G1X[#24-#1+[#12001]+[#13001]+0.1]Y#25
            distance = math.sqrt(pow((X1-(X2-A+Rad_fr+0.1)),2)+pow((Y2-Y1),2))
            self.time_cutting = self.time_cutting + (distance / 4000)
            # Code G1Z[#28+1]F1000
            distance = math.sqrt(pow((p28+1-V),2))
            self.time_cutting = self.time_cutting + (distance / 1000)
            # Code G1Z[#28+0.1]F500
            distance = 0.9
            self.time_cutting = self.time_cutting + (distance / 500)
            while p12 >= 1:
                p12 -= 1
                p28 -= Q
                if p19 !=0:
                    R = 0
                # Code G1Z#28X[#24+#1-[#12001]-[#13001]-0.1]F#3
                distance = math.sqrt(pow((A*2-0.2-Rad_fr*2),2)+pow(Q,2))
                self.time_cutting = self.time_cutting + (distance / p3)
                X1 = X2 + A - Rad_fr - 0.1
                while p7 > 0:
                    p7 -= 1
                    p14 = A - p7*Rad_fr
                    p15 = B - p7*Rad_fr
                    if p19 != 0:
                        if R < p27:
                            R = R + Rad_fr
                        if R > p27:
                            R = p27
                        if p7 == 0:
                            R = p27
                    distance = math.sqrt(pow((X1-(X2-p14-Rad_fr)),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    # distace = 2pR
                    F_last = F
                    if p7 == 0:
                        F_last = F*0.2
                    distance = 2*math.pi*(R-Rad_fr)
                    self.time_cutting = self.time_cutting + (distance / F_last)
                    # distace = 2*width + 2*hight
                    distance = 5*p15+4*p14-5*R
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Code G40X#24Y#25
                    distance = math.sqrt(pow((p14+Rad_fr),2)+pow((p15-R),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    X1 = X2
                p7 = p16
                # Code G1X[#24-#1+[#12001]+[#13001]+0.1]
                distance = math.sqrt(pow((A-Rad_fr-0.1),2))
                self.time_cutting = self.time_cutting + (distance / F)
        else:
            p16 = p5
            # Code G1X#24Y[#25+#2-[#12001]-[#13001]-0.1]
            distance = math.sqrt(pow((X1-X2),2)+pow((Y1-(Y2+B-0.1-Rad_fr)),2))
            self.time_cutting = self.time_cutting + (distance / 4000)
            # Code G1Z[#28+1]F1000
            distance = math.sqrt(pow((p28+1-V),2))
            self.time_cutting = self.time_cutting + (distance / 1000)
            # Code G1Z[#28+0.1]F500
            distance = 0.9
            self.time_cutting = self.time_cutting + (distance / 500)
            while p12 >= 1:
                p12 -= 1
                p28 -= Q
                if p19 !=0:
                    R = 0
                # Code G1Z#28Y[#25-#2+[#12001]+[#13001]+0.1]F#3
                distance = math.sqrt(pow((B*2-0.2-Rad_fr*2),2)+pow(Q,2))
                self.time_cutting = self.time_cutting + (distance / p3)
                Y1 = Y2 - B + Rad_fr + 0.1
                while p5 > 0:
                    p5 -= 1
                    p14 = A - p5*Rad_fr
                    p15 = B - p5*Rad_fr
                    if p19 != 0:
                        if R < p27:
                            R = R + Rad_fr
                        if R > p27:
                            R = p27
                        if p5 == 0:
                            R = p27
                    distance = math.sqrt(pow((Y1-(Y2+p15-Rad_fr)),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    # distace = 2pR
                    F_last = F
                    if p5 == 0:
                        F_last = F*0.3
                    distance = 2*math.pi*(R-Rad_fr)
                    self.time_cutting = self.time_cutting + (distance / F_last)
                    # distace = 2*width + 2*hight
                    distance = 4*p15+5*p14-5*R
                    self.time_cutting = self.time_cutting + (distance / F)
                    # Code G40X#24Y#25
                    distance = math.sqrt(pow((p15+Rad_fr),2)+pow((p14-R),2))
                    self.time_cutting = self.time_cutting + (distance / F)
                    Y1 = Y2
                p5 = p16
                # Code G1Y[#25+#2-[#12001]-[#13001]-0.1]
                distance = math.sqrt(pow((B-Rad_fr-0.1),2))
                self.time_cutting = self.time_cutting + (distance / F)
        # Code G1Z[#22]F4000
        distance = math.sqrt(pow((W-V),2))
        self.time_cutting = self.time_cutting + (distance / 4000)            
        X_Y_point['X'] = X2
        X_Y_point['Y'] = Y2
        X_Y_point['Z1'] = V            
        return X_Y_point


    def P44_loop(self,X1,X2,Y1,Y2,Z1,Z2,V,W,M,K,E,S,Rad_fr):
        X_Y_point ={}
        distance = math.sqrt(pow((X2-X1),2)+pow((Y2-Y1),2))
        self.time_cutting = self.time_cutting + (distance / 3000)
        if K == 0:
            if M == 1.4:
                K = 0.3
            if M == 1.6:
                K = 0.35
            if M == 2:
                K = 0.4
            if M == 2.5:
                K = 0.45
            if M == 3:
                K = 0.5
            if M == 4:
                K = 0.7
            if M == 5:
                K = 0.8
            if M == 6:
                K = 1
            if M == 8:
                K = 1.25
            if M == 10:
                K = 1.5                
            if M == 12:
                K = 1.75
            if M == 14 or M == 16 or M == 18:
                K = 2
            if M == 20:
                K = 2.5
        if K == 0:
            K = 0.5
        F = 0.01            
        if M <= 3.5:
            F = 0.01
        if M == 4:
            F = 0.02
        if M == 5:
            F = 0.028
        if M == 6:
            F = 0.035
        if M == 8 or M == 10:
            F = 0.04
        if M > 10:
            F = 0.08
        p5 = Rad_fr*2
        p3 = F * E * S
        p4 = ((M - p5)*p3) / M
        p17 = math.ceil(abs(Z2-W)/K)+1
        p21 = p17 * K
        # Code G1Z[#21+#23]F1000M8M138
        distance = math.sqrt(pow((V-(p21+W)),2))
        self.time_cutting = self.time_cutting + (distance / 1000)
        # Code G1Z#23F300
        distance = math.sqrt(pow(p21,2))
        self.time_cutting = self.time_cutting + (distance / 300)
        # Code #10=[[#13/2]-[#12001]]*0.3
        p10 = (M/2 - Rad_fr)*0.3
        p11 = M/2 - p10
        p20 = X2 + p11
        # Code G41X#20F10
        distance = math.sqrt(pow((X2-p20),2))
        self.time_cutting = self.time_cutting + (distance / 10)
        # Dlinna prugini L=n*sqrt((p*D)^2+t^2)
        # Where n - chislo vitkov, t - shag prugini, D - diametr
        # Code G03I[-1*#11]Z[#21+#23]K#6F#4
        distance = p17 * math.sqrt(pow((math.pi*(p11 - Rad_fr)*2),2) + pow(K,2))
        self.time_cutting = self.time_cutting + (distance / p4)
        # Code G1G40X#1F100
        distance = math.sqrt(pow((X2-p20),2))
        self.time_cutting = self.time_cutting + (distance / 100)
        # Code G1Z#23F300
        distance = math.sqrt(pow((Z2-W),2))
        self.time_cutting = self.time_cutting + (distance / 300)
        p11 = M / 2 - Rad_fr
        # Code G41X#20F10 - 5 times
        distance = math.sqrt(pow(p11,2))*5
        self.time_cutting = self.time_cutting + (distance / 10)
        # Code G03I[-1*#11]Z[#21+#23]K#6F#4 - 5 times
        distance = (p17 * math.sqrt(pow((math.pi*p11*2),2) + pow(K,2)))*5
        self.time_cutting = self.time_cutting + (distance / p4)
        # Code G1G40X#1F100 - 5 times
        distance = math.sqrt(pow(p11,2))*5
        self.time_cutting = self.time_cutting + (distance / 100)
        # Code G1Z#23F300 - 4 times
        distance = math.sqrt(pow((Z2-W),2))
        self.time_cutting = self.time_cutting + (distance / 300)
        # Code G1Z#22F3000
        distance = math.sqrt(pow((V-Z2),2))
        self.time_cutting = self.time_cutting + (distance / 3000)
        X_Y_point['X'] = X2
        X_Y_point['Y'] = Y2
        X_Y_point['Z1'] = V        
        return X_Y_point


    def P63_loop(self,X1,X2,Y1,Y2,Z1,Z2,V,W,A,B,R,F,K,Q,U,Rad_fr):
        X_Y_point ={}
        if U != 0:
            Q = (abs(W - Z2)) / U
        # p12 -> #12 KOL-VO PROHODOV
        p12 = math.ceil((abs(W-Z2))/Q)
        p28 = Q * p12 + W
        A = A / 2
        B = B / 2
        p19 = X2 - A + Rad_fr + K
        # Code G40G1Z#22F4000
        distance = math.sqrt(pow((V-Z1),2))
        self.time_cutting = self.time_cutting + (distance / 4000)
        # Code G1X#19Y#25F2000M8
        distance = math.sqrt(pow((A - Rad_fr - K),2)+pow((Y1-Y2),2))
        self.time_cutting = self.time_cutting + (distance / 2000)
        # Code G1Z[#28+1]F1000
        distance = math.sqrt(pow((V-p28),2))
        self.time_cutting = self.time_cutting + (distance / 1000)
        p4 = 0
        if B - R <= Rad_fr:
            p4 = Y2 - B + R
        else:
            p4 = Y2 - Rad_fr
        while p12 >= 1:
            p12 -= 1
            p28 -= Q
            # Code G1Z#28F1000
            distance = Q
            self.time_cutting = self.time_cutting + (distance / 1000)
            # Code G41X[#24-#1]F[#9/5] 
            distance = K
            self.time_cutting = self.time_cutting + (distance / (F/5))
            # distace = 2pR
            distance = 2*math.pi*(R-Rad_fr)
            self.time_cutting = self.time_cutting + (distance / (F/5))
            # distace = 2*width + 2*hight
            distance = 4*A+4*B-8*R
            self.time_cutting = self.time_cutting + (distance / F)
            # Code G1Y#4F#9
            distance = math.sqrt(pow((Y2-p4),2))
            self.time_cutting = self.time_cutting + (distance / F)
            # Code G40X#19Y#25
            distance = math.sqrt(pow((Y2-p4),2)+pow((K+Rad_fr),2))
            self.time_cutting = self.time_cutting + (distance / F)
        # Code G1Z[#22]F4000
        distance = math.sqrt(pow((V-W),2))
        self.time_cutting = self.time_cutting + (distance / 4000)            
        X_Y_point['X'] = X2
        X_Y_point['Y'] = Y2
        X_Y_point['Z1'] = V            
        return X_Y_point
    

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


    # Read arguments from line
    def count_alfa(self,X1,X2,X3,Y1,Y2,Y3):
        alfa = 0
        a = math.sqrt(pow((X1-X3),2)+pow((Y1-Y3),2))
        b = math.sqrt(pow((X1-X2),2)+pow((Y1-Y2),2))
        c = math.sqrt(pow((X2-X3),2)+pow((Y2-Y3),2))
        alfa = math.degrees(math.acos((pow(b,2)+pow(c,2)-pow(a,2)) / (2 * b * c)))
        return alfa


    # Read # means
    def par_reader(self,stroka):
        name_par = stroka.partition('=')[0]
        mean_par = ''
        i = stroka.find('=') + 1
        j = i
        while i < len(stroka):
            if stroka[i] == '(':
                i = len(stroka)
            else:
                mean_par = mean_par + stroka[i]
            i += 1
        self.param[name_par] = float(mean_par)
        return None


    # Make new mean for parametr
    def make_newMean(self,stroka):
        name_par = stroka.partition('=')[0]
        second_part = stroka.partition('=')[2]
        stroka2 = second_part.partition(name_par)[2]
        mean_par = stroka2[1:]
        sign = stroka2[0]
        if '(' in mean_par:
            mean_par = mean_par.partition('(')[0]
        if sign == '-':
            decimal.getcontext().prec = 4
            self.param[name_par] = float(Decimal(self.param[name_par]) - Decimal(mean_par))
        elif sign == '+':
            self.param[name_par] = self.param[name_par] + float(mean_par)
        return None


    # Count time for milling 
    def millingGOTO_time(self):
        i = 0
        marker = 0
        while marker == 0:
            if 'G201' in self.Myblock[i]:
                marker = 1
            i += 1

        while i < len(self.Myblock)-2:
            if self.Myblock[i] == '\n' or self.Myblock[i][0] == ' ' or self.Myblock[i][0] == '(':
                i += 1
            elif self.Myblock[i][0] == '#' and self.Myblock[i].count('#') == 1:
                self.par_reader(self.Myblock[i])
                i += 1
            elif self.Myblock[i][0] == 'N':
                i = self.make_millingBlock(i)
                
            else:
                i += 1
        return self.time_cutting


    # Make fulll simple sting without variables
    def read_Mysting(self,stroka):
        numbers_par = '0123456789'
        new_stroka = ''
        i = 0
        j = 0
        while i < len(stroka):
            if stroka[i] == '(':
                j = i + 1
                while j < len(stroka):
                    if stroka[j] != ')':
                        j += 1
                    else:
                        i = j + 1
                        j = len(stroka)
            elif stroka[i] == '#':
                par = '#'
                j = i + 1
                while stroka[j] in numbers_par:
                    par = par + stroka[j]
                    j += 1
                i = j
                new_stroka = new_stroka + str(self.param[par])
            else:
                new_stroka = new_stroka + stroka[i]
                i += 1
        return new_stroka


    # Find and make block with begin = N11 and ending = IF[#106GT0]GOTO11 
    def make_millingBlock(self,i):
        i += 1
        goto_block = []
        while self.Myblock[i][0] != 'I':
            goto_block.append(self.Myblock[i])
            i += 1
        goto_block.append(self.Myblock[i])
        simple_block = []
        stroka = goto_block[(len(goto_block)-1)].partition('#')[2]
        par = '#' + stroka.partition('GT')[0]
        j = self.param[par]
        while j > 0:
            k = 0
            while k < len(goto_block):
                if goto_block[k].count('=') > 0 and goto_block[k].count('#') > 1:
                    self.make_newMean(goto_block[k])
                    k += 1
                elif (goto_block[k][0] == '\n' or goto_block[k][0] == ' '
                      or goto_block[k][0] == '(' or goto_block[k][0] == 'I'):
                    k += 1
                elif len(goto_block[k]) >= 3 and goto_block[k][:3] == 'G31':
                    k += 1
                else:
                    new_stroka = self.read_Mysting(goto_block[k])
                    simple_block.append(new_stroka)
                    k += 1
            j -= 1
        self.count_simple(simple_block)
        return i + 1


    # count time for simple way
    def count_simple(self,simple_block):
        numbers = '-0123456789.'        
        mode_g = 'G1'
        group_07 = 'G40'
        old_group_07 = 'G40'
        X1 = 0.0 #old X
        X2 = 0.0 #new X
        X3 = 0.0 #will be in next position
        Y1 = 0.0
        Y2 = 0.0
        Y3 = 0.0
        Z1 = 0.0
        Z2 = 0.0
        F = 0.0
        R = 0.0
        arguments_1 = []
        arguments_2 = []
        arguments_3 = []
        i = 0
        while i < len(simple_block)-2:
            if simple_block[i] == '\n' or simple_block[i][0] == ' ' or simple_block[i][0] == '(':
                i += 1
            else:
                X1 = X2
                Y1 = Y2
                Z1 = Z2
                old_group_07 = group_07
                if 'G1' in simple_block[i]:
                    mode_g = 'G1'
                elif 'G2' in simple_block[i]:
                    mode_g = 'G2'
                elif 'G3' in simple_block[i]:
                    mode_g = 'G3'
                elif 'G0' in simple_block[i]:
                    mode_g = 'G0'
                if 'G41' in simple_block[i] or 'G42'in simple_block[i]:
                    group_07 = 'G41'
                elif 'G40' in simple_block[i]:
                    group_07 = 'G40'
                arguments_2 = self.arg_read(simple_block[i])
                for j in arguments_2:
                    if 'X' in j:
                        X2 = float(j[1:])
                    elif 'Y' in j:
                        Y2 = float(j[1:])
                    elif 'Z' in j:
                        Z2 = float(j[1:])
                    elif 'R' in j:
                        R = float(j[1:])
                    elif 'F' in j:
                        F = float(j[1:])
                try:
                    if (old_group_07 == group_07) and group_07 == 'G40':
                        if mode_g == 'G1':
                            distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))
                            self.time_cutting = self.time_cutting + (distance / F)
                        if mode_g == 'G2' or mode_g == 'G3':
                            distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))
                            angle = ((math.acos(distance / (2 * R))) * 180) / math.pi
                            dis_angl = (math.pi * R * (180 - 2 * angle) )/ 180
                            self.time_cutting = self.time_cutting + (dis_angl / F)                        
                    elif (old_group_07 != group_07) and group_07 == 'G41':
                        distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))-self.radius_f
                        self.time_cutting = self.time_cutting + (distance / F)
                    elif (old_group_07 == group_07) and group_07 == 'G41':
                        add_distanse = 0
                        if 'G40' not in simple_block[i+1]:
                            if 'X' in simple_block[i+1] or 'Y' in simple_block[i+1] and simple_block[i+1][0] != '(':
                                arguments_3 = self.arg_read(simple_block[i+1])
                                for j in arguments_3:
                                    if 'X' in j:
                                        X3 = float(j[1:])
                                    elif 'Y' in j:
                                        Y3 = float(j[1:])
                                    elif 'Z' in j:
                                        Z3 = float(j[1:])
                                if 'X' in simple_block[i+1] and X3 < X2:
                                    betta = 180.0 - (self.count_alfa(X1,X2,X3,Y1,Y2,Y3))
                                    add_distance = (1/(360 / betta)) * 2 * math.pi * self.radius_f
                                elif 'X' in simple_block[i+1] and X3 > X2:
                                    alfa = self.count_alfa(X1,X2,X3,Y1,Y2,Y3)
                                    if alfa < 180:
                                        add_distanse = -2 * (self.radius_f / (math.atan(alfa / 2)))
                        distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))
                        distance = distance + add_distanse
                        self.time_cutting = self.time_cutting + (distance / F)
                    else:
                        distance = math.sqrt(pow((X2-X1),2) + pow((Y2-Y1),2) + pow((Z2-Z1),2))-self.radius_f
                        self.time_cutting = self.time_cutting + (distance / F)                        
                except:
                    self.time_cutting = self.time_cutting + 0                
                i += 1
        return self.time_cutting

