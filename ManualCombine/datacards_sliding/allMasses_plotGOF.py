from ROOT import *
import ROOT, array, CMSGraphics, CMS_lumi, random
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooDataHist, RooCBShape, RooNumConvPdf, RooFFTConvPdf                   
from ROOT import gStyle, TStyle, TGraph, TGraphErrors, TMath, TMultiGraph, TLine, gPad, TGaxis, TLegend, TText, TLatex, TColor, TPaveText        
from ROOT import TAttFill, TLegend, TRatioPlot, TPad, THStack                                                                
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kPink, kGreen, kYellow, kCyan                                                                 
import argparse
import sys                                                                                                                               
import os                                                                                                                                     
ROOT.gROOT.SetBatch()                                                                                                                 
ROOT.gStyle.SetOptStat(0)                                                                                              
ROOT.gStyle.SetOptTitle(0)    

#cat = "cat1"
#mass_list = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

mass_list = []
pval_list = []

# Loop over masses from 10 to 70 GeV in steps of 5 GeV
for mass in range(10,71):
    mass_list.append(mass)
    mass_str = str(mass)
    cat = "condorSub/cat1/"
#    cat = "./cat1_gof/"
    f_data = TFile(cat+"/higgsCombineTest.GoodnessOfFit.mH"+mass_str+".root","READ")                                 
    t_data = f_data.Get("limit")                                                                                                               
    t_data.GetEntry(0)                                                                                                                                 
    q_data = t_data.limit                                                                                                            
    print("data test stat. is:",str(q_data))                                                                                                   
    f_toys = TFile(cat+"/higgsCombineToys.GoodnessOfFit.mH"+mass_str+".123456.root","READ")                                                                  
    t_toys = f_toys.Get("limit")
    t_toys.Print()

    h_lt = TH1F("h_lt","h_lt",200,0.0,0.05)                                                                                                 
    h_gt = TH1F("h_gt","h_gt",200,0.0,0.05)                                                                                    
    #h_lt = TH1F("h_lt","h_lt",100,0.0,0.01)                                                                                                 
    #h_gt = TH1F("h_gt","h_gt",100,0.0,0.01)                                                                                    
    t_toys.Draw("limit>>h_lt","limit<"+str(q_data),"goff")                                                                      
    t_toys.Draw("limit>>h_gt","limit>"+str(q_data),"goff")                             
    

    c = TCanvas("c", "c", 1000, 800)
    c.cd()

    h_lt.GetXaxis().SetTitleOffset(1.1)
    h_lt.GetXaxis().SetTitle("Data test statistics")
    h_lt.GetYaxis().SetTitle("Entries")
    h_lt.SetMaximum(1.2*max(h_lt.GetMaximum(),h_gt.GetMaximum()))                                                                   
    h_lt.SetLineWidth(2)
    h_lt.SetLineColor(ROOT.kAzure-2)
    h_lt.Draw()                                                                                                                    
    h_gt.SetFillColor(ROOT.kCyan+1)
    h_gt.Draw("same")                                                                                                                           

    # Print fit results on canvas
    text = TLatex()
    text.SetTextSize(0.04)
    massText = "Mass hyp = "+mass_str+" GeV"
    text.DrawLatexNDC(0.6, 0.75, massText)
    pval = h_gt.Integral()/(h_lt.Integral()+h_gt.Integral())
    text.SetTextSize(0.03)
    text.SetTextFont(20)
    text.DrawLatexNDC(0.6, 0.7, "Test statistics: %.5f" % q_data)
    text.DrawLatexNDC(0.6, 0.65, "pval: %.6f" % pval)

    pval_list.append(pval)

    # CMS lumi info                                                                                                                       
    CMS_lumi.writeExtraText = True                                                           
    CMS_lumi.extraText      = " Preliminary"                                                                                       
    CMS_lumi.lumi_sqrtS     = "13 TeV"                                                                                                          
    CMS_lumi.cmsTextSize    = 0.6                                                                                                                    
    CMS_lumi.lumiTextSize   = 0.46                                                                                                              
    CMS_lumi.extraOverCmsTextSize = 0.75                                                                                                
    CMS_lumi.relPosX = 0.12                                                                                                      
    CMS_lumi.CMS_lumi(c, 0, 0) 
    
    # Save canvas as pdf and png
    c.SaveAs(cat+"gof_m" + mass_str + "_fourCat_sliding_cat1.pdf")
    c.SaveAs(cat+"gof_m" + mass_str + "_fourCat_sliding_cat1.png")
    print("h_lt.Integral = :",h_lt.Integral()) 
    print("h_gt.Integral = :",h_gt.Integral()) 
    print("p-val:",h_gt.Integral()/(h_lt.Integral()+h_gt.Integral())) 

    # Close canvas and file
    c.Close()
    f_data.Close()    
    f_toys.Close()

print(mass_list)
print(pval_list)
