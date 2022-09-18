import sqlite3

import datetime

from sqlite3 import Error

way = 'mydatabase.db'

def sql_connection():
    try:
        cont = sqlite3.connect(way)
        return cont
    except Error:
        print(Error)


def make_Det(My_block, atr_b, my_tool, name_table,total_time,material):
    name_IZD = name_table.partition('.')[0]
    name_table = name_table.replace('.','_')
    name_table = name_table.replace('-','__')
    con = sql_connection()
    if check_existTable(con, name_table) == 0:
        create_Newtable(con,name_table)
    else:
        sql_deltab(con, name_table)
        create_Newtable(con,name_table)
    i = 0
    while i < len(My_block):
        entities = []
        if atr_b[i].title == 'title' or atr_b[i].title == 'Ren_150' or atr_b[i].title == 'Ren_200':
            i += 1
        else:
            entities.append(My_block[i][0].rstrip('\n'))
            if atr_b[i].title == 'Drill':
                entities.append('DRILL')
            else:
                entities.append('MILL')
            entities.append(str(my_tool[int(atr_b[i].tool)-1].DValue))
            entities.append(str(my_tool[int(atr_b[i].tool)-1].LValue))
            entities.append(str(my_tool[int(atr_b[i].tool)-1].ToolId))
            entities.append(str(my_tool[int(atr_b[i].tool)-1].ConeId))
            time_second = atr_b[i].time_cutting - int(atr_b[i].time_cutting)
            time_second = int(time_second * 60)
            all_time = str(int(atr_b[i].time_cutting)) + ':'
            all_time = all_time + str(time_second)
            entities.append(all_time)
            entities.append(name_IZD)
            entities.append(1)
            entities.append('29.11.2021')
            entities.append(material)
            entities.append(int(total_time))
            sql_insert(con, entities, name_table)
            i += 1
    con.close()
    
    

def create_Newtable(con, name_table):
    cursorObj = con.cursor()
    cursorObj.execute('''CREATE TABLE {0}(number_k text PRIMARY KEY,
                      tip_instr text,
                      diametr text,
                      dlina text,
                      index_fr text,
                      index_con text,
                      time_cut text,
                      number_IZD text,
                      sdelal_det integer,
                      data text,
                      material text,
                      total_time text)'''.format(name_table))
    con.commit()

def sql_insert(con, entities, name_table):
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO {0}(number_k,
                      tip_instr,
                      diametr,
                      dlina,
                      index_fr,
                      index_con,
                      time_cut,
                      number_IZD,
                      sdelal_det,
                      data,
                      material,
                      total_time)VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'''.format(name_table),entities)
    con.commit()

def sql_update(con, id_n):
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE employees SET name = "Roman" where id = {0}'.format(id_n))
    con.commit()

def sql_deltab(con, name_table):
    cursorObj = con.cursor()
    cursorObj.execute('DROP table if exists {0}'.format(name_table))
    con.commit()    

def check_existTable(con, name_table):
    cursorObj = con.cursor()
    cursorObj.execute('''SELECT name from sqlite_master where type="table" AND name="{0}"'''.format(name_table))
    if len(cursorObj.fetchall()) >= 1:
        return 1
    else:
        return 0

    
def sql_show(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT number_k FROM EQSAT_2578__06')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)
    con.commit()    





