#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from os.path import join, dirname, abspath
import xlrd
import os
        
def difference(a,b):
        if (a == b):
            return 0
        return 1

def edit_distance(i, j, str1, str2, arr):
        if i == 0:
                return j
        if j == 0:
                return i
        if arr[i-1-1][j-1] == -1:
                arr[i-1-1][j-1] = edit_distance(i-1, j, str1, str2, arr)
        distance1 = arr[i-1-1][j-1] + 1
        if arr[i-1][j-1-1] == -1:
                arr[i-1][j-1-1] = edit_distance(i, j-1, str1, str2, arr)
        distance2 = arr[i-1][j-1-1] + 1
        if arr[i-1-1][j-1-1] == -1:
                arr[i-1-1][j-1-1] = edit_distance(i-1, j-1, str1, str2, arr)
        distance3 = arr[i-1-1][j-1-1] +  difference(str1[i-1], str2[j-1])
        if distance1 <= distance2 and distance1 <= distance3:
                return distance1
        if distance2 <= distance3:
                return distance2
        return distance3

fname = join(dirname(dirname(abspath(__file__))), 'BantuData', 'database.xlsx')
workbook = xlrd.open_workbook(fname)
words = workbook.sheet_by_index(1);
sorting = workbook.sheet_by_index(2);
#rows, start at 3
#columns, start at 1

# ə and ̀ are not being combined, they are treated as different letters
#   possibly re-include:
#       import unicodedata
#       unicodedata.normalize('NFC', ...)

#initialize groupings
for column in range (1, sorting.ncols):
        groupings = []
        data = []
        for i in range(3, sorting.nrows):
                group = sorting.cell(i,column).value
                language = words.cell(i, 0).value
                word = words.cell(i, column).value
                if group not in groupings:
                        groupings.append(group)
                        data.append([])
                index = groupings.index(group)
                data[index].append([language, word])
        
        for i in data:
                # i of form [ [language, word], [language, word], ...]
                averages = []
                num = len(i) # number of languages in this group
                for init in range(0, num):
                        averages.append(0)
                for j in range(0, num):
                        # j of form [language, word]
                        if not isinstance(i[j][1], basestring):
                                num = num - 1
                        else:
                                for k in range(j+1, num):
                                        # k of form [language, word]
                                        if isinstance(i[k][1], basestring):
                                                arr = [[-1] * len(i[k][1])] * len(i[j][1])
                                                dist = edit_distance(len(i[j][1]), len(i[k][1]), i[j][1], i[k][1], arr)
                                                averages[j] += dist
                                                averages[k] += dist
                for a in range(0, len(averages)):
                        if averages[a] / num >= 10:
                                print ("\n------------------------------\nERROR:")
                                print (sorting.cell(2, column))
                                print (groupings[data.index(i)])
                                print (i[a])
                                print ("------------------------------")
