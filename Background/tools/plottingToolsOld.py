import ROOT
import json
from collections import OrderedDict as od
from commonObjects import *

def LoadTranslations(jsonfilename):
    with open(jsonfilename) as jsonfile:
        return json.load(jsonfile)
def Translate(name, ndict):
    return ndict[name] if name in ndict else name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Signal fit plots
# Plot final pdf at MH (with data) + individual Pdf components
def plotPdfMap(model,pdfs,plotBlindingRegion,_outdir='./',_cat='',_pdfNBins=1600,_dataNBins=80,setLogY=False):
  canv = ROOT.TCanvas()
  canv.SetLeftMargin(0.15)
  if setLogY: canv.SetLogy()
  hists = od()
  # Create pdf histograms
  pdfiter = 2
  for k,v in pdfs.iteritems():
    print pdfs.iteritems()
    kname = "_%s_%s"%(k[0],k[1])
    hists[k] = v['pdf'].createHistogram("h_pdf_%s"%kname,model.xvar,ROOT.RooFit.Binning(_pdfNBins))
    hists[k].SetLineWidth(2)
    hists[k].SetLineColor(pdfiter)
    hists[k].SetTitle("")
#    hists[k].Scale(0.05) # Makes PDF corresponding to 5% blinded data
    pdfiter += 1

  # Create data histogram
  hists['data'] = model.xvar.createHistogram("h_data",ROOT.RooFit.Binning(_dataNBins))
  model.DataHist.fillHistogram(hists['data'],ROOT.RooArgList(model.xvar))

  # Blinding region
  if model.blind:
    if plotBlindingRegion is not None:
      blindingRegion = plotBlindingRegion
    else:
      blindingRegion = model.blindingRegion
    for ibin in range(1,hists['data'].GetNbinsX()+1):
      xval = hists['data'].GetBinCenter(ibin)
      if( xval >= blindingRegion[0] )&( xval <= blindingRegion[1] ):
        hists['data'].SetBinContent(ibin,-1)
        hists['data'].SetBinError(ibin,0)
  hists['data'].SetTitle("")
  hists['data'].GetXaxis().SetTitle("m_{#gamma#gamma} [GeV]")
  hists['data'].SetMinimum(0)
  #hists['data'].Scale(float(model.nBins)/1600)
  hists['data'].SetMarkerStyle(20)
  hists['data'].SetMarkerColor(1)
  hists['data'].SetLineColor(1)
  hmax = hists['data'].GetMaximum()
  hmin = hists['data'].GetMinimum()

  # Draw histograms
  hists['data'].SetMaximum(1.2*hmax)
  if setLogY:
    hists['data'].SetMinimum(0.01)
  else:
    hists['data'].SetMinimum(0)
  hists['data'].Draw("PE")
  for k,v in pdfs.iteritems():
    # Scale pdf histograms
    hists[k].Scale(v['norm']*(float(_pdfNBins/_dataNBins)))
    hists[k].Draw("Same HIST")

  # Add legend
  #leg = ROOT.TLegend(0.58,0.6,0.86,0.85)
  leg = ROOT.TLegend(0.58,0.3,0.86,0.45)
  leg.SetFillStyle(0)
  leg.SetLineColor(0)
  leg.SetTextSize(0.03)
  leg.AddEntry(hists['data'],"Data","ep")
  for k in pdfs:
    ktitle = "(%s,%s)"%(k[0],k[1])
    leg.AddEntry(hists[k],ktitle,"L")
  leg.Draw("Same")

  # Add Latex
  lat = ROOT.TLatex()
  lat.SetTextFont(42)
  lat.SetTextAlign(31)
  lat.SetNDC()
  lat.SetTextSize(0.035)
  lat.DrawLatex(0.9,0.92,"3 fb^{-1} (13 TeV)") #Label is hard-coded
  lat1 = ROOT.TLatex()
  lat1.SetTextFont(42)
  lat1.SetTextAlign(11)
  lat1.SetNDC()
  lat1.SetTextSize(0.035)
  lat1.DrawLatex(0.15,0.92,"Category: %s"%_cat)

  canv.Update()
  if setLogY:
    canv.SaveAs("%s/bkgmodel_pdfs_%s_log.png"%(_outdir,_cat))
    canv.SaveAs("%s/bkgmodel_pdfs_%s_log.pdf"%(_outdir,_cat))
  else:
    canv.SaveAs("%s/bkgmodel_pdfs_%s.png"%(_outdir,_cat))
    canv.SaveAs("%s/bkgmodel_pdfs_%s.pdf"%(_outdir,_cat))
