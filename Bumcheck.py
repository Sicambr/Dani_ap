import os
import sys

import block_macker
import tool_maker
import find_mistakes
import Feed_rate
import Run_cuttime
import Rude_mistakes
import G304_maker
import customise_tool
import programm_tool
import Set_customise
import Loop_creator


from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtWinExtras import QtWin
from typing import List, Final
from PyQt5.QtCore import QSize, QStringListModel, Qt
from PyQt5.QtGui import QTextCursor, QIcon, QTextDocument, QFont, QPixmap


def main_time_count(i,j,block,m,My_tool,title):
    block[j].loop_arg = m.loop_arg
    # Count run time for milling and drilling
    diametr_f = My_tool[int(block[j].tool) - 1].DValue
    run_t = Run_cuttime.Run_timer(i, block[j].title, m.param, diametr_f)
    block[j].time_cutting = run_t.first_time()

#Make data tools from CATALOG
def create_new_tools():
    My_tool.clear()
    i = 0
    tool_file = tool_maker.Tool_maker.read_toolTable(way_tools)
    while i < tool_maker.Tool_maker.count_tool(tool_file):
        My_tool.append(tool_maker.Tool_maker(i))
        My_tool[i].Make_new_tool(i,tool_file)
        i += 1
    return tool_file

# Make blocks with titels
def create_new_blocks(My_blocks,block,MyOld_file):
    k = 0
    i = 0
    while k < len(MyOld_file):
        if len(My_blocks) == 0:
            block.append(block_macker.Block_macker(MyOld_file))
            My_blocks.append(block[i].title_block())
            k = len(My_blocks[0])-1
        else:
            block.append(block_macker.Block_macker(MyOld_file[k:]))
            My_blocks.append(block[i].common_block())
            k = k + len(My_blocks[i]) - 1
        i += 1
        k += 1

#Customise tool to blocks
def create_new_customiseT(My_blocks,block):
    i = 0
    while i < len(My_blocks):
        tol = customise_tool.Customise_tool(My_blocks[i],block[i].title,My_tool)
        block[i].tool = tol.set_tool()
        i += 1

# Delete empty lines in begin
# Make first renumeration
# Add M0 to te end of blocks, replace wrong parenthesis
def create_new_units(My_blocks,block):
    j = 0
    for i in My_blocks:
        if j > 0:
            block[j].first_n = (int(block[j-1].last_n / 10) + 1) * 10
            k = find_mistakes.Block_mist(i,block[j].title,block[j].first_n)
            #First renumeration
            i = k.first_renum()
            block[j].last_n = k.last_n
            i = k.rep_parenthesis()
            # Customise offset G304
            of_replace = G304_maker.Offset_maker(i,block[j].title)
            i = of_replace.g304_offset()
            # Check rude mistakes and customise list of arguments
            diametr_f = 0
            if (int(block[j].tool)-1)>=0 and (int(block[j].tool)-1)<=(tool_maker.Tool_maker.count_tool(tool_file)-1):
                diametr_f = My_tool[int(block[j].tool)-1].DValue
            m = Rude_mistakes.Rude_mist(i,block[j].title,block[j].tool,diametr_f)
            m.rude_mist()
            block[j].mistakes = m.rude_mistakes
            if of_replace.mistakes['total'] != 0 :
                mis = block[j].mistakes['total']
                block[j].mistakes['total'] = block[j].mistakes['total'] + of_replace.mistakes['total']
                block[j].mistakes[mis + 1] = of_replace.mistakes[1]
            block[j].warning_m = m.warning_m
            block[j].milling_mode = m.milling_mode
            block[j].loops_names = m.loops_names
            if block[j].mistakes['total'] == 0:
                main_time_count(i, j, block, m, My_tool, block[j].title)
        else:
            k = find_mistakes.Block_mist(i,block[j].title)
            i = k.rep_parenthesis()
            # Customise offset G304
            of_replace = G304_maker.Offset_maker(i,block[j].title)
            i = of_replace.g304_title()
            block[0].mistakes = {'total': 0}
        j += 1

#Delete empty spaces between N and below
def create_empty_spaces(My_blocks,block):
    i = 1
    while i < len(My_blocks):
        first_mes = len(My_blocks[i])
        My_blocks[i] = block_macker.kill_emptySpaces(My_blocks[i])
        second_mes = len(My_blocks[i])
        if first_mes != second_mes and block[i].mistakes['total'] != 0:
            block[i].mistakes = block_macker.rename_mistakes(block[i].mistakes,(first_mes-second_mes))
        i += 1

#Start app widget and splash
#if __name__ == '__main__':
app = QApplication([])
app.setWindowIcon(QIcon('koala.png'))
# Create loading screen
splash = QtWidgets.QSplashScreen(QtGui.QPixmap('pictures/Dani_panda.jpg'))
splash.show()

# Load settings from maing config file
way_tools = Set_customise.Customise_ToolWay()
# Directory of files
way = Set_customise.Directory_files()

My_tool = []
otkat_text = []
old_title = ''
My_blocks = []
block = []
total_time = 0
MyOld_file = []
name_of_file = ''
file_without_changing = ''
tool_file = []

if way_tools != 'Неправильный путь для .json файла':
    tool_file = create_new_tools()
    # List of files in directory
    if way != 'Несуществующий каталог':
        f_home = list(os.listdir(way))
        # Read all stings from file
        if len(f_home) > 0:
            name_of_file = f_home[0]
            for line in open(way + '\\' + name_of_file):MyOld_file.append(line)
    file_without_changing = MyOld_file.copy()
    create_new_blocks(My_blocks,block,MyOld_file)
    create_new_customiseT(My_blocks,block)
    create_new_units(My_blocks,block)
    create_empty_spaces(My_blocks,block)
#Variables or open text
current_Textp = Set_customise.My_current_page(0,0,0,0,59,name_of_file,way,file_without_changing)
tool_file2 = tool_maker.Tool_maker.read_toolTable(way_tools)
current_Textp.tool_amount = tool_maker.Tool_maker.count_tool(tool_file2) - 1

#add information from my DATA to detail tools table
"""
name_table = 'EQSAT.2578-02'
material = ['ALUMINIUM','STEEL','TITAN','BRASS','COPPER','32NKD']
programm_tool.make_Det(My_blocks, block, My_tool,name_table,total_time,material[0])
"""
# Get means of Feed rate
"""
old_f = '1440'
new_f = '4000'
numb = 19
feed = Feed_rate.feed_r(My_blocks[numb],block[numb].title)
block[numb].feed = feed.feed_mesuare()
My_blocks[numb] = feed.feed_rep(block[numb].title, old_f, new_f)
"""
# total_time - safes full time of milling and drilling
#print('Total Time = ', total_time)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('Firs_form.ui', self) # Load the .ui file
        theSizeText= 14
        theSizeButtons = 12
        self.txtEdit = self.findChild(QTextEdit, 'textEdit')
        self.doc_page = QTextDocument()
        self.txtEdit.setDocument(self.doc_page)
        self.txtEdit.setFont(QFont('Arial',theSizeText))
        # Set Icon for my window
        self.setWindowTitle('DANI v.1.32   <' + str(way + name_of_file) + '>')
        ico = QIcon('koala.png')
        self.setWindowIcon(ico)
        # Change setting for customise my application icon in bottom windows panel
        # By default all application's icons have python icons
        myappid = 'mycompany.myproduct.subproduct.version'  # !!!
        QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
        self.layout = QVBoxLayout()
        self.buttons_menu: List[QPushButton] = []
        self.labels_menu7: List[QWidget] = []
        wdg = self.findChild(QWidget, 'scrollAreaWidgetContents')
        for n in range(len(My_blocks)):
            self.make_new_rightside(n, 'add')
            self.button = QPushButton(str(My_blocks[n][1].rstrip('\n')))
            self.button.setMinimumHeight(35)
            self.button.setMaximumWidth(569)
            self.button.setFont(QFont('Arial',theSizeButtons))
            self.buttons_menu.append(self.button)
            if n > 0 and block[n].mistakes['total'] != 0:
                self.button.setStyleSheet("QPushButton {color: red}")
            self.button.pressed.connect(lambda n=n: self.btn_Press(n))
            self.layout.addWidget(self.button)
            #self.layout.addSpacing(25)
        wdg.setLayout(self.layout)
        self.first_open()

        if way_tools == 'Неправильный путь для .json файла':
            self.attention_message()
        #connect signal that we edit text in page
        self.txtEdit.textChanged.connect(self.Text_changed)


        #Make button save file button
        self.Save_button = self.findChild(QPushButton, 'SaveButton')
        self.Save_button.pressed.connect(self.save_newFile)
        ico_sbutton = QIcon('Icons_milling/saved.png')
        if self.compare_original_file() != 0:
            ico_sbutton = QIcon('Icons_milling/not_save.png')
            current_Textp.switch_check = 1
        self.Save_button.setIconSize(QSize(44, 44))
        self.Save_button.setIcon(ico_sbutton)
        self.Save_button.setToolTip('СОХРАНИТЬ СДЕЛАННЫЕ ИЗМЕНЕНИЯ')

        #Make button for reload page
        self.Reload_button = self.findChild(QPushButton, 'ReloadButton')
        self.Reload_button.pressed.connect(self.Reload_page)
        ico_Rbutton = QIcon('Icons_milling/processing.png')
        self.Reload_button.setIconSize(QSize(44, 44))
        self.Reload_button.setIcon(ico_Rbutton)
        self.Reload_button.setToolTip('ПРОВЕРИТЬ КАДР')

        #Make button for replaced S in all blocks with the same tool
        self.S_button = self.findChild(QPushButton, 'ZamenaFS')
        self.S_button.pressed.connect(self.All_SReplace)
        self.S_button.setToolTip('УСТАНАВЛИВАЕТ ОБОРОТЫ "S" ПРОСМАТРИВАЕМОГО БЛОКА \n ДЛЯ ВСЕХ "T" С ТЕМ ЖЕ НОМЕРОМ В ДРУГИХ БЛОКАХ')
        icoSbutton = QIcon('Icons_milling/replace_S.png')
        self.S_button.setIconSize(QSize(130, 54))
        self.S_button.setIcon(icoSbutton)

        #Make button for replaced T in all blocks with the same tool
        self.T_button = self.findChild(QPushButton, 'Zamena_T')
        self.T_button.pressed.connect(self.All_TReplaceMENU)
        self.T_button.setToolTip('ЗАМЕНА НОМЕРА ИНСТРУМЕНТА "T" НА ДРУГОЙ НОМЕР ВО ВСЕХ БЛОКАХ')
        ico_Tbutton = QIcon('Icons_milling/replace_T.png')
        self.T_button.setIconSize(QSize(130, 54))
        self.T_button.setIcon(ico_Tbutton)

        #Create button for insert block before active block
        self.add_before_button = self.findChild(QPushButton, 'add_before_block')
        self.add_before_button.pressed.connect(lambda t_f = tool_file, o_t = otkat_text, o_f = old_title,\
                                                      m_f = MyOld_file, m_b = My_blocks,\
                                                      bl = block, ad_b = 1: self.add_block_before(t_f, o_t, o_f, m_f, m_b, bl, ad_b))
        self.add_before_button.setToolTip('ВСТАВИТЬ ПУСТОЙ КАДР ПЕРЕД ТЕКУЩИМ КАДРОМ')
        ico_add_before = QIcon('Icons_milling/add_beforeA.png')
        self.add_before_button.setIconSize(QSize(50, 50))
        self.add_before_button.setIcon(ico_add_before)

        #Create button for insert block before active block
        self.add_after_button = self.findChild(QPushButton, 'add_after_block')
        self.add_after_button.pressed.connect(lambda t_f=tool_file, o_t=otkat_text, o_f=old_title, \
                                                      m_f=MyOld_file, m_b=My_blocks, \
                                                      bl=block, ad_b = 2: self.add_block_before(t_f, o_t, o_f, m_f, m_b, bl, ad_b))
        self.add_after_button.setToolTip('ДОБАВИТЬ ПУСТОЙ КАДР ПОСЛЕ ТЕКУЩЕГО КАДРА')
        ico_add_after = QIcon('Icons_milling/insert_afterA.png')
        self.add_after_button.setIconSize(QSize(50, 50))
        self.add_after_button.setIcon(ico_add_after)

        #Create button for delete block
        self.delblock_button = self.findChild(QPushButton, 'delete_block')
        self.delblock_button.pressed.connect(lambda t_f=tool_file, o_t=otkat_text, o_f=old_title, \
                                                      m_f=MyOld_file, m_b=My_blocks, \
                                                      bl=block: self.delActive_block(t_f, o_t, o_f, m_f, m_b, bl))
        self.delblock_button.setToolTip('УДАЛИТЬ ПРОСМАТРИВАЕМЫЙ КАДР')
        ico_add_after = QIcon('Icons_milling/delete_colour.png')
        self.delblock_button.setIconSize(QSize(50, 50))
        self.delblock_button.setIcon(ico_add_after)

        #Create button for hole milling
        self.holemil_button = self.findChild(QPushButton, 'create_holes')
        self.holemil_button.setToolTip('СГЕНЕРИРОВАТЬ РАСТОЧКУ ОТВЕРСТИЙ ДЛЯ ПРОСМАТРИВАЕМОГО КАДРА')
        self.holemil_button.pressed.connect(lambda o_t=otkat_text, m_b=My_blocks, \
                                                    bl=block, myt = My_tool: self.holes_milling(o_t, m_b, bl, myt))
        ico_hole_mill = QIcon('Icons_milling/black_rast.png')
        self.holemil_button.setIconSize(QSize(50, 50))
        self.holemil_button.setIcon(ico_hole_mill)


        # Create button for making full form of loops
        self.fullL_button = self.findChild(QPushButton, 'full_loopForm')
        self.fullL_button.pressed.connect(self.create_full_loop)
        self.fullL_button.setToolTip('НАПИСАТЬ ЦИКЛЫ КАДРА СО ВСЕМИ АРГУМЕНТАМИ')
        ico_fullL = QIcon('Icons_milling/maximaze_A.png')
        self.fullL_button.setIconSize(QSize(50, 50))
        self.fullL_button.setIcon(ico_fullL)


        # Create button for making short form of loops
        self.shrinkL_button = self.findChild(QPushButton, 'short_loopForm')
        self.shrinkL_button.pressed.connect(self.create_short_loop)
        self.shrinkL_button.setToolTip('УБРАТЬ ПОВТОРЯЮЩИЕСЯ АРГУМЕНТЫ В ЦИКЛАХ КАДРА')
        ico_shrinkL = QIcon('Icons_milling/shrink_loop.png')
        self.shrinkL_button.setIconSize(QSize(50, 50))
        self.shrinkL_button.setIcon(ico_shrinkL)


        # Make button for creating loop from full code
        self.Make_loop = self.findChild(QPushButton, 'Create_loop')
        self.otkat_all = self.findChild(QPushButton, 'otkat')
        self.Make_loop.pressed.connect(lambda m_b = My_blocks: self.create_repetition(m_b))
        self.otkat_all.pressed.connect(self.otkat_repetit)
        self.paint_all_icons()
        self.Make_loop.setToolTip('СДЕЛАТЬ ИЗ ОБЫЧНОГО ФРЕЗЕРОВАНИЯ БЛОК С GOTO ЦИКЛОМ')
        # Make button OTKAT
        self.otkat_all.setToolTip('ОТКАТИТЬ КОНВЕРТАЦИЮ')

        #Make buttons with FEED RATE
        self.edits: List[QLineEdit] = []
        self.buttons_1: List[QPushButton] = []
        self.buttons_2: List[QPushButton] = []
        self.buttons_3: List[QPushButton] = []
        self.main_layout = QHBoxLayout(self)
        self.edits_layout = QVBoxLayout(self)
        self.btn1_layout = QVBoxLayout(self)
        self.btn2_layout = QVBoxLayout(self)
        self.btn3_layout = QVBoxLayout(self)
        self.wdg_feed = self.findChild(QWidget, 'scrollAreaWidgetContents_2')
        self.main_layout.addLayout(self.btn1_layout)
        self.main_layout.addLayout(self.edits_layout)
        self.main_layout.addLayout(self.btn2_layout)
        self.main_layout.addLayout(self.btn3_layout)
        self.wdg_feed.setLayout(self.main_layout)

        #Make buttons with mistakes
        self.mistake_button: List[QPushButton] = []
        self.btnMIS_layout = QVBoxLayout(self)
        self.wdg_mistakes = self.findChild(QWidget, 'scrollAreaWidgetContents_3')
        self.wdg_mistakes.setLayout(self.btnMIS_layout)

        #Make my progressbar
        wgt_status = self.findChild(QWidget,'widget_status')
        self.label_status = QLabel('')
        self.btn_st_lay = QVBoxLayout(self)
        self.btn_st_lay.addWidget(self.label_status, alignment=Qt.AlignHCenter)
        wgt_status.setLayout(self.btn_st_lay)

        # Make a menu action OTRKIT file
        self.otk_file = self.findChild(QMenu,'menu')
        self.otrit_new_fileQMENU = QAction('Открыть...',self)
        self.otrit_new_fileQMENU.setFont(QFont('MS Shell Dlg 2',12))
        self.otk_file.addAction(self.otrit_new_fileQMENU)
        self.otrit_new_fileQMENU.triggered.connect(lambda t_f = tool_file, o_t = otkat_text, o_f = old_title,\
                                                          m_f = MyOld_file, m_b = My_blocks,\
                                                          bl = block: self.otkrit_newfile(t_f, o_t, o_f, m_f, m_b, bl))

        # Make a menu action RABOCHAYA PAPKA
        self.nastroiky = self.findChild(QMenu, 'menu_2')
        self.rab_papka = QAction('Рабочая папка...', self)
        self.rab_papka.setFont(QFont('MS Shell Dlg 2', 12))
        self.nastroiky.addAction(self.rab_papka)
        self.rab_papka.triggered.connect(self.show_modal_papka)


        #Make graphic scene
        #self.wdg_scene = self.findChild(QWidget, 'widget')
        #self.grathcview = QGraphicsView(self.wdg_scene)
        #self.My_scene = QGraphicsScene(0,0,400,500)
        #self.grathcview.setScene(self.My_scene)


    # Create full form of loop arguments
    def create_full_loop(self):
        if (len(block) > 0 and block[current_Textp.new_Textpage].title == 'Loop' \
                and block[current_Textp.new_Textpage].mistakes['total'] == 0):
            new_spisok = self.txtEdit.toPlainText().split('\n')
            My_blocks[current_Textp.new_Textpage].clear()
            My_blocks[current_Textp.new_Textpage] = new_spisok
            My_blocks[current_Textp.new_Textpage] = block_macker.full_loopCreater(My_blocks[current_Textp.new_Textpage])
            self.txtEdit.clear()
            for j in My_blocks[current_Textp.new_Textpage]:
                self.txtEdit.append(j.rstrip('\n'))
            cursor = QTextCursor(self.txtEdit.document())
            cursor.setPosition(0)
            self.txtEdit.setTextCursor(cursor)
        return None

    # Create short form of loop arguments
    def create_short_loop(self):
        if (len(block) > 0 and block[current_Textp.new_Textpage].title == 'Loop' \
                and block[current_Textp.new_Textpage].mistakes['total'] == 0):
            new_spisok = self.txtEdit.toPlainText().split('\n')
            My_blocks[current_Textp.new_Textpage].clear()
            My_blocks[current_Textp.new_Textpage] = new_spisok
            My_blocks[current_Textp.new_Textpage] = block_macker.short_loopCreater(My_blocks[current_Textp.new_Textpage])
            self.txtEdit.clear()
            for j in My_blocks[current_Textp.new_Textpage]:
                self.txtEdit.append(j.rstrip('\n'))
            cursor = QTextCursor(self.txtEdit.document())
            cursor.setPosition(0)
            self.txtEdit.setTextCursor(cursor)
        return None


    # add block before our active block
    def holes_milling(self, otkat_text, My_blocks, block, My_tool):
        mas_titles = ['Drill']
        if (current_Textp.new_Textpage > 0 and block[current_Textp.new_Textpage].title in mas_titles\
                and block[current_Textp.new_Textpage].mistakes['total'] == 0):
            current_Textp.new_Textpage += 1
            current_Textp.old_Textpage += 1
            for n in self.buttons_menu:
                self.layout.removeWidget(n)
            self.buttons_menu.clear()
            for n in self.labels_menu7:
                self.layout.removeWidget(n)
            self.labels_menu7.clear()
            self.txtEdit.clear()
            for btn3 in self.buttons_3:
                self.btn3_layout.removeWidget(btn3)
            self.buttons_3.clear()
            for btn2 in self.buttons_2:
                self.btn2_layout.removeWidget(btn2)
            self.buttons_2.clear()
            for edit in self.edits:
                self.edits_layout.removeWidget(edit)
            self.edits.clear()
            for btn1 in self.buttons_1:
                self.btn1_layout.removeWidget(btn1)
            self.buttons_1.clear()
            for btn_mis in self.mistake_button:
                self.btnMIS_layout.removeWidget(btn_mis)
            self.mistake_button.clear()
            my_new_block = block_macker.Block_macker('')
            my_new_block.body_b = block_macker.create_boring(My_blocks,block,(current_Textp.new_Textpage-1),\
                                                             current_Textp.tool_amount,My_tool)
            my_new_block.title = 'Loop'
            block.insert(current_Textp.new_Textpage,my_new_block)
            My_blocks.insert(current_Textp.new_Textpage,my_new_block.body_b)
            tol = customise_tool.Customise_tool(My_blocks[current_Textp.new_Textpage],\
                                                block[current_Textp.new_Textpage].title, My_tool)
            block[current_Textp.new_Textpage].tool = tol.set_tool()
            #Changed here
            m = Rude_mistakes.Rude_mist(My_blocks[current_Textp.new_Textpage], \
                                        block[current_Textp.new_Textpage].title, block[current_Textp.new_Textpage].tool, \
                                        My_tool[int(block[current_Textp.new_Textpage].tool)-1].DValue)
            m.rude_mist()
            block[current_Textp.new_Textpage].mistakes = m.rude_mistakes
            block[current_Textp.new_Textpage].warning_m = m.warning_m
            block[current_Textp.new_Textpage].milling_mode = m.milling_mode
            block[current_Textp.new_Textpage].loops_names = m.loops_names
            if block[current_Textp.new_Textpage].mistakes['total'] == 0:
                main_time_count(My_blocks[current_Textp.new_Textpage], current_Textp.new_Textpage,\
                                block, m, My_tool, block[current_Textp.new_Textpage].title)
            #current_Textp.new_Textpage = 0
            #current_Textp.old_Textpage = 0
            current_Textp.switch_check = 0
            current_Textp.check_mistakesBlock = 0
            theSizeButtons = 12
            # Renum my old blocks
            My_blocks = find_mistakes.new_renum(My_blocks,block)
            for n in range(len(My_blocks)):
                self.make_new_rightside(n, 'add')
                self.button = QPushButton(str(My_blocks[n][1].rstrip('\n')))
                self.button.setMinimumHeight(35)
                self.button.setMaximumWidth(569)
                self.button.setFont(QFont('Arial', theSizeButtons))
                self.buttons_menu.append(self.button)
                if n > 0 and block[n].mistakes['total'] != 0:
                    self.button.setStyleSheet("QPushButton {color: red}")
                self.button.pressed.connect(lambda n=n: self.btn_Press(n))
                self.layout.addWidget(self.button)
            self.buttons_menu[current_Textp.new_Textpage].setStyleSheet("QPushButton { background-color: grey }")
            for j in My_blocks[current_Textp.new_Textpage]:
                self.txtEdit.append(j.rstrip('\n'))
            cursor = QTextCursor(self.txtEdit.document())
            cursor.setPosition(0)
            self.txtEdit.setTextCursor(cursor)
            otkat_text.clear()
            self.paint_all_icons()

    # delete active block
    def delActive_block(self, tool_file, otkat_text, old_title, MyOld_file, My_blocks, block):
        if current_Textp.new_Textpage > 0:
            status_stroka = 'УДАЛЕНИЕ БЛОКА ' + My_blocks[current_Textp.new_Textpage][0].rstrip('\n') + '...'
            self.label_status.setText(status_stroka)
            qApp.processEvents()
            self.label_status.clear()
            for n in self.buttons_menu:
                self.layout.removeWidget(n)
            self.buttons_menu.clear()
            for n in self.labels_menu7:
                self.layout.removeWidget(n)
            self.labels_menu7.clear()
            self.txtEdit.clear()
            for btn3 in self.buttons_3:
                self.btn3_layout.removeWidget(btn3)
            self.buttons_3.clear()
            for btn2 in self.buttons_2:
                self.btn2_layout.removeWidget(btn2)
            self.buttons_2.clear()
            for edit in self.edits:
                self.edits_layout.removeWidget(edit)
            self.edits.clear()
            for btn1 in self.buttons_1:
                self.btn1_layout.removeWidget(btn1)
            self.buttons_1.clear()
            for btn_mis in self.mistake_button:
                self.btnMIS_layout.removeWidget(btn_mis)
            self.mistake_button.clear()
            del My_blocks[current_Textp.new_Textpage]
            del block[current_Textp.new_Textpage]
            #current_Textp.new_Textpage = 0
            #current_Textp.old_Textpage = 0
            current_Textp.switch_check = 0
            current_Textp.check_mistakesBlock = 0
            theSizeButtons = 12
            # Renum my old blocks
            My_blocks = find_mistakes.new_renum(My_blocks,block)
            for n in range(len(My_blocks)):
                self.make_new_rightside(n, 'add')
                self.button = QPushButton(str(My_blocks[n][1].rstrip('\n')))
                self.button.setMinimumHeight(35)
                self.button.setMaximumWidth(569)
                self.button.setFont(QFont('Arial', theSizeButtons))
                self.buttons_menu.append(self.button)
                if n > 0 and block[n].mistakes['total'] != 0:
                    self.button.setStyleSheet("QPushButton {color: red}")
                self.button.pressed.connect(lambda n=n: self.btn_Press(n))
                self.layout.addWidget(self.button)
            self.buttons_menu[current_Textp.new_Textpage].setStyleSheet("QPushButton { background-color: grey }")
            for j in My_blocks[current_Textp.new_Textpage]:
                self.txtEdit.append(j.rstrip('\n'))
            cursor = QTextCursor(self.txtEdit.document())
            cursor.setPosition(0)
            self.txtEdit.setTextCursor(cursor)
            otkat_text.clear()
            self.paint_all_icons()


    # add block before our active block
    def add_block_before(self, tool_file, otkat_text, old_title, MyOld_file, My_blocks, block, position_b):
        if (current_Textp.new_Textpage > 0 and position_b == 1) \
                or (position_b == 2):
            if position_b == 2:
                current_Textp.new_Textpage += 1
                current_Textp.old_Textpage += 1
            for n in self.buttons_menu:
                self.layout.removeWidget(n)
            self.buttons_menu.clear()
            for n in self.labels_menu7:
                self.layout.removeWidget(n)
            self.labels_menu7.clear()
            self.txtEdit.clear()
            for btn3 in self.buttons_3:
                self.btn3_layout.removeWidget(btn3)
            self.buttons_3.clear()
            for btn2 in self.buttons_2:
                self.btn2_layout.removeWidget(btn2)
            self.buttons_2.clear()
            for edit in self.edits:
                self.edits_layout.removeWidget(edit)
            self.edits.clear()
            for btn1 in self.buttons_1:
                self.btn1_layout.removeWidget(btn1)
            self.buttons_1.clear()
            for btn_mis in self.mistake_button:
                self.btnMIS_layout.removeWidget(btn_mis)
            self.mistake_button.clear()
            my_new_block = block_macker.Block_macker('')
            my_new_block.body_b = block_macker.replace_head(My_blocks,block,current_Textp.new_Textpage)
            my_new_block.title = 'milling'
            block.insert(current_Textp.new_Textpage,my_new_block)
            My_blocks.insert(current_Textp.new_Textpage,my_new_block.body_b)
            tol = customise_tool.Customise_tool(My_blocks[current_Textp.new_Textpage],\
                                                block[current_Textp.new_Textpage].title, My_tool)
            block[current_Textp.new_Textpage].tool = tol.set_tool()
            m = Rude_mistakes.Rude_mist(My_blocks[current_Textp.new_Textpage], \
                                        block[current_Textp.new_Textpage].title, block[current_Textp.new_Textpage].tool, 0)
            m.rude_mist()
            block[current_Textp.new_Textpage].mistakes = m.rude_mistakes
            block[current_Textp.new_Textpage].warning_m = m.warning_m
            block[current_Textp.new_Textpage].milling_mode = m.milling_mode
            block[current_Textp.new_Textpage].loops_names = m.loops_names
            if block[current_Textp.new_Textpage].mistakes['total'] == 0:
                main_time_count(My_blocks[current_Textp.new_Textpage], current_Textp.new_Textpage,\
                                block, m, My_tool, block[current_Textp.new_Textpage].title)
            #current_Textp.new_Textpage = 0
            #current_Textp.old_Textpage = 0
            current_Textp.switch_check = 0
            current_Textp.check_mistakesBlock = 0
            theSizeButtons = 12
            # Renum my old blocks
            My_blocks = find_mistakes.new_renum(My_blocks,block)
            for n in range(len(My_blocks)):
                self.make_new_rightside(n, 'add')
                self.button = QPushButton(str(My_blocks[n][1].rstrip('\n')))
                self.button.setMinimumHeight(35)
                self.button.setMaximumWidth(569)
                self.button.setFont(QFont('Arial', theSizeButtons))
                self.buttons_menu.append(self.button)
                if n > 0 and block[n].mistakes['total'] != 0:
                    self.button.setStyleSheet("QPushButton {color: red}")
                self.button.pressed.connect(lambda n=n: self.btn_Press(n))
                self.layout.addWidget(self.button)
            self.buttons_menu[current_Textp.new_Textpage].setStyleSheet("QPushButton { background-color: grey }")
            for j in My_blocks[current_Textp.new_Textpage]:
                self.txtEdit.append(j.rstrip('\n'))
            cursor = QTextCursor(self.txtEdit.document())
            cursor.setPosition(0)
            self.txtEdit.setTextCursor(cursor)
            otkat_text.clear()
            self.paint_all_icons()



    def otkrit_newfile(self, tool_file, otkat_text, old_title, MyOld_file, My_blocks, block):
        # I added C: wrong purposely because I want to change it later
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:')[0]
        marker = 1
        if current_Textp.switch_check == 1 and len(fname) != 0:
            resultation = QtWidgets.QMessageBox.question(self,"Открытие нового файла",
                                                         "В последнем файле есть несохраненные изменения!\nЕсли вы откроете новый файл"\
                                                         + " вы потеряете последние изменения в текущем файле.\n"\
                                                         + "Вы действительно хотите открыть " + str(fname) +" ?",
                                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                         QtWidgets.QMessageBox.No)
            if resultation == QtWidgets.QMessageBox.Yes:
                marker = 1
            else:
                marker = 0
        if len(fname) != 0 and marker == 1:
            current_Textp.name_of_mainFile = Set_customise.determinate_new_name(fname)
            current_Textp.way_of_mainFile = Set_customise.determinate_new_way(fname)
            status_stroka = 'ОТКРЫТИЕ ФАЙЛА ' + current_Textp.name_of_mainFile + '...'
            self.label_status.setText(status_stroka)
            qApp.processEvents()
            self.label_status.clear()
            del tool_file
            tool_file = create_new_tools()
            otkat_text.clear()
            old_title = ''
            MyOld_file.clear()
            for line in open(fname): MyOld_file.append(line)
            current_Textp.file_without_changing = MyOld_file.copy()
            for n in self.buttons_menu:
                self.layout.removeWidget(n)
            self.buttons_menu.clear()
            for n in self.labels_menu7:
                self.layout.removeWidget(n)
            self.labels_menu7.clear()
            self.txtEdit.clear()
            for btn3 in self.buttons_3:
                self.btn3_layout.removeWidget(btn3)
            self.buttons_3.clear()
            for btn2 in self.buttons_2:
                self.btn2_layout.removeWidget(btn2)
            self.buttons_2.clear()
            for edit in self.edits:
                self.edits_layout.removeWidget(edit)
            self.edits.clear()
            for btn1 in self.buttons_1:
                self.btn1_layout.removeWidget(btn1)
            self.buttons_1.clear()
            for btn_mis in self.mistake_button:
                self.btnMIS_layout.removeWidget(btn_mis)
            self.mistake_button.clear()
            self.setWindowTitle('DANI v.1.32   <' + str(fname) + '>')
            My_blocks.clear()
            block.clear()
            create_new_blocks(My_blocks, block, MyOld_file)
            create_new_customiseT(My_blocks, block)
            create_new_units(My_blocks, block)
            create_empty_spaces(My_blocks, block)
            current_Textp.new_Textpage = 0
            current_Textp.old_Textpage = 0
            current_Textp.switch_check = 0
            current_Textp.check_mistakesBlock = 0
            theSizeButtons = 12
            for n in range(len(My_blocks)):
                self.make_new_rightside(n, 'add')
                self.button = QPushButton(str(My_blocks[n][1].rstrip('\n')))
                self.button.setMinimumHeight(35)
                self.button.setMaximumWidth(569)
                self.button.setFont(QFont('Arial', theSizeButtons))
                self.buttons_menu.append(self.button)
                if n > 0 and block[n].mistakes['total'] != 0:
                    self.button.setStyleSheet("QPushButton {color: red}")
                self.button.pressed.connect(lambda n=n: self.btn_Press(n))
                self.layout.addWidget(self.button)
                #self.layout.addSpacing(25)
            self.first_open()
            if self.compare_original_file() != 0:
                current_Textp.switch_check = 1
                ico_sbutton = QIcon('Icons_milling/not_save.png')
                self.Save_button.setIconSize(QSize(44, 44))
                self.Save_button.setIcon(ico_sbutton)
            else:
                current_Textp.switch_check = 0
                ico_sbutton = QIcon('Icons_milling/saved.png')
                self.Save_button.setIconSize(QSize(44, 44))
                self.Save_button.setIcon(ico_sbutton)
            self.paint_all_icons()


    # CLose main window
    def closeEvent(self, e):
        if current_Textp.switch_check == 1:
            resultation = QtWidgets.QMessageBox.question(self,"Закрытие программы",
                                                         "В программе есть несохраненные изменения!\nВы действительно хотите закрыть файл без сохранения?",
                                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                         QtWidgets.QMessageBox.No)
            if resultation == QtWidgets.QMessageBox.Yes:
                e.accept()
                QtWidgets.QWidget.closeEvent(self,e)
            else:
                e.ignore()
        else:
            e.accept()



    # Create from simple block - new block with repetition and parametrs
    def create_repetition(self,My_blocks):
        if block[current_Textp.new_Textpage].title == 'milling':
            status_stroka = 'ИЗМЕНЕНИЕ БЛОКА С МЕТКОЙ GOTO...'
            self.label_status.setText(status_stroka)
            qApp.processEvents()
            self.label_status.clear()
            new_spisok = self.txtEdit.toPlainText().split('\n')
            j = 0
            while j < len(new_spisok):
                new_spisok[j] = new_spisok[j] + '\n'
                j += 1
            otkat_text.clear()
            otkat_text.extend(new_spisok)
            # Create text with iteration
            text_withLoop = Loop_creator.main_creator(new_spisok)
            # Replace my block for future
            My_blocks[current_Textp.new_Textpage].clear()
            My_blocks[current_Textp.new_Textpage] = text_withLoop
            block[current_Textp.new_Textpage].title = 'milling_GOTO'
            old_title = 'milling'
            # Create a new page with loop
            self.txtEdit.clear()
            My_blocks = find_mistakes.new_renum(My_blocks, block)
            for j in My_blocks[current_Textp.new_Textpage]:
                self.txtEdit.append(j.rstrip('\n'))
            cursor = QTextCursor(self.txtEdit.document())
            cursor.setPosition(0)
            self.txtEdit.setTextCursor(cursor)
            self.paint_all_icons()
            self.Reload_page()


    # Return our block to begin statment
    def otkat_repetit(self):
        if len(otkat_text) != 0:
            status_stroka = 'ОТКАТ ПРЕОБРАЗОВАНИЯ БЛОКА...'
            self.label_status.setText(status_stroka)
            qApp.processEvents()
            self.label_status.clear()
            self.txtEdit.clear()
            for j in otkat_text:
                self.txtEdit.append(j.rstrip('\n'))
            otkat_text.clear()
            My_blocks[current_Textp.new_Textpage].clear()
            My_blocks[current_Textp.new_Textpage] = otkat_text
            block[current_Textp.new_Textpage].title = old_title
            cursor = QTextCursor(self.txtEdit.document())
            cursor.setPosition(0)
            self.txtEdit.setTextCursor(cursor)
            self.paint_all_icons()
            self.Reload_page()



    def btn_Press(self, id_b):
        if len(My_blocks[id_b]) > 1000:
            status_stroka = 'Загрузка '+ str(len(My_blocks[id_b])) + ' строк кадра ' + My_blocks[id_b][0].rstrip('\n') + '... '
            self.label_status.setText(status_stroka)
        qApp.processEvents()
        self.label_status.clear()
        # Clear old otkat
        otkat_text.clear()
        # Save old text in old block
        new_spisok = self.txtEdit.toPlainText().split('\n')
        j = 0
        while j < len(new_spisok):
            new_spisok[j] = new_spisok[j] + '\n'
            j += 1
        My_blocks[current_Textp.old_Textpage].clear()
        My_blocks[current_Textp.old_Textpage] = new_spisok
        self.Reload_page()
        self.buttons_menu[current_Textp.old_Textpage].setStyleSheet("QPushButton { background-color: light grey }")
        if block[current_Textp.old_Textpage].mistakes['total'] != 0:
            self.buttons_menu[current_Textp.old_Textpage].setStyleSheet("QPushButton { color: red }"
                                                                         "QPushButton { background-color: light grey }")
        # Check our last page if we did change
        if current_Textp.switch_check == 1:
            self.Check_Lastpage()
        #current_Textp.switch_check = 0
        #Set text for old menu's button
        self.buttons_menu[current_Textp.old_Textpage].setText(str(My_blocks[current_Textp.old_Textpage][1].rstrip('\n')))
        current_Textp.old_Textpage = id_b
        current_Textp.new_Textpage = id_b
        self.buttons_menu[id_b].setStyleSheet("QPushButton { background-color: grey }")
        if block[id_b].mistakes['total'] != 0:
            self.buttons_menu[id_b].setStyleSheet("QPushButton { color: red }"
                                                  "QPushButton { background-color: grey }")
        #Make new page
        self.txtEdit.blockSignals(True)
        self.txtEdit.clear()
        for j in My_blocks[id_b]:
            self.txtEdit.append(j.rstrip('\n'))
        self.txtEdit.blockSignals(False)

        self.Make_field_feed(id_b)
        self.Mistakes_field_feed(id_b)
        cursor = QTextCursor(self.txtEdit.document())
        cursor.setPosition(0)
        self.txtEdit.setTextCursor(cursor)
        #print(Set_customise.Read_new_TandS(My_blocks[id_b]))
        # Change active icons:
        self.paint_all_icons()


    def first_open(self):
        if len(My_blocks) > 0:
            for j in My_blocks[0]:
                self.buttons_menu[0].setStyleSheet("QPushButton { background-color: grey }")
                self.txtEdit.append(j.rstrip('\n'))
                cursor = QTextCursor(self.txtEdit.document())
                cursor.setPosition(0)
                self.txtEdit.setTextCursor(cursor)

    def Text_changed(self):
        ico_sbutton = QIcon('Icons_milling/not_save.png')
        self.Save_button.setIconSize(QSize(44, 44))
        self.Save_button.setIcon(ico_sbutton)
        current_Textp.check_mistakesBlock = current_Textp.new_Textpage
        current_Textp.switch_check = 1

    def Text_changed2(self):
        ico_sbutton = QIcon('Icons_milling/not_save.png')
        self.Save_button.setIconSize(QSize(44, 44))
        self.Save_button.setIcon(ico_sbutton)
        current_Textp.switch_check = 1

    # Make right bottom field with FEED RATE elements
    def Make_field_feed(self,id_b):
        feed = Feed_rate.feed_r(My_blocks[id_b],block[id_b].title)
        block[id_b].feed = feed.feed_mesuare()
        for btn3 in self.buttons_3:
            self.btn3_layout.removeWidget(btn3)
        self.buttons_3.clear()
        for btn2 in self.buttons_2:
            self.btn2_layout.removeWidget(btn2)
        self.buttons_2.clear()
        for edit in self.edits:
            self.edits_layout.removeWidget(edit)
        self.edits.clear()
        for btn1 in self.buttons_1:
            self.btn1_layout.removeWidget(btn1)
        self.buttons_1.clear()
        i = 0
        while i < len (block[id_b].feed):
            feed_line = QLineEdit()
            self.edits.append(feed_line)
            self.edits_layout.addWidget(feed_line)
            btn_find = QPushButton('F' + ' = ' + str(block[id_b].feed[i]))
            btn_find.pressed.connect(lambda numb=id_b, i=i: self.searsh_feed(numb, i))
            self.buttons_1.append(btn_find)
            self.btn1_layout.addWidget(btn_find)
            btn_replace = QPushButton('Заменить')
            text_tip = 'УСТАНОВИТЬ ЗАДАННУЮ ПОДАЧУ ТОЛЬКО В ТЕКУЩЕМ БЛОКЕ'
            btn_replace.setToolTip(text_tip)
            btn_replace.pressed.connect(lambda numb=id_b, i=i: self.btn_Freplace(numb, i))
            self.buttons_2.append(btn_replace)
            self.btn2_layout.addWidget(btn_replace)
            name_tool = 'Все T' + block[id_b].tool
            btn_Allreplace = QPushButton(name_tool)
            btn_Allreplace.pressed.connect(lambda numb=id_b, i=i: self.All_feedReplace(numb, i))
            text_tip = 'УСТАНОВИТЬ ЗАДАННУЮ ПОДАЧУ ДЛЯ ВСЕХ ИНСТРУМЕНТОВ T' + block[id_b].tool + ' ВО ВСЕХ БЛОКАХ'
            btn_Allreplace.setToolTip(text_tip)
            self.buttons_3.append(btn_Allreplace)
            self.btn3_layout.addWidget(btn_Allreplace)
            i += 1


    def searsh_feed(self,numb,n):
        text = 'F' + str(block[numb].feed[n])
        a = self.txtEdit.find(text)
        self.txtEdit.setFocus()
        if a == False:
            cursor = QTextCursor(self.txtEdit.document())
            cursor.setPosition(0)
            self.txtEdit.setTextCursor(cursor)

    # Make left field with mistakes on the bottom
    def Mistakes_field_feed(self,id_b):
        for btn_mis in self.mistake_button:
            self.btnMIS_layout.removeWidget(btn_mis)
        self.mistake_button.clear()
        i = 0
        while i < block[id_b].mistakes['total']:
            real_number = i + 1
            text_button = str(block[id_b].mistakes[real_number])
            if text_button.count('*') == 1:
                text_button = text_button.partition('*')[0]
            btn_mis = QPushButton(text_button)
            btn_mis.pressed.connect(lambda numb=id_b, num_mis=real_number: self.Find_fragment_mistake(numb, num_mis))
            self.mistake_button.append(btn_mis)
            self.btnMIS_layout.addWidget(btn_mis)
            i += 1


    def Find_fragment_mistake(self,numb,num_mis):
        n = 0
        if block[numb].mistakes[num_mis].count('*') == 1:
            n = int(block[numb].mistakes[num_mis].partition('*')[2])
            cursor = QTextCursor(self.txtEdit.document())
            cursor.setPosition(0)
            while n > 0:
                cursor.movePosition(QTextCursor.Down)
                n -= 1
            cursor.select(QTextCursor.LineUnderCursor)
            self.txtEdit.setTextCursor(cursor)
            self.txtEdit.setFocus()



    # Set new feed from button ZAM to Edit text page
    def btn_Freplace(self,numb, n):
        if len(My_blocks[numb]) > 1000:
            status_stroka = 'Установка подачи '+ self.edits[n].text() + ' в кадре ' + My_blocks[numb][0].rstrip('\n') + '... '
            self.label_status.setText(status_stroka)
        qApp.processEvents()
        self.label_status.clear()
        # Save old text in old block
        if current_Textp.switch_check == 1:
            new_spisok = self.txtEdit.toPlainText().split('\n')
            j = 0
            while j < len(new_spisok):
                new_spisok[j] = new_spisok[j] + '\n'
                j += 1
            My_blocks[numb].clear()
            My_blocks[numb] = new_spisok
        self.txtEdit.clear()
        feed = Feed_rate.feed_r(My_blocks[numb],block[numb].title)
        feed.feed_mesuare()
        My_blocks[numb] = feed.feed_rep(block[numb].title, block[numb].feed[n], self.edits[n].text())
        for j in My_blocks[numb]:
            self.txtEdit.append(j.rstrip('\n'))
        cursor = QTextCursor(self.txtEdit.document())
        cursor.setPosition(0)
        if self.edits[n].text() in block[numb].feed:
            self.Make_field_feed(numb)
            self.txtEdit.setTextCursor(cursor)
        else:
            self.txtEdit.setTextCursor(cursor)
            new_text_button = 'F = ' + self.edits[n].text()
            block[numb].feed[n] = self.edits[n].text()
            self.buttons_1[n].setText(new_text_button)
            self.edits[n].clear()


    # Function replaces all blocks with choosed S
    def All_SReplace(self):
        if current_Textp.switch_check == 1:
            new_spisok = self.txtEdit.toPlainText().split('\n')
            j = 0
            while j < len(new_spisok):
                new_spisok[j] = new_spisok[j] + '\n'
                j += 1
            My_blocks[current_Textp.new_Textpage].clear()
            My_blocks[current_Textp.new_Textpage] = new_spisok
        # Feed and Turn (F and S)
        if (current_Textp.new_Textpage != 0 and block[current_Textp.new_Textpage].title != 'Ren_150'
            and block[current_Textp.new_Textpage].title != 'Ren_200'):
            FS = Set_customise.Read_new_TandS(My_blocks[current_Textp.new_Textpage])
            # Set new S for all tools with numbers T
            st = Set_customise.Set_new_TandS(My_blocks,block,FS)
            self.show_modal_window_FS(FS,st)
        self.Text_changed2()



    # Open new window where you can replace all T numbers
    def All_TReplaceMENU(self):
        global modalWindow
        size_text = 14
        modalWindow = QWidget(win, Qt.Window)
        modalWindow.resize(400,100)
        name_window = 'Замена номера инструмента T'
        modalWindow.setWindowTitle(name_window)
        modalWindow.setWindowModality(Qt.ApplicationModal)
        modalWindow.setAttribute(Qt.WA_DeleteOnClose,True)
        if current_Textp.switch_check == 1:
            self.Reload_page()
        # Try to set start text
        text_line1 = ''
        if (current_Textp.new_Textpage != 0 and block[current_Textp.new_Textpage].title != 'Ren_150'
            and block[current_Textp.new_Textpage].title != 'Ren_200'):
            text_line1 = 'T' + block[current_Textp.new_Textpage].tool
        stroka = Set_customise.helper_field_T(block, My_blocks)
        layout_modal = QVBoxLayout()
        layout_grid = QGridLayout()
        field_1 = QLabel('Исходный:')
        field_1.setFont(QFont('Arial',size_text))
        field_2 = QLabel('Заменить на:')
        field_2.setFont(QFont('Arial',size_text))
        status_l = QLabel()
        status_l.setFont(QFont('Arial', size_text))
        instrument_l = QLabel(stroka)
        instrument_l.setFont(QFont('Arial', size_text-2))
        line_1 = QLineEdit(text_line1)
        line_1.setFont(QFont('Arial',size_text))
        line_2 = QLineEdit()
        line_2.setFont(QFont('Arial',size_text))
        replace_button = QPushButton('Заменить')
        replace_button.setFont(QFont('Arial',size_text))
        replace_button.pressed.connect(lambda status_l = status_l, line_1 = line_1, line_2 = line_2: self.All_T_Replace(status_l, line_1, line_2))
        replace_button.pressed.connect(modalWindow.close)
        replace_button.pressed.connect(self.Text_changed2)
        layout_grid.addWidget(field_1, 0, 0)
        layout_grid.addWidget(field_2, 0, 1)
        layout_grid.addWidget(line_1, 1, 0)
        layout_grid.addWidget(line_2, 1, 1)
        layout_modal.addLayout(layout_grid)
        layout_modal.addWidget(replace_button)
        layout_modal.addWidget(instrument_l)
        layout_modal.addWidget(status_l)
        modalWindow.setLayout(layout_modal)
        modalWindow.show()


    def All_T_Replace(self, status_l, line_1, line_2):
        number_T1 = line_1.text()
        number_T2 = line_2.text()
        numbers = '0123456789'
        marker = 0
        replaced_blocks = []
        if len(number_T1) >= 2 and number_T1[0] == 'T':
            tool_n1 = number_T1.partition('T')[2]
            for i in tool_n1:
                if i not in numbers:
                    marker = 1
            if len(number_T2) >= 2 and number_T2[0] == 'T' and marker == 0:
                tool_n2 = number_T2.partition('T')[2]
                for i in tool_n2:
                    if i not in numbers:
                        marker = 1
                if marker == 0:
                    replaced_blocks = Set_customise.Set_new_allT(tool_n1, tool_n2, My_blocks, block)
                    #Make new page
                    if len(My_blocks[current_Textp.new_Textpage]) > 1000:
                        status_stroka = 'Смена номера инструмента ' + number_T1 + ' на ' + number_T2 + '...'
                        status_l.setText(status_stroka)
                    qApp.processEvents()
                    status_l.clear()
                    self.txtEdit.blockSignals(True)
                    self.txtEdit.clear()
                    for j in My_blocks[current_Textp.new_Textpage]:
                        self.txtEdit.append(j.rstrip('\n'))
                    self.txtEdit.blockSignals(False)
                    #block[current_Textp.new_Textpage].tool = line_2
                    self.Mistakes_field_feed(current_Textp.new_Textpage)
                    cursor = QTextCursor(self.txtEdit.document())
                    cursor.setPosition(0)
                    self.txtEdit.setTextCursor(cursor)
                    for j in replaced_blocks:
                        current_Textp.check_mistakesBlock = j
                        self.Check_Lastpage()
                    j = 1
                    while j < len(My_blocks):
                        # Replaxe all instrument on the right side
                        self.make_new_rightside(j, 'replace')
                        j += 1
                    self.Make_field_feed(current_Textp.new_Textpage)
                    self.Reload_page()



    # Replace feed and Spindel speed for all blocks with current number T
    def All_feedReplace(self,numb, n):
        if len(My_blocks[numb]) > 1000:
            status_stroka = 'Установка подачи '+ self.edits[n].text() + ' для всех кадров с инструментом T' + block[numb].tool + '...'
            self.label_status.setText(status_stroka)
        qApp.processEvents()
        self.label_status.clear()
        # Save old text in old block
        if current_Textp.switch_check == 1:
            new_spisok = self.txtEdit.toPlainText().split('\n')
            j = 0
            while j < len(new_spisok):
                new_spisok[j] = new_spisok[j] + '\n'
                j += 1
            My_blocks[numb].clear()
            My_blocks[numb] = new_spisok
        self.txtEdit.clear()
        k = 1
        numbers_replaces = []
        not_replaced = []
        mis_replaced = []
        while k < len(My_blocks):
            if block[k].mistakes['total'] == 0 and block[k].tool == block[numb].tool:
                feed = Feed_rate.feed_r(My_blocks[k],block[k].title)
                block[k].feed = feed.feed_mesuare()
                p = 0
                old_feed = self.buttons_1[n].text().partition('=')[2].lstrip(' ')
                marker = 0
                while p < len(block[k].feed):
                    if block[k].feed[p] == old_feed:
                        marker = 1
                        numbers_replaces.append(My_blocks[k][0])
                        My_blocks[k] = feed.feed_rep(block[k].title, block[k].feed[p], self.edits[n].text())
                    p += 1
                if marker == 0:
                    not_replaced.append(My_blocks[k][0])
                feed = Feed_rate.feed_r(My_blocks[k],block[k].title)
                block[k].feed = feed.feed_mesuare()
            elif block[k].mistakes['total'] != 0 and block[k].tool == block[numb].tool:
                mis_replaced.append(My_blocks[k][0])
            k += 1
        for j in My_blocks[numb]:
            self.txtEdit.append(j.rstrip('\n'))
        cursor = QTextCursor(self.txtEdit.document())
        cursor.setPosition(0)
        self.show_modal_window(numbers_replaces,not_replaced,mis_replaced,block[numb].tool, self.edits[n].text())
        if self.edits[n].text() in block[numb].feed:
            self.Make_field_feed(numb)
            self.txtEdit.setTextCursor(cursor)
        else:
            self.txtEdit.setTextCursor(cursor)
            new_text_button = 'F = ' + self.edits[n].text()
            block[numb].feed[n] = self.edits[n].text()
            self.buttons_1[n].setText(new_text_button)
            self.edits[n].clear()



    #If i CLICKED the BUTTON check page
    def Reload_page(self):
        new_spisok = self.txtEdit.toPlainText().split('\n')
        j = 0
        while j < len(new_spisok):
            new_spisok[j] = new_spisok[j] + '\n'
            j += 1
        My_blocks[current_Textp.new_Textpage].clear()
        My_blocks[current_Textp.new_Textpage] = new_spisok
        # Defining a new title
        block[current_Textp.new_Textpage].title = block_macker.initialization_block(My_blocks[current_Textp.new_Textpage])
        if block[current_Textp.new_Textpage].title == 'Ren_200' or block[current_Textp.new_Textpage].title == 'Ren_150':
            block[current_Textp.new_Textpage].tool = '60'
        diametr_f = 0
        if (int(block[current_Textp.new_Textpage].tool)-1)>=0 and (int(block[current_Textp.new_Textpage].tool)-1)<=current_Textp.tool_amount:
            diametr_f = My_tool[int(block[current_Textp.new_Textpage].tool)-1].DValue
        m = Rude_mistakes.Rude_mist(My_blocks[current_Textp.new_Textpage],block[current_Textp.new_Textpage].title,
                                    block[current_Textp.new_Textpage].tool, diametr_f)
        m.rude_mist()
        block[current_Textp.new_Textpage].mistakes = m.rude_mistakes
        block[current_Textp.new_Textpage].warning_m = m.warning_m
        block[current_Textp.new_Textpage].milling_mode = m.milling_mode
        block[current_Textp.new_Textpage].loops_names = m.loops_names
        # Replace number of tools and mistakes if we changed T
        if block[current_Textp.new_Textpage].tool != m.correctT:
            block[current_Textp.new_Textpage].tool = m.correctT
            # Replaxe lables with new instrument
            self.make_new_rightside(current_Textp.new_Textpage, 'replace')
            if (int(block[current_Textp.new_Textpage].tool)-1)>=0 and (int(block[current_Textp.new_Textpage].tool)-1)<=current_Textp.tool_amount:
                diametr_f = My_tool[int(block[current_Textp.new_Textpage].tool)-1].DValue
            m2 = Rude_mistakes.Rude_mist(My_blocks[current_Textp.new_Textpage],
                                         block[current_Textp.new_Textpage].title,
                                         block[current_Textp.new_Textpage].tool, diametr_f)
            m2.rude_mist()
            block[current_Textp.new_Textpage].mistakes = m2.rude_mistakes
            block[current_Textp.new_Textpage].warning_m = m2.warning_m
            block[current_Textp.new_Textpage].milling_mode = m2.milling_mode
            block[current_Textp.new_Textpage].loops_names = m.loops_names
            # Count and replace time
            if block[current_Textp.new_Textpage].mistakes['total'] == 0:
                main_time_count(My_blocks[current_Textp.new_Textpage], current_Textp.new_Textpage, block, m,
                                My_tool, block[current_Textp.new_Textpage].title)
            self.Make_field_feed(current_Textp.new_Textpage)
        # Count and replace time
        if block[current_Textp.new_Textpage].mistakes['total'] == 0:
            #print(Set_customise.Read_new_TandS(My_blocks[current_Textp.new_Textpage]).get('T'))
            #block[current_Textp.new_Textpage].tool = str(Set_customise.Read_new_TandS(My_blocks[current_Textp.new_Textpage]).get('T'))
            main_time_count(My_blocks[current_Textp.new_Textpage], current_Textp.new_Textpage, block, m,
                            My_tool, block[current_Textp.new_Textpage].title)

        #Make a new field with feed
        self.Mistakes_field_feed(current_Textp.new_Textpage)
        self.buttons_menu[current_Textp.old_Textpage].setStyleSheet("QPushButton { background-color: grey }")
        if block[current_Textp.old_Textpage].mistakes['total'] != 0:
            self.buttons_menu[current_Textp.old_Textpage].setStyleSheet("QPushButton { color: red }"
                                                                         "QPushButton { background-color: grey }")
        j = 1
        while j < len(My_blocks):
            # Replaxe all instrument on the right side
            self.make_new_rightside(j, 'replace')
            j += 1
        # Change all icons
        self.paint_all_icons()


    # check page after click on new pag (only if we had chenged text)
    def Check_Lastpage(self):
        diametr_f = 0
        if (int(block[current_Textp.check_mistakesBlock].tool)-1)>=0 and (int(block[current_Textp.check_mistakesBlock].tool)-1)<=current_Textp.tool_amount:
            diametr_f = My_tool[int(block[current_Textp.check_mistakesBlock].tool)-1].DValue
        m = Rude_mistakes.Rude_mist(My_blocks[current_Textp.check_mistakesBlock],block[current_Textp.check_mistakesBlock].title, block[current_Textp.check_mistakesBlock].tool, diametr_f)
        m.rude_mist()
        theSizeButtons = 12
        if block[current_Textp.check_mistakesBlock].tool != m.correctT:
            block[current_Textp.check_mistakesBlock].tool = m.correctT
            self.make_new_rightside(current_Textp.check_mistakesBlock, 'replace')
            if (int(block[current_Textp.check_mistakesBlock].tool)-1)>=0 and (int(block[current_Textp.check_mistakesBlock].tool)-1)<=current_Textp.tool_amount:
                diametr_f = My_tool[int(block[current_Textp.check_mistakesBlock].tool)-1].DValue
            m2 = Rude_mistakes.Rude_mist(My_blocks[current_Textp.check_mistakesBlock],block[current_Textp.check_mistakesBlock].title, block[current_Textp.check_mistakesBlock].tool, diametr_f)
            m2.rude_mist()
            block[current_Textp.check_mistakesBlock].mistakes = m2.rude_mistakes
            block[current_Textp.check_mistakesBlock].warning_m = m2.warning_m
        else:
            block[current_Textp.check_mistakesBlock].mistakes = m.rude_mistakes
            block[current_Textp.check_mistakesBlock].warning_m = m.warning_m
        if block[current_Textp.check_mistakesBlock].mistakes['total'] != 0:
            self.buttons_menu[current_Textp.check_mistakesBlock].setStyleSheet("QPushButton { color: red }"
                                                                         "QPushButton { background-color: light grey }")
        else:
            self.buttons_menu[current_Textp.check_mistakesBlock].setStyleSheet("QPushButton { background-color: light grey }")



    # Make new field on right side
    def make_new_rightside(self,n, action_n):
        theSizeButtons = 12
        # Replaxe lables with new instrument
        G_layout = QHBoxLayout()
        G_widget = QWidget()
        G_widget.resize(569, 64)
        label_number = QLabel(My_blocks[n][0])
        label_number.setStyleSheet("QLabel { background-color: white }")
        label_number.setAlignment(Qt.AlignBaseline | Qt.AlignCenter)
        label_number.setFont(QFont('Arial', theSizeButtons + 4))
        label_operation = QLabel()
        Set_customise.type_operation(label_operation, block, n)
        label_g40 = QLabel()
        if block[n].title == 'milling' or block[n].title == 'milling_GOTO':
            Set_customise.type_g40(label_g40, block, n)
        label_instrument = QLabel()
        Set_customise.type_instrument(label_instrument, block, n, My_tool,current_Textp.tool_amount)
        label_Tnum = QLabel()
        Set_customise.number_Tins(label_Tnum, block, n, My_tool, My_blocks,current_Textp.tool_amount)
        label_Tnum.setStyleSheet("QLabel { background-color: white }")
        label_Tnum.setAlignment(Qt.AlignBaseline | Qt.AlignCenter)
        label_Tnum.setFont(QFont('Arial', theSizeButtons + 2))
        label_timer = QLabel()
        Set_customise.time_cut(label_timer, block, n)
        G_layout.addWidget(label_number)
        G_layout.addWidget(label_operation)
        if block[n].title == 'milling' or block[n].title == 'milling_GOTO':
            G_layout.addWidget(label_g40)
        G_layout.addWidget(label_instrument)
        G_layout.addWidget(label_Tnum)
        G_layout.addWidget(label_timer)
        if block[n].title == 'milling' or block[
            n].title == 'milling_GOTO':
            G_layout.addSpacing(30)
        else:
            G_layout.addSpacing(90)
        G_widget.setLayout(G_layout)
        if action_n == 'replace':
            # Replace my instrument
            self.layout.replaceWidget(self.labels_menu7[n], G_widget)
            self.labels_menu7[n].setParent(None)
            self.labels_menu7[n] = G_widget
        elif action_n == 'add':
            if n == 0 :
                empty_wdg = QWidget()
                self.labels_menu7.append(empty_wdg)
            else:
                self.labels_menu7.append(G_widget)
                self.layout.addWidget(G_widget)
        return None

    # Make modal window with additional information about feed replacing
    def show_modal_window(self, numbers_replaces, not_replaced, mis_replaced, num_t, feed):
        global modalWindow
        modalWindow = QWidget(win, Qt.Window)
        modalWindow.resize(400,200)
        name_window = 'Установка подачи F' + feed + ' для инструмента T' + num_t
        modalWindow.setWindowTitle(name_window)
        modalWindow.setWindowModality(Qt.ApplicationModal)
        modalWindow.setAttribute(Qt.WA_DeleteOnClose,True)
        # Make label with text
        stroka = 'Замена произведена в кадрах:\n'
        for j in numbers_replaces:
            stroka = stroka + j.rstrip('\n') + ', '
        stroka = stroka.rstrip(', ')
        if len(not_replaced) > 0:
            stroka = stroka + '\n Подача не встречается в кадрах: \n'
            for j in not_replaced:
                stroka = stroka + j.rstrip('\n') + ', '
        stroka = stroka.rstrip(', ')
        if len(mis_replaced) > 0:
            stroka = stroka + '\n Без изменений, из-за неисправленных ошибок:\n'
            for j in mis_replaced:
                stroka = stroka + j.rstrip('\n') + ', '
        stroka = stroka.rstrip(', ')
        stroka = stroka.rstrip('\n')
        label_replaces = QLabel(stroka)
        label_replaces.setFont(QFont('Arial',12))
        # Make close-button
        close_button = QPushButton('ОК')
        close_button.setFont(QFont('Arial',12))
        close_button.pressed.connect(modalWindow.close)
        layout_modal = QVBoxLayout()
        layout_modal.addWidget(label_replaces)
        layout_modal.addWidget(close_button)
        modalWindow.setLayout(layout_modal)
        modalWindow.show()


    # Make modal window with additional information about feed replacing
    def show_modal_window_FS(self, FS, stroka):
        global modalWindow2
        modalWindow2 = QWidget(win, Qt.Window)
        modalWindow2.resize(400,200)
        name_window = 'Замена S' + str(FS['S']) + ' для инструмента T' + str(FS['T'])
        modalWindow2.setWindowTitle(name_window)
        modalWindow2.setWindowModality(Qt.ApplicationModal)
        modalWindow2.setAttribute(Qt.WA_DeleteOnClose,True)
        # Make label with text
        stroka2 = 'Для T' + str(FS['T']) + ' зёамена произведена в кадрах:\n' + stroka
        label_replaces = QLabel(stroka2)
        label_replaces.setFont(QFont('Arial',12))
        # Make close-button
        close_button = QPushButton('ОК')
        close_button.setFont(QFont('Arial',12))
        close_button.pressed.connect(modalWindow2.close)
        layout_modal = QVBoxLayout()
        layout_modal.addWidget(label_replaces)
        layout_modal.addWidget(close_button)
        modalWindow2.setLayout(layout_modal)
        modalWindow2.show()


    # Create modal window with settings of ways
    def show_modal_papka(self):
        global modalWindow3
        modalWindow3 = QWidget(win, Qt.Window)
        modalWindow3.resize(800,200)
        name_window = 'Меню путей к рабочим папкам:'
        modalWindow3.setWindowTitle(name_window)
        modalWindow3.setWindowModality(Qt.ApplicationModal)
        modalWindow3.setAttribute(Qt.WA_DeleteOnClose,True)
        # Make label with text
        text_line1 = Set_customise.Customise_ToolWay()
        text_line2 = Set_customise.Directory_files()
        layout_modal = QVBoxLayout()
        field_1 = QLabel('Путь для файла data/*.json программы CATALOG:')
        field_1.setFont(QFont('MS Shell Dlg 2',12))
        field_2 = QLabel('Стартовая папка в которой DANI открывает файл после запуска: ')
        field_2.setFont(QFont('MS Shell Dlg 2',12))
        line_1 = QLineEdit(text_line1)
        line_1.setFont(QFont('MS Shell Dlg 2',12))
        line_2 = QLineEdit(text_line2)
        line_2.setFont(QFont('MS Shell Dlg 2',12))
        # Make close-button
        OK_button = QPushButton('Сохранить')
        OK_button.setFont(QFont('MS Shell Dlg 2',10))
        otm_button = QPushButton('Отмена')
        otm_button.setFont(QFont('MS Shell Dlg 2', 10))
        otm_button.pressed.connect(modalWindow3.close)
        text1 = line_1.text()
        text2 = line_2.text()
        OK_button.pressed.connect(lambda t1=line_1, t2=line_2: self.save_new_way_papka(t1, t2))
        OK_button.pressed.connect(modalWindow3.close)
        layout_H = QHBoxLayout()
        layout_H.addWidget(OK_button)
        layout_H.addWidget(otm_button)
        layout_modal.addWidget(field_1)
        layout_modal.addWidget(line_1)
        layout_modal.addWidget(field_2)
        layout_modal.addWidget(line_2)
        layout_modal.addLayout(layout_H)
        modalWindow3.setLayout(layout_modal)
        modalWindow3.show()

    def save_new_way_papka(self, line_1, line_2):
        My_new_config = []
        text1 = line_1.text() + '\n'
        text2 = line_2.text() + '\n'
        newfile = open('Config_d.txt', 'w')
        My_new_config.append('Way for tools\n')
        My_new_config.append(text1)
        My_new_config.append('Way for files\n')
        My_new_config.append(text2)
        for i in My_new_config:
            newfile.write(i)
        newfile.close()


    # Paint all icons in out Tool bar
    def paint_all_icons(self):
        if len(block) > 0 and block[current_Textp.new_Textpage].title == 'milling':
            Loop_icon = QIcon('Icons_milling/Loop_conversionA.png')
            self.Make_loop.setIconSize(QSize(50, 50))
            self.Make_loop.setIcon(Loop_icon)
        else:
            Loop_icon = QIcon('Icons_milling/Loop_conversionD.png')
            self.Make_loop.setIconSize(QSize(50, 50))
            self.Make_loop.setIcon(Loop_icon)
        if (len(block) > 0 and block[current_Textp.new_Textpage].title == 'Drill'\
                and block[current_Textp.new_Textpage].mistakes['total'] == 0):
            ico_hole_mill = QIcon('Icons_milling/color_rast.png')
            self.holemil_button.setIconSize(QSize(50, 50))
            self.holemil_button.setIcon(ico_hole_mill)
        else:
            ico_hole_mill = QIcon('Icons_milling/black_rast.png')
            self.holemil_button.setIconSize(QSize(50, 50))
            self.holemil_button.setIcon(ico_hole_mill)
        if (len(block) > 0 and block[current_Textp.new_Textpage].title == 'Loop' \
                and block[current_Textp.new_Textpage].mistakes['total'] == 0):
            ico_fullL = QIcon('Icons_milling/maximaze_A.png')
            self.fullL_button.setIconSize(QSize(50, 50))
            self.fullL_button.setIcon(ico_fullL)
            ico_shrinkL = QIcon('Icons_milling/shrink_loop.png')
            self.shrinkL_button.setIconSize(QSize(50, 50))
            self.shrinkL_button.setIcon(ico_shrinkL)
        else:
            ico_fullL = QIcon('Icons_milling/maximaze_B.png')
            self.fullL_button.setIconSize(QSize(50, 50))
            self.fullL_button.setIcon(ico_fullL)
            ico_shrinkL = QIcon('Icons_milling/shrink_loopB.png')
            self.shrinkL_button.setIconSize(QSize(50, 50))
            self.shrinkL_button.setIcon(ico_shrinkL)
        if len(otkat_text) != 0:
            otkat_icon = QIcon('Icons_milling/Green_return.png')
            self.otkat_all.setIconSize(QSize(50, 50))
            self.otkat_all.setIcon(otkat_icon)
        else:
            otkat_icon = QIcon('Icons_milling/notactive_return.png')
            self.otkat_all.setIconSize(QSize(50, 50))
            self.otkat_all.setIcon(otkat_icon)
        if current_Textp.new_Textpage == 0:
            ico_add_before = QIcon('Icons_milling/add_beforeB.png')
            self.add_before_button.setIconSize(QSize(50, 50))
            self.add_before_button.setIcon(ico_add_before)
            ico_add_after = QIcon('Icons_milling/delete_black.png')
            self.delblock_button.setIconSize(QSize(50, 50))
            self.delblock_button.setIcon(ico_add_after)
        else:
            ico_add_before = QIcon('Icons_milling/add_beforeA.png')
            self.add_before_button.setIconSize(QSize(50, 50))
            self.add_before_button.setIcon(ico_add_before)
            ico_add_after = QIcon('Icons_milling/delete_colour.png')
            self.delblock_button.setIconSize(QSize(50, 50))
            self.delblock_button.setIcon(ico_add_after)


    def save_newFile(self):
        if current_Textp.switch_check == 1:
            new_spisok = self.txtEdit.toPlainText().split('\n')
            j = 0
            while j < len(new_spisok):
                new_spisok[j] = new_spisok[j] + '\n'
                j += 1
            My_blocks[current_Textp.new_Textpage].clear()
            My_blocks[current_Textp.new_Textpage] = new_spisok
            #way = Set_customise.Directory_files()
            os.rename(current_Textp.way_of_mainFile+'\\'+current_Textp.name_of_mainFile, current_Textp.way_of_mainFile+'\\'+current_Textp.name_of_mainFile+'_OLD')
            nefile = open(current_Textp.way_of_mainFile + '\\'+current_Textp.name_of_mainFile,'w')
            # Kill empty spaces at the end of block (we need only two spaces)
            i = 0
            while i < len(My_blocks):
                j = len(My_blocks[i])-1
                while j > 0:
                    if My_blocks[i][j] == '\n':
                        del My_blocks[i][j]
                    elif My_blocks[i][j] == ' \n':
                        del My_blocks[i][j]
                    else:
                        break
                    j -= 1
                i += 1
            # Add double space for the first Block
            if (My_blocks[0][len(My_blocks[0])-1]) != '\n':
                My_blocks[0].append('\n')
                My_blocks[0].append('\n')
            elif (My_blocks[0][len(My_blocks[0])-2]) != '\n':
                My_blocks[0].append('\n')
            # Add empty spaces at the end of blocks
            k = 1
            while k < len(My_blocks):
                if My_blocks[k][len(My_blocks[k])-1] != '\n':
                    My_blocks[k].append('\n')
                    My_blocks[k].append('\n')
                elif My_blocks[k][len(My_blocks[k]) - 2] != '\n':
                    My_blocks[k].append('\n')
                k += 1
            # Save my blocks in file
            i = 0
            while i < len(My_blocks):
                j = 0
                while j < len(My_blocks[i]):
                    nefile.write(My_blocks[i][j])
                    j += 1
                i += 1
            nefile.close()
            os.remove(current_Textp.way_of_mainFile+'\\'+current_Textp.name_of_mainFile+'_OLD')
            ico_sbutton = QIcon('Icons_milling/saved.png')
            self.Save_button.setIconSize(QSize(44, 44))
            self.Save_button.setIcon(ico_sbutton)
            current_Textp.switch_check = 0


    # Function check first open file, and compare, if we changed it
    def compare_original_file(self):
        i = 0
        wait_file = []
        izm = 0
        while i < len(My_blocks):
            j = 0
            while j < len(My_blocks[i]):
                wait_file.append(My_blocks[i][j])
                j += 1
            j = len(wait_file) - 1
            while j > 0:
                if wait_file[j] == '\n' or wait_file[j] == ' \n' or wait_file[j] == '':
                    wait_file.pop()
                else:
                    break
                j -= 1
            i += 1
            wait_file.append('\n')
            wait_file.append('\n')
        if current_Textp.file_without_changing != wait_file:
            izm = 1
        return izm

    # Attention message if we didn't have normal setting
    def attention_message(self):
        self.txtEdit.append('Не найден файл *.json по заданному пути.')
        self.txtEdit.append('Необходимо произвести настройку файла Config_d.txt!\n')
        self.txtEdit.append('Сделайте следующее:\n')
        self.txtEdit.append('1) Откройте меню Настройки/Рабочая папка...')
        self.txtEdit.append('2) В строке "Путь для файла data/*.json программы CATALOG:" укажите правильный путь где\
         расположен файл *.json из вашей программы CATALOG на компьютере.')
        self.txtEdit.append('3) Нажмите кнопку "Сохранить".')
        self.txtEdit.append('Теперь перезапустите программу:')
        self.txtEdit.append('4) Нажмите крестик в правом верхнем углу для закрытия программы.')
        self.txtEdit.append('5) Нажмите "Yes" на вопрос о несохраненных изменениях.')
        return None

win = UI()
win.show()
splash.finish(win)
sys.exit(app.exec_())






