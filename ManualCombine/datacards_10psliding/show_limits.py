import ROOT, array, CMSGraphics, CMS_lumi, random, copy
import os,sys
from ROOT import TGraphAsymmErrors
from ROOT import TGraphErrors
from ROOT import TColor
from array import array
from ROOT import *
from operator import truediv
import random
import math
from glob import glob
import re 
import sys
from math import sqrt

limit1obs=array('d')
limit1=array('d')
limiteps2=array('d')
limit190=array('d')
limiteps290=array('d')
limit195up=array('d')
limit195down=array('d')
limit168up=array('d')
limit168down=array('d')
limit1Observed=array('d')
limit2=array('d')
limit2eps2=array('d')
limit290=array('d')
limit2eps290=array('d')
limit295up=array('d')
limit295down=array('d')
limit268up=array('d')
limit268down=array('d')
limit2Observed=array('d')
mass1=array('d')
mass2=array('d')
masserr1=array('d')
masserr2=array('d')


# lumi = 62.4
# lumi_project = 62.4

#lumi = 54.4
lumi = 5.44
lumi_project = 54.4 

param_scale = 1.

cat = "cat01"
combine_output = "./limits_"+cat+"/"

files = glob(combine_output + "higgsCombineTest.AsymptoticLimits.mH*.root")

masses = []
file_list = []

masses5 = []
limits5 = []

for fname in files:
        m = fname.split("mH")[1].rstrip(".root")
        masses.append(float(m))
        #print("m = ", str(m))
        fname = combine_output + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root"
        file_list.append(fname)
masses.sort()

i=0
for m in masses:
        #print("File: ", file_list[i])
        f=ROOT.TFile.Open(file_list[i])
        #f=ROOT.TFile.Open(combine_output + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root")
        tree=f.Get("limit")

        tree.GetEntry(5)
        limit1obs.append(math.sqrt(lumi/lumi_project)*tree.limit/param_scale)

        tree.GetEntry(2)
        limit1.append(math.sqrt(lumi/lumi_project)*tree.limit/param_scale)
        #print("limit from rootFile", tree.limit)
        #print("limit", math.sqrt(lumi/lumi_project)*tree.limit/param_scale)
        if (m%5 == 0): limits5.append(round(math.sqrt(lumi/lumi_project)*tree.limit/param_scale, 3))
        
        tree.GetEntry(0)
        limit195up.append(abs(math.sqrt(lumi/lumi_project)*tree.limit/param_scale-limit1[-1]))
        
        tree.GetEntry(4)
        limit195down.append(abs(math.sqrt(lumi/lumi_project)*tree.limit/param_scale-limit1[-1]))
        
        tree.GetEntry(1)
        limit168up.append(abs(math.sqrt(lumi/lumi_project)*tree.limit/param_scale-limit1[-1]))

        tree.GetEntry(3)
        limit168down.append(abs(math.sqrt(lumi/lumi_project)*tree.limit/param_scale-limit1[-1]))
            
        mass1.append(m)
        masserr1.append(0.)

        if (m%5 == 0): masses5.append(m)

        i+=1
print(cat)
print(masses5)
print(limits5)

