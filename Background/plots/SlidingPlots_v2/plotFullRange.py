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
fullpdfhist = TH1F()
data_hist = TH1F()

masslist =[11,13,15,18,22,26,31,37,45,55,67]
norms = [563,751,787,797,888,931,999,1327,1824,2558,2957]


for win in range(1,12):
    data_file = TFile("../PiecewisePlots/data_UntaggedTag_"+str(cat)+"_Window"+str(win)+".root","READ")

    data_hist = data_file.Get("h_data__CMS_hgg_mass")
    fulldatahist.Add(data_hist)

fullmax = fulldatahist.GetMaximum()
fulldatahist.SetMaximum(4.0*fullmax)
fulldatahist.SetMarkerStyle(20)
fulldatahist.SetMarkerColor(1)
fulldatahist.SetLineColor(1)
fulldatahist.Draw("ep")

for i,mass in enumerate(masslist):
    pdf_file = TFile("pdfs_UntaggedTag_"+str(cat)+"_"+str(mass)+"GeV_Bernstein2.root","READ")
    pdf_hist = pdf_file.Get("h_pdf__Bernstein_2__CMS_hgg_mass")
    #tempmin = pdf_hist_temp.GetXaxis().GetXmin()
    #tempmax = pdf_hist_temp.GetXaxis().GetXmax()
    #pdf_hist = TH1F("pdf_hist","pdf_hist",52800,9,75)
    #pdf_hist.Add(pdf_hist_temp)
    pdf_hist.SetLineColor(2)
    pdf_hist.SetLineWidth(2)
    pdf_hist.Scale(1.0/40.0)
    pdf_hist.SetMinimum(0)
    fullpdfhist.Add(pdf_hist)

fullpdfhist.Draw("histsame")

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
canv.SaveAs("/eos/user/a/atsatsos/www/JUL2024FinalFits_SigExt_v2/SlidingPlotTest_v2/bkgmodel_pdfs_%s_full.png"%cat)
canv.SaveAs("/eos/user/a/atsatsos/www/JUL2024FinalFits_SigExt_v2/SlidingPlotTest_v2/bkgmodel_pdfs_%s_full.pdf"%cat)


