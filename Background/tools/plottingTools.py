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
# Plot final pdf at MH = 125 (with data) + individual Pdf components
def plotPdfMap(model,pdfs,plotBlindingRegion,_outdir='./',_cat='',_pdfNBins=1600,_dataNBins=80,_massh='10GeV',setLogY=False):
  canv = ROOT.TCanvas()
  canv.SetLeftMargin(0.15)
  if setLogY: canv.SetLogy()
  hists = od()
  # Create pdf histograms
  pdfiter = 2
  for k,v in pdfs.iteritems():
    kname = "_%s_%s"%(k[0],k[1])
    hists[k] = v['pdf'].createHistogram("h_pdf_%s"%kname,model.xvar,ROOT.RooFit.Binning(_pdfNBins))
    hists[k].SetLineWidth(2)
    hists[k].SetLineColor(pdfiter)
    hists[k].SetTitle("")
    pdfiter += 1

  # Create data histogram
  if _dataNBins == None:
    _dataNBins = model.xvar.getBins()

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
  hists['data'].GetYaxis().SetTitle("Events / (%.2f GeV)"%((model.xvar.getMax()-model.xvar.getMin())/_dataNBins))
  hists['data'].SetMinimum(0)
  #hists['data'].Scale(float(model.nBins)/1600)
  hists['data'].SetMarkerStyle(20)
  hists['data'].SetMarkerColor(1)
  hists['data'].SetLineColor(1)
  hmax = hists['data'].GetMaximum()
  hmin = hists['data'].GetMinimum()

  # Draw histograms and save them
  hists['data'].SetMaximum(1.5*hmax)
  #hists['data'].SetMaximum(max(25.0,1.5*hmax))
  if setLogY:
    min_vals = []
    for k,v in pdfs.iteritems():
      min_vals.append(hists[k].GetMinimum())
    hists['data'].SetMinimum(max(min_vals))
  else:
    hists['data'].SetMinimum(0)
  hists['data'].Draw("PE")
  hists['data'].SaveAs("%s/data_%s_%s.root"%(_outdir,_cat,_massh))
  for k,v in pdfs.iteritems():
    # Scale pdf histograms
    hists[k].Scale(v['norm']*(float(_pdfNBins)/_dataNBins))
    hists[k].Draw("Same HIST ][")
    hists[k].SaveAs("%s/pdfs_%s_%s_%s%s.root"%(_outdir,_cat,_massh,k[0],k[1]))

  # Add legend
  height_per_pdf = 0.12/4
  #leg = ROOT.TLegend(0.53,0.33-height_per_pdf*(len(pdfs)+1),0.85,0.33)
  #leg = ROOT.TLegend(0.53,0.30-height_per_pdf*(len(pdfs)+1),0.85,0.30)
  leg = ROOT.TLegend(0.53,0.85-height_per_pdf*(len(pdfs)+1),0.85,0.85)
  leg.SetFillStyle(0)
  leg.SetLineColor(0)
  leg.SetTextSize(0.035)
  leg.AddEntry(hists['data'],"Data","ep")
  for k,v in pdfs.iteritems():
    gof = round(ROOT.TMath.Prob(v['NLL']*2.0,v['Ndof']),3)
    ktitle = "(%s,%s) GOF = %s"%(k[0],k[1],gof)
    leg.AddEntry(hists[k],ktitle,"L")
  leg.Draw("Same")

  # Add Latex
  lat = ROOT.TLatex()
  lat.SetTextFont(42)
  lat.SetTextAlign(31)
  lat.SetNDC()
  lat.SetTextSize(0.035)
  #lat.DrawLatex(0.9,0.92,"5.44 fb^{-1} (13 TeV)")
  lat.DrawLatex(0.9,0.92,"54.4 fb^{-1} (13 TeV)")
  lat1 = ROOT.TLatex()
  lat1.SetTextFont(61)
  lat1.SetTextAlign(11)
  lat1.SetNDC()
  lat1.SetTextSize(0.045)
#  lat1.DrawLatex(0.15,0.92,"Category: %s"%_cat)
  lat1.DrawLatex(0.20,0.84,"CMS")
  lat2 = ROOT.TLatex()
  lat2.SetTextFont(52)
  lat2.SetTextAlign(11)
  lat2.SetNDC()
  lat2.SetTextSize(0.035)
  lat2.DrawLatex(0.22,0.80,"Preliminary")

  canv.Update()
  if setLogY:
    canv.SaveAs("%s/bkgmodel_pdfs_%s_%s_log.png"%(_outdir,_cat,_massh))
    canv.SaveAs("%s/bkgmodel_pdfs_%s_%s_log.pdf"%(_outdir,_cat,_massh))
  else:
    canv.SaveAs("%s/bkgmodel_pdfs_%s_%s.png"%(_outdir,_cat,_massh))
    canv.SaveAs("%s/bkgmodel_pdfs_%s_%s.pdf"%(_outdir,_cat,_massh))
