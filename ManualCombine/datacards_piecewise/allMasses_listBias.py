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

cat = "1"
pdfidx = "4"
mass_list = [10, 12.25, 15, 18.5, 22.75, 27.75, 34, 41.75, 51, 62.25]
#mass_list = [10]

means = []
sigmas = []

# Loop over masses from 10 to 70 GeV in steps of 5 GeV
for i,mass in enumerate(mass_list):
    mass_str = str(mass)

    # Open fit diagnostics file for current mass
    #f = TFile("m" + mass_str + "_backup/fitDiagnosticsTest.root", "READ")
    #f = TFile("envelope_cat"+cat+"/fitDiagnosticsEnvelopeCat"+cat+"W"+str(i+1)+".root", "READ")
    f = TFile("freezepdf"+pdfidx+"_cat"+cat+"/fitDiagnosticsFreeze"+pdfidx+"Cat"+cat+"W"+str(i+1)+".root", "READ")
    print f
    #f = TFile("condorSub/m" + mass_str + "/fitDiagnosticsTest.root", "READ")
    t = f.Get("tree_fit_sb")
    h = TH1F("h", "h", 56, -7, 7)

    # Define r_toys and draw histogram
    r_toys = 0.0
    t.Draw("(r-0.0)/(0.5*(rHiErr+rLoErr))>>h", "fit_status>=0")

    # Fit histogram with Gaussian
    h.Fit("gaus")

    # Create canvas
    c = TCanvas("c", "c", 1000, 800)
    c.cd()

    # Draw histogram
    h.GetXaxis().SetTitleOffset(1.1)
    h.GetXaxis().SetTitle("(r - r_{toys})/(0.5 * (r_{HiErr} + r_{LoErr}))")
    h.GetYaxis().SetTitle("Entries")
    h.SetLineColor(ROOT.kAzure-2)
    h.SetFillColor(ROOT.kAzure-9)
    h.SetTitle("")
    h.Draw()

    fit_function = h.GetFunction("gaus")
    fit_function.SetLineWidth(2)
    fit_function.SetLineColor(ROOT.kMagenta-7)

    # Get fit results
    fit_mean = h.GetFunction("gaus").GetParameter(1)
    fit_sigma = h.GetFunction("gaus").GetParameter(2)
    means.append(fit_mean)
    sigmas.append(fit_sigma)

    # Close canvas and file
    c.Close()
    f.Close()

print "PDF Index: ", pdfidx
print "Cat: ", cat
print "Means: ", means
print "Sigmas: ", sigmas
