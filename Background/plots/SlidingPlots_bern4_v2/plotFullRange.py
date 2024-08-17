from ROOT import *
import json
from collections import OrderedDict as od
from commonObjects import *

cat=1

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
canv = TCanvas("canv","canv",1200,1200)
canv.SetLeftMargin(0.15)

fulldatahist1 = TH1F("fulldatahist1","fulldatahist1",1320,9,75)
fulldatahist2 = TH1F("fulldatahist2","fulldatahist2",1320,9,75)
fullpdfhist1 = TH1F("fullpdfhist1","fullpdfhist1",52800,9,75)
fullpdfhist2 = TH1F("fullpdfhist2","fullpdfhist2",52800,9,75)

masslist = [11,13,15,18,22,26,31,37,45,55,67]
fitlist = ["Exponential1","Bernstein4","Bernstein2","Bernstein3","Bernstein2","Bernstein4","Bernstein2","Exponential1","Bernstein4","Bernstein3","Bernstein4"]

for i in range(0,11):
    if(i%2==0):
        pdf_file1 = TFile("pdfs_UntaggedTag_"+str(cat)+"_"+str(masslist[i])+"GeV_"+fitlist[i]+".root","READ")
        pdf_hist1 = pdf_file1.Get("h_pdf__"+fitlist[i][:-1]+"_"+fitlist[i][-1:]+"__CMS_hgg_mass")
        fullpdfhist1.Add(pdf_hist1)
        pdf_hist1.Delete()
    else:
        pdf_file2 = TFile("pdfs_UntaggedTag_"+str(cat)+"_"+str(masslist[i])+"GeV_"+fitlist[i]+".root","READ")
        pdf_hist2 = pdf_file2.Get("h_pdf__"+fitlist[i][:-1]+"_"+fitlist[i][-1:]+"__CMS_hgg_mass")
        fullpdfhist2.Add(pdf_hist2)
        pdf_hist2.Delete()

for i in range(0,11):
    if(i%2==0):
        data_file1 = TFile("./data_UntaggedTag_"+str(cat)+"_"+str(masslist[i])+"GeV.root","READ")
        data_hist1 = data_file1.Get("h_data__CMS_hgg_mass")
        fulldatahist1.Add(data_hist1)
        data_hist1.Delete()
    else:
        data_file2 = TFile("./data_UntaggedTag_"+str(cat)+"_"+str(masslist[i])+"GeV.root","READ")
        data_hist2 = data_file2.Get("h_data__CMS_hgg_mass")
        fulldatahist2.Add(data_hist2)
        data_hist2.Delete()


fullmax1 = fulldatahist1.GetMaximum()
fulldatahist1.SetMinimum(0)
fulldatahist1.SetMaximum(2.0*fullmax1)
fulldatahist1.SetMarkerStyle(20)
fulldatahist1.SetMarkerColor(1)
fulldatahist1.SetLineColor(1)
fulldatahist1.Draw("epsame")

fullmax2 = fulldatahist2.GetMaximum()
fulldatahist2.SetMinimum(0)
fulldatahist2.SetMaximum(2.0*fullmax2)
fulldatahist2.SetMarkerStyle(20)
fulldatahist2.SetMarkerColor(1)
fulldatahist2.SetLineColor(1)
fulldatahist2.Draw("epsame")

fullpdfhist1.SetMinimum(0)
fullpdfhist1.SetLineWidth(3)
fullpdfhist1.SetLineColor(5)
fullpdfhist1.Draw("hist same")

fullpdfhist2.SetMinimum(0)
fullpdfhist2.SetLineWidth(3)
fullpdfhist2.SetLineColor(7)
fullpdfhist2.Draw("hist same")


# Add legend
leg1 = TLegend(0.35,0.53,0.60,0.88)
leg1.SetFillStyle(0)
leg1.SetLineColor(0)
leg1.SetTextSize(0.02)
leg1.AddEntry(fullpdfhist1, str(masslist[0])+" GeV: "+fitlist[0][:-1]+" "+fitlist[0][-1:])
leg1.AddEntry(fullpdfhist2, str(masslist[1])+" GeV: "+fitlist[1][:-1]+" "+fitlist[1][-1:])
leg1.AddEntry(fullpdfhist1, str(masslist[2])+" GeV: "+fitlist[2][:-1]+" "+fitlist[2][-1:])
leg1.AddEntry(fullpdfhist2, str(masslist[3])+" GeV: "+fitlist[3][:-1]+" "+fitlist[3][-1:])
leg1.AddEntry(fullpdfhist1, str(masslist[4])+" GeV: "+fitlist[4][:-1]+" "+fitlist[4][-1:])
leg1.AddEntry(fullpdfhist2, str(masslist[5])+" GeV: "+fitlist[5][:-1]+" "+fitlist[5][-1:])

leg2 = TLegend(0.60,0.53,0.85,0.88)
leg2.SetFillStyle(0)
leg2.SetLineColor(0)
leg2.SetTextSize(0.02)
leg2.AddEntry(fullpdfhist1, str(masslist[6])+" GeV: "+fitlist[6][:-1]+" "+fitlist[6][-1:])
leg2.AddEntry(fullpdfhist2, str(masslist[7])+" GeV: "+fitlist[7][:-1]+" "+fitlist[7][-1:])
leg2.AddEntry(fullpdfhist1, str(masslist[8])+" GeV: "+fitlist[8][:-1]+" "+fitlist[8][-1:])
leg2.AddEntry(fullpdfhist2, str(masslist[9])+" GeV: "+fitlist[9][:-1]+" "+fitlist[9][-1:])
leg2.AddEntry(fullpdfhist1, str(masslist[10])+" GeV: "+fitlist[10][:-1]+" "+fitlist[10][-1:])
leg2.AddEntry(fulldatahist1,"Data","ep")

leg1.Draw("same")
leg2.Draw("same")
canv.Update()

# Add Latex
lat = TLatex()
lat.SetTextFont(42)
lat.SetTextAlign(31)
lat.SetNDC()
lat.SetTextSize(0.035)
lat.DrawLatex(0.9,0.92,"5.44 fb^{-1} (13 TeV)")

lat1 = TLatex()
lat1.SetTextFont(42)
lat1.SetTextAlign(11)
lat1.SetNDC()
lat1.SetTextSize(0.035)
lat1.DrawLatex(0.15,0.92,"Category: UntaggedTag_%s"%cat)

canv.Update()
canv.SaveAs("/eos/user/a/atsatsos/www/JUL2024FinalFits_SigExt_v2/SlidingPlotTest_bern4_v2/bkgmodel_pdfs_%s_full.png"%cat)
canv.SaveAs("/eos/user/a/atsatsos/www/JUL2024FinalFits_SigExt_v2/SlidingPlotTest_bern4_v2/bkgmodel_pdfs_%s_full.pdf"%cat)

print(fulldatahist1.Integral())
print(fulldatahist2.Integral())
print(fullpdfhist1.Integral())
print(fullpdfhist2.Integral())

