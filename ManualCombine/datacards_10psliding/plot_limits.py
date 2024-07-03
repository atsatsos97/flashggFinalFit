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

cat = "cat3"
combine_output = "./limits_"+cat+"/"
combine_plots = "/eos/user/a/atsatsos/www/JUN2024FinalFits_SigExt_v2/10pData_4Cat_SlidingWindow_SigExt_vExp2/"
if not os.path.exists(combine_plots):
    # If not, create it
    os.makedirs(combine_plots)
#    print(f"Directory '{combine_plots}' created.")

files = glob(combine_output + "higgsCombineTest.AsymptoticLimits.mH*.root")

masses = []
file_list = []
masses5 = []
limits5 = []

for fname in files:
        m = fname.split("mH")[1].rstrip(".root")
        masses.append(float(m))
        print("m = ", str(m))
        fname = combine_output + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root"
        file_list.append(fname)
masses.sort()

i=0
for m in masses:
        print("File: ", file_list[i])
        f=ROOT.TFile.Open(file_list[i])
        #f=ROOT.TFile.Open(combine_output + "higgsCombineTest.AsymptoticLimits.mH"+str(m)+".root")
        tree=f.Get("limit")

        tree.GetEntry(5)
        limit1obs.append(math.sqrt(lumi/lumi_project)*tree.limit/param_scale)

        tree.GetEntry(2)
        limit1.append(math.sqrt(lumi/lumi_project)*tree.limit/param_scale)
        print("limit from rootFile", tree.limit)
        #print("limit", math.sqrt(lumi/lumi_project)*tree.limit/param_scale)
        if (m%5 == 0): limits5.append(math.sqrt(lumi/lumi_project)*tree.limit/param_scale)
        
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

#lhcbmass=array('d')
#lhcblimit=array('d')

print(masses5)
print(limits5)
#print(limit1obs)

#with open("resources/LHCb_Aaij2019bvg_prompt.lmt","r") as f:
#        for line in f:
#                print("LHCb",line.split()[0],line.split()[1])

#                if (float(line.split()[0])<0.212): continue
#                if (float(line.split()[0])>0.5): continue
                
#                lhcbmass.append(float(line.split()[0]))
#                lhcblimit.append(float(line.split()[1]))

c1=ROOT.TCanvas("c1","c1",700,500)
#c1.SetGrid()
c1.SetLogy()
#c1.SetLogx()
c1.SetBottomMargin(0.15)

mg=ROOT.TMultiGraph()
mg.SetMaximum(100.0)
mgeps=ROOT.TMultiGraph()
graph_limit1=ROOT.TGraph(len(mass1),mass1,limit1)
#graph_limit1.SetTitle("graph_limit1")
graph_limit1.SetMarkerSize(1)
graph_limit1.SetMarkerStyle(20)
graph_limit1.SetMarkerColor(kBlack)
graph_limit1.SetLineWidth(2)
graph_limit1.SetLineStyle(7)
#graph_limit1.GetYaxis().SetRangeUser(0,100)
#graph_limit1.GetXaxis().SetRangeUser(0.2,0.6)
graph_limit1.GetXaxis().SetMoreLogLabels()
graph_limit1.GetYaxis().SetTitle("#sigma_{gg #rightarrow #phi} x BR(#phi #rightarrow #gamma#gamma) [pb]")
graph_limit1.GetYaxis().SetTitleSize(0.04)
graph_limit1.GetXaxis().SetTitle("m_{#phi} [GeV]")

graph_limit1obs=ROOT.TGraph(len(mass1),mass1,limit1obs)
graph_limit1.SetTitle("graph_limit1obs")
graph_limit1.SetMarkerSize(1)
graph_limit1.SetMarkerStyle(20)
graph_limit1.SetMarkerColor(kBlack)
graph_limit1.SetLineWidth(2)
graph_limit1.SetLineStyle(1)

graph_limit195up=ROOT.TGraphAsymmErrors(len(mass1),mass1,limit1,masserr1,masserr1,limit195up,limit195down)
graph_limit195up.SetTitle("graph_limit195up")
graph_limit195up.SetFillColor(ROOT.TColor.GetColor(252,241,15))

graph_limit168up=ROOT.TGraphAsymmErrors(len(mass1),mass1,limit1,masserr1,masserr1,limit168up,limit168down)
graph_limit168up.SetTitle("graph_limit168up")
graph_limit168up.SetFillColor(kGreen);
graph_limit168up.SetMarkerColor(kGreen)

#graph_lhcb=ROOT.TGraph(len(lhcbmass),lhcbmass,lhcblimit)
#graph_lhcb.SetTitle("graph_lhcb")
#graph_lhcb.SetMarkerSize(0.001)
#graph_lhcb.SetMarkerStyle(20)
#graph_lhcb.SetMarkerColor(4)
#graph_lhcb.SetLineWidth(2)
#graph_lhcb.SetLineColor(4)
#graph_lhcb.SetLineStyle(1)

mg.Add(graph_limit195up,"3")
mg.Add(graph_limit168up,"3")
mg.Add(graph_limit1,"pl")
mg.Add(graph_limit1obs,"pl")
#mg.Add(graph_lhcb,"pl")

mg.Draw("APC")

mg.GetYaxis().SetTitle("#sigma_{gg #rightarrow #phi} x BR(#phi #rightarrow #gamma#gamma) [pb] ")
mg.GetYaxis().SetTitleOffset(1.01)
mg.GetYaxis().SetTitleSize(0.035)
mg.GetXaxis().SetTitle("m_{#phi} [GeV]")
mg.GetXaxis().SetTitleSize(0.05)
mg.GetXaxis().SetMoreLogLabels()
c1.Update()
legend=ROOT.TLegend(0.6,0.65,0.85,0.8)

# CMS lumi info                                                                                                                          
CMS_lumi.writeExtraText = True                                                                                                        
CMS_lumi.extraText = "  Preliminary"                                                                                
CMS_lumi.lumi_sqrtS = str(lumi_project) + " fb^{-1} (13 TeV)"                                                                                             
CMS_lumi.cmsTextSize = 0.6                                                                                                       
CMS_lumi.lumiTextSize = 0.46                                                                                               
CMS_lumi.extraOverCmsTextSize = 0.75                                                                                          
CMS_lumi.relPosX = 0.12                                                                                       
CMS_lumi.CMS_lumi(c1, 0, 0) 

#leg=ROOT.TLegend(0.2,0.25,0.55,0.5)
leg=ROOT.TLegend(0.6,0.63,0.88,0.8)
leg.SetTextSize(0.025)
leg.SetBorderSize( 0 )
leg.SetFillStyle( 1001 )
leg.SetFillColor(kWhite) 
leg.SetHeader("Category "+cat[3:],"C")
#leg.AddEntry( obse , "Observed",  "LP" )
leg.AddEntry( graph_limit1 , "Expected",  "LP" )
leg.AddEntry( graph_limit168up, "#pm 1#sigma",  "F" ) 
leg.AddEntry( graph_limit195up, "#pm 2#sigma",  "F" ) 
leg.AddEntry( graph_limit1obs, "Obs (blinded)",  "L" ) 
#leg.AddEntry( graph_limit1obs, "Obs",  "F" ) 
leg.Draw("same")
c1.SaveAs(combine_plots + "limitLowMassDiPhoton_sigext_fourCat_slidingwindow_"+cat+"_obs.root")
c1.SaveAs(combine_plots + "limitLowMassDiPhoton_sigext_fourCat_slidingwindow_"+cat+"_obs.pdf")
c1.SaveAs(combine_plots + "limitLowMassDiPhoton_sigext_fourCat_slidingwindow_"+cat+"_obs.png")
