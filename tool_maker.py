"""This modul make tool data table for application from our base
"""

import os

class Tool_maker:
    def __init__(self,CellNumber):
        self.CellNumber = CellNumber
        self.ConeId = ''
        self.ToolId = ''
        self.DValue = ''
        self.LValue = ''
        self.BValue = ''
        self.RValue = ''
        self.ToolNameType =''
        self.way_tools = ''

    @staticmethod
    def read_toolTable(way_tools):
        #Make data tools
        My_tools_file = []
        for line in open(way_tools,encoding="utf-8"):My_tools_file.append(line)
        return My_tools_file


    @staticmethod
    def count_tool(My_tools_file):
        #Make data tools
        k = 0
        i = 0
        My_tool = []
        while i < len(My_tools_file):
            if 'CellNumber' in My_tools_file[i]:
                k += 1
            i += 1
        return k 
    

    #I make a new tool
    def Make_new_tool(self, k, My_tools_file):
        i = 0
        our_pos = -1
        while i < len(My_tools_file):
            while our_pos < k:
                if 'CellNumber' in My_tools_file[i]:
                    our_pos += 1
                i += 1
            self.BValue = My_tools_file[i-2].partition('": ')[2].rstrip('\n').rstrip(',')
            while '}' not in My_tools_file[i]:
                if 'ConeId' in My_tools_file[i]:
                    self.ConeId = My_tools_file[i].partition('": "')[2].rstrip('\n').rstrip(',').rstrip('"')
                    if self.ConeId == '':
                        self.ConeId = 'None_Con'
                if 'DValue' in My_tools_file[i]:
                    self.DValue = My_tools_file[i].partition('": "')[2].rstrip('\n').rstrip(',').rstrip('"')
                    if self.DValue != '':
                        self.DValue = float(self.DValue)
                    else:
                        self.DValue = 0
                if 'LValue' in My_tools_file[i]:
                    self.LValue = My_tools_file[i].partition('": ')[2].rstrip('\n').rstrip(',')
                if 'RValue' in My_tools_file[i]:
                    self.RValue = My_tools_file[i].partition('": ')[2].rstrip('\n').rstrip(',')            
                if 'ToolId' in My_tools_file[i]:
                    self.ToolId = My_tools_file[i].partition('": "')[2].rstrip('\n').rstrip(',').rstrip('"')
                    if self.ToolId == '':
                        self.ToolId = 'None_Tool_Id'
                if 'ToolNameType' in My_tools_file[i]:
                    self.ToolNameType = My_tools_file[i].partition('": "')[2].rstrip('\n').rstrip('"')
                i += 1
            i = len(My_tools_file)
        
