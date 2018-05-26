#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

def is_answer_check(question):
    while True:
        print('$ {0}'.format(question))
        answer = input()
        if answer != 'y' and answer != 'n':
            print('$ error:enter y or n')
            continue
        else:
            break
    return answer

def is_enter_check(question,disp1,disp2):
    print('$ {0}'.format(question))
    while True:
        print('$ {0}'.format(disp1))
        try:
            x_min = float(input())
        except:
            print('$ error:enter int or float')
            continue
        break
    while True:
        print('$ {0}'.format(disp2))
        try:
            x_max = float(input())
        except:
            print('$ error:enter int or float')
            continue
        if x_min >= x_max:
            print('$ error:x_max must be larger than x_min')
            continue
        break
    return x_min,x_max

def is_confirm_filename(dir_path,filename):
    confirm_filename = os.path.isfile(dir_path + '/' + filename)
    if confirm_filename == False:
        print('$ error:no file such as {0}'.format(filename))
        sys.exit()

def savefig():
    question = 'save figure?:y or n'
    ans = is_answer_check(question)
    if ans == 'y':
        print('$ enter file name')
        filename = input()
        print('$ save as {0}'.format(filename))
        plt.savefig(filename)

###plot configuration###
plt.rcParams['font.family']='sans-serif'
plt.rcParams['xtick.direction']='in'
plt.rcParams['ytick.direction']='in'
plt.rcParams['xtick.major.width']=1.0
plt.rcParams['ytick.major.width']=1.0
plt.rcParams['font.size']=20
plt.rcParams['axes.linewidth']=1.0

if __name__=='__main__':
    if len(sys.argv) < 2:
        target_dir_path = os.getcwd()
    else:
        target_dir_path = sys.argv[1]
    print('$ select data number')
    print('$ if no initial, enter bc')
    data_number = input()
    if data_number == 'bc':
        data_number = ''
    print('$ read data')
    freq_filename = data_number + 'freq.txt'
    LMAG_filename = data_number + 'LMAG_trace.txt'
    xgauss_filename = data_number + 'X_gauss.txt'
    is_confirm_filename(target_dir_path,freq_filename)
    is_confirm_filename(target_dir_path,LMAG_filename)
    is_confirm_filename(target_dir_path,xgauss_filename)
    data1 = pd.read_table(target_dir_path + '/' + freq_filename,header=None)
    data2 = pd.read_table(target_dir_path + '/' + LMAG_filename,header=None)
    field = pd.read_table(target_dir_path + '/' + xgauss_filename,header=None)
    freq = data1[0]/1000000000
    x_gauss = field[0]
    print('$ plot data in color')
    x,y = np.meshgrid(x_gauss,freq)
    plt.xlabel('external field /mT')
    plt.ylabel('resonant frequency /GHz')
    plt.pcolor(x,y,data2)
    plt.colorbar()
    plt.show(block=False)
    savefig()

    question_select_data = 'select data limit?: y or n'
    answer_select_data = is_answer_check(question_select_data)
    if answer_select_data == 'y':
        question_1 = 'enter external field limit'
        disp1_1 = 'enter Hex_min'
        disp1_2 = 'enter Hex_max'
        question_2 = 'enter frequency limit'
        disp2_1 = 'enter freq_min'
        disp2_2 = 'enter freq_max'
        while True:
            xlimit=is_enter_check(question_1,disp1_1,disp1_2)
            x_gauss_2 = x_gauss[x_gauss<xlimit[1]]
            x_gauss_2 = x_gauss_2[xlimit[0]<x_gauss_2]
            initial_index_x = x_gauss_2.index[0]
            end_index_x = x_gauss_2.index[-1]
            data2_2 = data2.iloc[:,initial_index_x:end_index_x+1]

            ylimit=is_enter_check(question_2,disp2_1,disp2_2)
            freq_2 = freq[freq<ylimit[1]]
            freq_2 = freq_2[ylimit[0]<freq_2]
            initial_index_y = freq_2.index[0]
            end_index_y = freq_2.index[-1]
            data2_2 = data2_2.iloc[initial_index_y:end_index_y+1,:]
            plt.close()
            print(x_gauss_2.shape)
            print(freq_2.shape)
            print(data2_2.shape)

            x,y = np.meshgrid(x_gauss_2,freq_2)
            plt.xlabel('external field/Oe')
            plt.ylabel('resonant frequency/GHz')
            plt.pcolor(x,y,data2_2)
            plt.tight_layout()
            plt.colorbar()
            plt.show(block=False)
            savefig()

            question_reselect_data = 'replot?:y or n'
            answer_reselect_data = is_answer_check(question_reselect_data)
            if answer_reselect_data == 'y':
                continue
            else:
                x_gauss = x_gauss_2
                freq = freq_2
                data2 = data2_2
                break

    question_sphere_data = 'select data sphere?:y or n'
    answer_select_data = is_answer_check(question_sphere_data)
    if answer_select_data == 'y':
        question_1 = 'enter external field sphere'
        disp1_1 = 'enter Hex_min'
        disp1_2 = 'enter Hex_max'
        question_2 = 'enter frequency sphere'
        disp2_1 = 'enter freq_min'
        disp2_2 = 'enter freq_max'
        while True:
            xsphere = is_enter_check(question_1,disp1_1,disp1_2)
            ysphere = is_enter_check(question_2,disp2_1,disp2_2)
            plt.close()
            x,y = np.meshgrid(x_gauss,freq)
            plt.xlabel('external field/Oe')
            plt.ylabel('resonant frequency/GHz')
            plt.pcolor(x,y,data2)
            plt.xlim([xsphere[0],xsphere[1]])
            plt.ylim([ysphere[0],ysphere[1]])
            plt.colorbar()
            plt.show(block=False)
            savefig()
            question_resphere_data = 'replot?:y or n'
            answer_resphere_data = is_answer_check(question_resphere_data)
            if answer_resphere_data == 'y':
                continue
            else:
                break
