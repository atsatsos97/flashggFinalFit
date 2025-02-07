import ROOT
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
#import mplhep as hep
import argparse
import sys
import os
from matplotlib.ticker import ScalarFormatter

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

def getEffSigma(_h):
  nbins, binw, xmin = _h.GetXaxis().GetNbins(), _h.GetXaxis().GetBinWidth(1), _h.GetXaxis().GetXmin()
  mu, rms, total = _h.GetMean(), _h.GetRMS(), _h.Integral()
  # Scan round window of mean: window RMS/binWidth (cannot be bigger than 0.1*number of bins)
  nWindow = int(rms/binw) if (rms/binw) < 0.1*nbins else int(0.1*nbins)
  # Determine minimum width of distribution which holds 0.693 of total
  rlim = 0.693*total
  wmin, iscanmin = 9999999, -999
  for iscan in range(-1*nWindow,nWindow+1):
    # Find bin idx in scan: iscan from mean
    i_centre = int((mu-xmin)/binw+1+iscan)
    x_centre = (i_centre-0.5)*binw+xmin # * 0.5 for bin centre
    x_up, x_down = x_centre, x_centre
    i_up, i_down = i_centre, i_centre
    # Define counter for yield in bins: stop when counter > rlim
    y = _h.GetBinContent(i_centre) # Central bin height
    r = y
    reachedLimit = False
    for j in range(1,nbins):
      if reachedLimit: continue
      # Up:
      if(i_up < nbins)&(not reachedLimit):
        i_up+=1
        x_up+=binw
        y = _h.GetBinContent(i_up) # Current bin height
        r+=y
        if r>rlim: reachedLimit = True
      else:
        print(" --> Reach nBins in effSigma calc: %s. Returning 0 for effSigma"%_h.GetName())
        return 0
      # Down:
      if( not reachedLimit ):
        if(i_down > 0):
          i_down-=1
          x_down-=binw
          y = _h.GetBinContent(i_down) #Current bin height
          r+=y
          if r>rlim: reachedLimit = True
        else:
          print(" --> Reach 0 in effSigma calc: %s. Returning 0 for effSigma"%_h.GetName())
          return 0
    # Calculate fractional width in bin takes above limt (assume linear)
    if y == 0.: dx = 0.
    else: dx = (r-rlim)*(binw/y)
    # Total width: half of peak
    w = (x_up-x_down+binw-dx)*0.5
    if w < wmin:
      wmin = w
      iscanmin = iscan
  # Return effSigma
  return wmin

def plot(mhs, vals, spline_name):
  #fig, ax = plt.subplots(figsize=(12, 8))
  #fig.patch.set_facecolor('white')
  plt.scatter(mhs, vals)
  plt.style.use('classic')
  plt.xlabel(r"$m_{\gamma\gamma}$ [GeV]", fontsize=18, x=0.9, y=1)
  plt.ylabel(spline_name, fontsize=14)
  plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))

  plt.plot([mhs[0], mhs[-1]], [vals[0], vals[-1]], color="royalblue", label='Category 0')

  #plt.style.use(hep.style.ROOT)
  #hep.cms.label("Preliminary", data=False)
  plt.title("13 TeV", fontsize=22, loc='right')
  plt.title(r"\textbf{CMS} \textit{Simulation Preliminary}", fontsize=22, loc='left', usetex=True)
  plt.legend(loc='lower right', frameon=False, fontsize=18) #loc='upper left','upper center'

  max_val_y = max(vals)
  min_val_y = min(vals)
  range_val_y = max_val_y - min_val_y
  new_max_y = max_val_y + 0.2 * range_val_y
  new_min_y = min_val_y - 0.2 * range_val_y
  plt.ylim(new_min_y, new_max_y)

  plt.savefig("/eos/user/a/atsatsos/www/SEP2024FinalFits/signal_cat0_effSigma.png")
  plt.savefig("/eos/user/a/atsatsos/www/SEP2024FinalFits/signal_cat0_effSigma.pdf")
  plt.clf()

mhs = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
eff_sigs = []
for mh in mhs:
    file = ROOT.TFile("/afs/cern.ch/work/e/elfontan/public/lowMassDiPhoton/sigModelPdfHistos/CAT0/pdfHistos_"+str(mh)+".root","READ")
    histo = file.Get("scaled_hist_mass_"+str(mh))
    sigmaeff = getEffSigma(histo)
    eff_sigs.append(sigmaeff)

print(mhs)
print(eff_sigs)

plot(mhs,eff_sigs,"Effective Sigma [GeV]")
