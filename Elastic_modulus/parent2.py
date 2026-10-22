import os
import subprocess
import numpy as np
import time
import props as p

data1 =np.loadtxt('results_emod_with_pressure')
#data1=np.loadtxt('stat_mat_output')   # use this while considering averaged first step results

len=len(data1)
tt=np.zeros(len)
e_matrix=np.zeros(len)
pois_matrix=np.zeros(len)
#pore_vol=np.zeros(len)
#mat_vol=np.zeros(len)

for i in xrange(len):
    tt[i]=data1[i][0]
    e_matrix[i]=data1[i][1]
    pois_matrix[i]=data1[i][2]

for i in xrange(len):
    tk=tt[i]
    emod_mat=e_matrix[i]
    f=open('emod_mat%d'%tk,'w')
    f.write(str(emod_mat))
    f.close()
    pois_mat=pois_matrix[i]
    f=open('pois_mat%d'%tk,'w')
    f.write(str(pois_mat))
    f.close()

    f=open('mod-fib%d'%tk,'w')
    f.write(str(p.mod_fib))
    f.close()

    f=open('pois-fib%d'%tk,'w')
    f.write(str(p.pois_fib))
    f.close()

    f=open('run_p.job', 'w')
    f.write("#!/bin/bash")
    f.write("\n")
    f.write("#PBS -N P%d"%tk)
    f.write("\n")
    f.write("#PBS -W group_list=oiz")
    f.write("\n")
    f.write("#PBS -q standard")
    f.write("\n")
    f.write("#PBS -l select=1:ncpus=8:mem=48gb:pcmem=6gb")
    f.write("\n")
    f.write("#PBS -l place=free:shared")
    f.write("\n")
    f.write("#PBS -l walltime=00:40:00")
    f.write("\n")
    f.write("#PBS -l cput=00:40:00")
    f.write("\n")
    f.write("cd /home/u23/tejakondury/ONYX")
    f.write("\n")
    #f.write("abaqus cae noGUI=comp_emod_2d_fibs.py ")
    f.write("abaqus cae noGUI=comp_emod_3d_fibs.py ")  # choose a different file for long props
    f.close()

    os.environ['tt']=str(tk)

    subprocess.call('qsub -v tt=$tt run_p.job',shell=True)

    print('analysis is submitted for temp',tk)

    time.sleep(45)
