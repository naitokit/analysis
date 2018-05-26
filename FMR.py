#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import numpy as np
import scipy.optimize
import math
import matplotlib.pyplot as plt
import os

#Fitting function(lorenssian)
#def lorenssian(x,A,x0,r):
#    f = A*(r/2)**2/((r/2)**2+(x-x0)**2)+A*r/2*(x-x0)**2/((r/2)**2+(x-x0)**2)
#    return f

def lorenssian(x,A_1,A_2,x0,r):
    f = A_1*r**2/(r**2+(x-x0)**2)+A_2*r*(x-x0)/(r**2+(x-x0)**2)
    return f

#Fitting function(for_plot)
def lorenssian_for_plot(x, param):
    f = lorenssian(x, param[0], param[1], param[2], param[3]) + param[4]
    return f

#Residual function
def residuals(param,x,y):
    A_1 = param[0]
    A_2 = param[1]
    x0 = param[2]
    r  = param[3]
    base = param[4]
    error = (y-(lorenssian(x,A_1,A_2,x0,r)+base))
    return error

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

#Plot configuration
plt.rcParams['font.family']='sans-serif'
plt.rcParams['xtick.direction']='in'
plt.rcParams['ytick.direction']='in'
plt.rcParams['xtick.major.width']=1.0
plt.rcParams['ytick.major.width']=1.0
plt.rcParams['font.size']=10
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
    LMAG_filename = data_number + 'averagedLMAG_trace.txt'
    xgauss_filename = data_number + 'X_gauss.txt'
    is_confirm_filename(target_dir_path,freq_filename)
    is_confirm_filename(target_dir_path,LMAG_filename)
    is_confirm_filename(target_dir_path,xgauss_filename)
    data1 = pd.read_table(target_dir_path + '/' + freq_filename,header=None)
    data2 = pd.read_table(target_dir_path + '/' + LMAG_filename,header=None)
    field = pd.read_table(target_dir_path + '/' + xgauss_filename,header=None)
    xdata = data1[0]/1000000000
    x_gauss = field[0]

    while True:
        while True: 
            while True:
                print('$ input start data number')
                start_index = int(input())-1
                if start_index>=len(field):
                    print('$ error:start data number is over the last data number')
                    continue
                elif start_index<0:
                    print('$ error:start data number must be larger than 1')
                    continue
                break
            index = start_index
            end_index=start_index+24
#            end_index=start_index+15
            index_for_subplot = 1
            graph_number = 5
#            graph_number = 4
            while index<=end_index:
                ydata_for_all = data2[index]
                plt.subplot(graph_number,graph_number,index_for_subplot)
                plt.subplots_adjust(wspace=0.4,hspace=0.6)
                plt.plot(xdata,ydata_for_all,color='red')
                plt.xlabel('frequency /GHz')
                plt.ylabel(r'LMAG($S_{11}$)')
                plt.xlim([0.0,20.0])
                plt.title('external field /mT = %f' % x_gauss[index],loc='center')
                index += 1
                index_for_subplot += 1
            print('$ display fitting graph')
            plt.show(block=False)
            question_1 = 'start fitting?: y or n'
            answer_start_fitting = is_answer_check(question_1)
            if answer_start_fitting == 'y':
                break
            else:
                plt.close()
                continue
        savefig()
        plt.close()
        print('$ display fitting start data')
        ydata = data2[start_index]
        plt.plot(xdata,ydata,color='red')
        plt.xlabel('frequency /GHz')
        plt.ylabel(r'LogMag($S_{11}$)')
#        plt.title('external field/mT = %f' % x_gauss[start_index],loc='center')
        plt.tight_layout()
        plt.show(block=False)
        savefig()

    #Fitting start parameter
        print('$ input initial fitting parameter')
        print('Amplitude_1')
        amplitude_1 = float(input())
        print('Amplitude_2')
        amplitude_2 = float(input())
        print('Center')
        center = float(input())
        print('Gamma')
        gamma = float(input())
        print('Baseline')
        baseline = float(input())
        plt.close()
        result_center = []
        result_gamma = []
        index = start_index
        index_for_subplot = 1
        while index<=end_index:
            ydata = data2[index]
            initial_param = [amplitude_1, amplitude_2, center, gamma, baseline]
            result = scipy.optimize.leastsq(residuals,initial_param,args=(xdata,ydata))
            param_result = result[0] # fitted parameters
            covar_result = result[1] # covariant matrix
            amplitude_1 = param_result[0]
            amplitude_2 = param_result[1]
            center = param_result[2]
            gamma = param_result[3]
            baseline = param_result[4]
            print("data number:",index+1)
            print("x_gauss   : %f" % x_gauss[index]) 
            print("Amplitude_1 : %f" % (param_result[0]/(2*math.pi*param_result[2])))
            print("Amplitude_2 : %f" % (param_result[1]/(2*math.pi*param_result[2])))
            print("Center    : %f" % (param_result[2]))
            print("gamma     : %f" % (param_result[3]))
            print("Baseline  : %f" % (param_result[4]))
            print("====================")

            result_center.append(center)
            result_gamma.append(gamma)

            plt.subplots_adjust(wspace=0.4,hspace=0.6)
            plt.subplot(graph_number,graph_number,index_for_subplot)
            plt.plot(xdata, ydata, color="red")
            plt.plot(xdata, lorenssian_for_plot(xdata,param_result),color="blue",linestyle="-")
#            plt.legend(['Measured Data', 'Fit', 'True'],fontsize=5)
            plt.xlabel('frequency /GHz')
            plt.ylabel(r'LMAG($S_{11}$)')
            plt.title('external field = %f' % x_gauss[index],loc='center')
            plt.xlim([0.0,20.0])
    #    plt.ylim([-0.1,0.01])
            index += 1
            index_for_subplot += 1
    #plt.savefig('fit_lorenssian.eps',dpi=150,transparent=True)
        print('$ display fitting result')
        plt.show(block=False)
        question_2 = 'Refitting?:y or n'
        answer_continue = is_answer_check(question_2)
        if answer_continue == 'n':
            savefig()
            plt.close()
            break
        if answer_continue == 'y':
            plt.close()
            print('$ Reset fitting data')
            index_for_subplot = 1
            index = start_index
            continue
    question_3 = 'save data? y or n'
    answer_save = is_answer_check(question_3)
    savefilename = data_number + 'fitresult.txt'
    if answer_save == 'y':
        print('$ save result as {0}'.format(savefilename))
        save_path_name = target_dir_path + '/' + savefilename
        confirm_filename = os.path.isfile(save_path_name)
        if confirm_filename == True:
            file_use = open(save_path_name,'a')
            index = 0
            end_index = len(result_center)-1
            while index<=end_index:
                file_use.write('\n' + str(x_gauss[index+start_index]) + '\t' + str(result_center[index]) + '\t' + str(result_gamma[index]))
                index += 1
            file_use.close
        else:
            file_use = open(save_path_name,'w')
            file_use.write('Field/mT' '\t' 'Resonant_frequency/GHz' '\t' 'FWHM/GHz')
            index = 0
            end_index = len(result_center)-1
            while index<=end_index:
                file_use.write('\n' + str(x_gauss[index+start_index]) + '\t' + str(result_center[index]) + '\t' + str(result_gamma[index]))
                index += 1
            file_use.close
