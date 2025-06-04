import ROOT, array, CMSGraphics, CMS_lumi, random, copy
import os, sys, re
from glob import glob
from ROOT import TGraphAsymmErrors, TGraphErrors, TColor, gStyle, gROOT, kGray
from array import array
from math import sqrt
import numpy as np

ROOT.gROOT.SetBatch()                                                    
ROOT.gStyle.SetOptStat(0)                                                        
ROOT.gStyle.SetOptTitle(0)

# Define arrays
pvals = array('d')
mass1 = array('d')

# Lumi settings
lumi, lumi_project = 54.4, 54.4
#lumi, lumi_project = 5.44, 54.4
param_scale = 1
cat = "0"
combine_output = f"./pval_cat{cat}_AllData/"
combine_plots = '/eos/user/e/elfontan/www/Hgg_veryLowMass_Paper/'

if not os.path.exists(combine_plots):
    os.makedirs(combine_plots)

files = glob(combine_output + "higgsCombineTest.Significance.mH*.root")

masses, file_list = [], []

mass_pattern = re.compile(r"higgsCombineTest\.Significance\.mH(\d+(\.\d+)?)\.root")

for fname in files:
    match = mass_pattern.search(fname)
    if match:
        m_str = match.group(1)  # This will capture the mass part (either integer or float)
        mass = float(m_str)
        #print(mass)
        if mass.is_integer():
            m = int(mass)  # Keep as an integer if there's no decimal part
        else:
            m = mass
        #print(m)
        #print("----------------------------")
        masses.append(m)
        f = combine_output + "higgsCombineTest.Significance.mH"+str(m)+".root"
        file_list.append(f)
        
masses.sort()
file_list.sort()

#print("----------------------------------------")
#print(masses)
#print("----------------------------------------")
#print(file_list)

i = 0
for m in masses:
    print("-------------------------------------")
    print(file_list[i])
    f = ROOT.TFile.Open(file_list[i])
    tree = f.Get("limit")
    tree.GetEntry(0); pvals.append(tree.limit)
    
    mass1.append(m)
    i += 1
    f.Close()


print("# ------------------------------ #")
print("# Expected limits for all masses #")
print("# ------------------------------ #")
print(mass1)
print("# ------------- Cat 0 ---------- #")
print(pvals)

print("# ---------------------- #")
print("# Filtered mass list  #")
print("# ---------------------- #")
targets = np.array([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])

def get_representative_values_with_limits(targets, mass_array, limit_array):
    representative_masses = []
    representative_limits = []
    
    for target in targets:
        # Get index of the closest mass value
        idx = np.argmin(np.abs(mass_array - target))
        
        # Get corresponding mass and limit
        closest_mass = mass_array[idx]
        corresponding_limit = limit_array[idx]
        
        # Append to lists
        representative_masses.append(closest_mass)
        representative_limits.append(corresponding_limit)
    
    return representative_masses, representative_limits

# Get the filtered masses and limits
# ----------------------------------
filtered_masses, filtered_pvals = get_representative_values_with_limits(targets, mass1, pvals)
print(filtered_masses)
print(filtered_pvals)

# Plotting
c1 = ROOT.TCanvas("c1", "c1", 1400, 1000)
c1.SetLogy()
c1.SetBottomMargin(0.16)

mg = ROOT.TMultiGraph()
graph_pvals = ROOT.TGraph(len(mass1), mass1, pvals)
graph_pvals.SetMarkerSize(0.5)
graph_pvals.SetMarkerStyle(20)
graph_pvals.SetMarkerColor(ROOT.kBlack)
graph_pvals.SetLineColor(ROOT.kCyan-3)
graph_pvals.SetLineWidth(3)
#graph_pvals.SetLineStyle(2)

mg.Add(graph_pvals, "lp")
#mg.Add(graph_pvals, "cp") # Spline
mg.SetMinimum(0.00000005)
mg.SetMaximum(100.0)
mg.Draw("APC")

# Customize axis
mg.GetYaxis().SetTitle("p-value")
#mg.GetYaxis().SetTitle("#sigma_{gg #rightarrow #phi} x BR(#phi #rightarrow #gamma#gamma) [pb]")
mg.GetYaxis().SetTitleOffset(1.01)
mg.GetYaxis().SetTitleSize(0.04)
mg.GetXaxis().SetTitle("m_{#phi} [GeV]")
mg.GetXaxis().SetTitleSize(0.045)
c1.Update()

# Adding labels for W1, W2, W3, W4 in the center of each range
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.03)
latex.SetTextAlign(22)

window_labels = [("W1", 10.2), ("W2", 28.), ("W3", 47 ), ("W4", 62.2)]
for label, pos in window_labels:
    latex.SetTextColor(ROOT.kGray)
    latex.DrawLatex(pos, mg.GetYaxis().GetXmin() * 2.8, label)

# Legend
# ------
leg = ROOT.TLegend(0.7, 0.26, 0.85, 0.4)
leg.SetTextSize(0.037)
leg.SetHeader("#bf{#it{Category 0}}", "L")  # "C" centers the title
leg.SetBorderSize(0)
leg.SetFillStyle(1001)
leg.AddEntry(graph_pvals, "p-value", "LPC")
#leg.Draw("same")

# Adding vertical lines for mass windows
lines_masses = [14.5, 40, 54.4]
line1 = ROOT.TLine(14.5, 0.00000015, 14.5, 1.0)
line1.SetLineColor(kGray)
line1.SetLineStyle(7)
line1.SetLineWidth(1)
line1.Draw("same")
line2 = ROOT.TLine(40, 0.00000015, 40, 1.0)
line2.SetLineColor(kGray)
line2.SetLineStyle(7)
line2.SetLineWidth(1)
line2.Draw("same")
line3 = ROOT.TLine(54.5, 0.00000015, 54.5, 1.0)
line3.SetLineColor(kGray)
line3.SetLineStyle(7)
line3.SetLineWidth(1)
line3.Draw("same")

sigma_levels = {
    "1": 0.3173,
    "2": 0.0455,
    "3": 0.0027,
    "4": 0.000063,
    "5": 3e-7
}

lines = []
for sigma, p_val in sigma_levels.items():
    line = ROOT.TLine(10, p_val, 70, p_val)
    line.SetLineColor(ROOT.kAzure)  # Choose color
    line.SetLineStyle(2)  # Dashed line style
    line.Draw()
    # Label each line with its sigma level
    text = ROOT.TLatex()
    text.SetTextSize(0.03)
    text.SetTextColor(ROOT.kAzure)
    nsigma = sigma + "#sigma"
    text.DrawLatex(70.5, p_val * 0.5, nsigma)  # Adjust position as needed
    lines.append(line)

# CMS lumi info
# -------------
CMS_lumi.writeExtraText = False
CMS_lumi.lumi_sqrtS = f"{lumi_project} fb^{{-1}} (13 TeV)"
CMS_lumi.CMS_lumi(c1, 0, 0)

latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.06)  
latex.SetTextAlign(13)   
#latex.DrawLatexNDC(0.265, 0.855, "#it{Preliminary}")  # Post approval


#c1.SaveAs(combine_plots + "allDataPVals_4Windows_syst_cat" + cat + ".pdf")
#c1.SaveAs(combine_plots + "allDataPVals_4Windows_syst_cat" + cat + ".png")
c1.SaveAs(combine_plots + "allDataPVals.pdf")
c1.SaveAs(combine_plots + "allDataPVals.png")
#c1.SaveAs(combine_plots + "allDataPVals_preliminary.pdf")
#c1.SaveAs(combine_plots + "allDataPVals_preliminary.png")
