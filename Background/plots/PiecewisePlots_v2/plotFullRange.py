from ROOT import *
import json
from collections import OrderedDict as od
from commonObjects import *

cat=0
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
canv = TCanvas("canv","canv",1200,1200)
canv.SetLeftMargin(0.15)
fulldatahist = TH1F("fulldatahist","fulldatahist",1320,9,75)
fullpdfhist = TH1F("fullpdfhist","fullpdfhist",52800,9,75)
data_hist = TH1F()

masslist = [11,13,15,18,22,26,31,37,45,55,67]
fitlist = ["Bernstein2","Bernstein2","Bernstein2","Bernstein2","Bernstein2","Bernstein2","Bernstein2","Bernstein2","Bernstein2","Bernstein2","Bernstein2"]

for win in range(1,12):
    pdf_file = TFile("pdfs_UntaggedTag_"+str(cat)+"_Window"+str(win)+"_"+fitlist[win-1]+".root","READ")
    pdf_hist = pdf_file.Get("h_pdf__Bernstein_2__CMS_hgg_mass")
    print(pdf_hist.GetMaximum())
    fullpdfhist.Add(pdf_hist)

for win in range(1,12):
    data_file = TFile("./data_UntaggedTag_"+str(cat)+"_Window"+str(win)+".root","READ")
    data_hist = data_file.Get("h_data__CMS_hgg_mass")
    fulldatahist.Add(data_hist)

fullmax = fulldatahist.GetMaximum()
fulldatahist.SetMinimum(0)
fulldatahist.SetMaximum(2.0*fullmax)
fulldatahist.SetMarkerStyle(20)
fulldatahist.SetMarkerColor(1)
fulldatahist.SetLineColor(1)
fulldatahist.Draw("epsame")

fullpdfhist.SetMinimum(0)
fullpdfhist.SetLineColor(3)
fullpdfhist.Draw("hist same")

# Add legend
leg = TLegend(0.55,0.68,0.85,0.88)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetTextSize(0.035)
leg.AddEntry(fulldatahist,"Data","ep")
leg.AddEntry(fullpdfhist, "Bernstein 2")
leg.Draw("Same")

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
canv.SaveAs("/eos/user/a/atsatsos/www/JUL2024FinalFits_SigExt_v2/PiecewisePlotTest_bern4_v2/bkgmodel_pdfs_%s_full.png"%cat)
canv.SaveAs("/eos/user/a/atsatsos/www/JUL2024FinalFits_SigExt_v2/PiecewisePlotTest_bern4_v2/bkgmodel_pdfs_%s_full.pdf"%cat)

print(fulldatahist.Integral())
print(fullpdfhist.Integral())
