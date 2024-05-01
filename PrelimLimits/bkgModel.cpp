// ----------------------------------------------------------- //
// Macro for the bkg modelling of the low mass diphoton search //
// ----------------------------------------------------------- //

#include "RooRealVar.h"
#include "RooDataSet.h"
#include <RooDataHist.h>
#include "RooGaussian.h"
#include "RooConstVar.h"
#include "RooAddPdf.h"
#include <RooBernstein.h>
#include "RooChebychev.h"
#include "RooFitResult.h"
#include "RooGenericPdf.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TText.h"
#include "TAttLine.h"
#include "TLegend.h"
#include "RooPlot.h"
#include "TFile.h"
#include "TStyle.h"
#include "TH2.h"
#include "TMatrixDSym.h"
#include <RooChi2Var.h>
#include <cstdio>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;
using namespace RooFit;

void bkgModel(TString year="2018"){
	//INPUT FILE WITH HISTOGRAMS TO FIT BACKGROUND COMPONENTS
        TFile* bkg_file = NULL; 
        bkg_file=TFile::Open("/afs/cern.ch/work/e/elfontan/public/lowMassDiPhoton/histos_mass_cat_pNN0p907_HggLM.root");    
	cout << "Background file: " << bkg_file->GetName() << endl;
	cout << "----------------------------------------" << endl;

	// Get the histograms
	// ------------------
	//h_diphoMass_data_c0, h_diphoMass_sb_c0, h_diphoMass_ggmc_c0, h_diphoMass_data_c1, h_diphoMass_sb_c1, h_diphoMass_ggmc_c1 
				      
	TH1D* cat_bkg=(TH1D*)bkg_file->Get("h_diphoMass_ggmc_c1");
	double massLow  =  cat_bkg->GetXaxis()->GetXmin();
	double massHigh =  cat_bkg->GetXaxis()->GetXmax();
	double n_bins = cat_bkg->GetSize()-2;
	//double fit_min = cat_bkg->GetXaxis()->GetXmin();
	//double fit_max = cat_bkg->GetXaxis()->GetXmax();
	double fit_min = 10.;
	double fit_max = 65.;
	//double fit_min = cat_bkg->GetMean()-3*cat_bkg->GetRMS();
	//double fit_max = cat_bkg->GetMean()+3*cat_bkg->GetRMS();
	int fit_nbins = int((fit_max - fit_min)/((massHigh - massLow)/n_bins)); 
	
	// Compute mass point and define ROOFit variables
	RooRealVar CMS_hgg_mass("CMS_hgg_mass", "CMS_hgg_mass", fit_min, fit_max);
	
	// -----------------------
	// Define the bkg model
	// -----------------------
	RooDataHist data_bkg("data_bkg", "data_bkg", RooArgList(CMS_hgg_mass), cat_bkg);        
	RooRealVar bkg_norm("bkg_norm", "bkg_norm",cat_bkg->Integral());
	cout << "RooDataHist Integral: " << cat_bkg->Integral() << endl;

	RooArgList alist;
	RooRealVar p0("p0", "Param 0", 0.1, 0.0, 1.0);
	RooRealVar p1("p1", "Param 1", 1.2, 1.0, 5.0);
	RooRealVar p2("p2", "Param 2", 1., 0.01, 10.0);
	RooRealVar p3("p3", "Param 3", 1., 0.0, 10.0);
	RooRealVar p4("p4", "Param 4", 1., 0.0, 10.0);
	//RooRealVar p0("p0", "Param 0", 0.9);
	//RooRealVar p1("p1", "Param 1", 1.2);
	//RooRealVar p2("p2", "Param 2", 5.5);
	//RooRealVar p3("p3", "Param 3", 0.4);
	//RooRealVar p4("p4", "Param 4", 2.1);
	alist.add(CMS_hgg_mass);
	alist.add(p0);
	alist.add(p1);
	alist.add(p2);
	alist.add(p3);
	alist.add(p4);
	for (int i = 0; i < alist.getSize(); ++i) {
	  RooAbsArg* arg = alist.at(i);
	  std::cout << "Argument " << i << ": " << arg->GetName() << std::endl;
	}

	//RooGenericPdf bkg_pol("bkg_pol", "Background model for the diphoton background", "p0 + p1 * CMS_hgg_mass + p2 * CMS_hgg_mass * CMS_hgg_mass", RooArgSet(alist));
	RooGenericPdf bkg_pol("bkg_pol", "Background model for the diphoton background", "p0 + p1 * CMS_hgg_mass + p2 * CMS_hgg_mass * CMS_hgg_mass + p3 * CMS_hgg_mass * CMS_hgg_mass * CMS_hgg_mass + p4 *CMS_hgg_mass * CMS_hgg_mass* CMS_hgg_mass * CMS_hgg_mass", RooArgSet(alist));
	///RooGenericPdf bkg_pol("bkg_pol", "Background model for the diphoton background", "p0*pow(CMS_hgg_mass, p1)*(1+p2*pow(CMS_hgg_mass, p3))", RooArgSet(alist));
	//RooFitResult* result = bkg_pol.fitTo(data_bkg, Range(fit_min, fit_max), Save());

	// Construct the error function and a coefficient for the error function in the combined bkg model
	// -----------------------------------------------------------------------------------------------
	RooRealVar err_mean("err_mean", "Error function mean", 50, 40.0, 70.0); // Best for now: 60, 50.0, 70.0 
	RooRealVar err_sigma("err_sigma", "Error function sigma", 2., 0.0, 10.0); // Best for now: 1., 0.0, 3.0
	RooGenericPdf err_function("err_function", "Error function", "0.5 * (1 + TMath::Erf((CMS_hgg_mass - err_mean) / (sqrt(2) * err_sigma)))", RooArgSet(CMS_hgg_mass, err_mean, err_sigma));
	RooRealVar err_coeff("err_coeff", "Error function coefficient", 0.7, 0.0, 1.0); // Best for now: 0.5, 0.0, 1.0

	//RooGaussian bkg_model("bkg_model", "bkg_model", CMS_hgg_mass, mean, sigma);
	//RooGaussian gauss1("gauss1", "gauss1", CMS_hgg_mass, mean1, sigma1);
	//RooGaussian gauss2("gauss2", "gauss2", CMS_hgg_mass, mean2, sigma2);
	//RooGaussian gauss3("gauss3", "gauss3", CMS_hgg_mass, mean3, sigma3);
	//RooAddPdf sig_model("sig_model", "sig_model", RooArgList(gauss1,gauss2,gauss3), RooArgList(frac1,frac2), true); 	

	// Chebyshev polynomial function
	RooRealVar c0("c0", "c0", 0.8, -1, 1);
	RooRealVar c1("c1", "c1", 0.5, -1, 1);
	RooChebychev chebychev("chebychev", "Chebychev PDF", CMS_hgg_mass, RooArgList(c0, c1));
	RooRealVar frac("frac", "Fraction", 0.1, 0.0, 1.0);
	
	// Construct the combined model
	// ----------------------------
	RooAddPdf bkg_model("bkg_model", "Background model", RooArgList(bkg_pol, err_function), RooArgList(err_coeff));
	//RooAddPdf bkg_model("bkg_model", "Background model", RooArgList(bkg_pol, chebychev), RooArgList(frac));
	
	//-------------------------
	// Fitting: combined model
	//-------------------------
	//bkg_model.fitTo(data_bkg);
	RooFitResult* result = bkg_model.fitTo(data_bkg, Range(fit_min, fit_max), Save()); 


	cout << "#########################" << endl;
	cout << "##### PRINT RESULTS #####" << endl;
	cout << "#########################" << endl;
	if (result) {
	  result->Print("v");
	  TH2 *hcorr = result->correlationHist();
	  TFile *bkg_out = new TFile("testing_bkgModelling/bkg_cat0.root", "RECREATE");
	  result->Write();
	  hcorr->Write();
	  bkg_out->Close();
	} else {
	  cout << "Fit failed! Unable to print results." << endl;
	}
	
	TH2* hcorr = result->correlationHist();
	TFile* bkg_out = new TFile("testing_bkgModelling/bkg_cat0.root", "RECREATE");
	result->Write();
	hcorr->Write();
	bkg_out->Close();
	
	// Each RooRealVar is set to be a constant after the result of the fit
	p0.setConstant(kTRUE);
	p1.setConstant(kTRUE);
	p2.setConstant(kTRUE);
	//p3.setConstant(kTRUE);
	//p4.setConstant(kTRUE);
       
	//-------------------------
	// RooPlot
	//-------------------------	
	RooPlot *bkg_frame = CMS_hgg_mass.frame();                                             

	std::cout << "################" << std::endl;
	std::cout << "##### CHI2 #####" << std::endl;
	std::cout << "################" << std::endl;
	
	bkg_frame->SetTitle("");
	bkg_frame->GetXaxis()->SetTitle("Mass [GeV]");
	bkg_frame->GetYaxis()->SetTitle("Events/0.1");
	data_bkg.plotOn(bkg_frame);                                  
	//bkg_model->plotOn(bkg_frame, RooFit::Name("BkgModel"), LineColor(kRed));
	bkg_model.plotOn(bkg_frame, RooFit::Name("BkgModel"), LineColor(kRed));

	cout << "-----------------------------" << endl;
	cout << "# TH1D Histo bins: " << n_bins << endl;
	cout << "# NBins data_bkg = " << (data_bkg.numEntries() -2) << endl;
	// Print number of floating parameters in the PDF
	//cout << "# Number of floating parameters: " << result->floatParsFinal().getSize() << endl;
	double chi2_over_ndof = bkg_frame->chiSquare(result->floatParsFinal().getSize()); //tell the chiSquare method how many free parameters you have
	cout << "Chi2/ndof = " << chi2_over_ndof << endl;
	cout << "-----------------------------" << endl;

	//-------------------------
	// Plotting
	//-------------------------	
	TCanvas c_bkg("c_bkg", "c_bkg", 1200, 1000);                
	bkg_frame->Draw("");

	//TLegend *leg = new TLegend(0.88,0.88,0.6,0.76); //top right
	TLegend *leg = new TLegend(0.2,0.88,0.6,0.76); //top left
	leg->SetHeader(Form("#chi^{2}/N_{dof} = %.4f", chi2_over_ndof));
	//leg->SetHeader(Form("#chi^{2} = %.2f", chi2_bkg_model.getVal()));
	leg->SetLineColor(kWhite);
	leg->SetFillColor(0);
	leg->SetTextFont(42);
	leg->SetTextSize(0.03);
	leg->AddEntry(bkg_frame->findObject("BkgModel"),"Background Model","l");
	leg->Draw();
	//TLegendEntry *header = (TLegendEntry*)leg->GetListOfPrimitives()->First();
	//header->SetTextSize(.03);

	// Add text to frame
	/*
	TLatex *latex = new TLatex(); // prepare text in LaTeX format
	latex->SetTextSize(0.035);
	latex->SetNDC();
	latex->DrawLatex(0.6, 0.9, Form("#frac{#chi^{2}}{N_{dof}} = %.2f", chi2_bkg_model.getVal())); 
	bkg_frame->addObject(latex);
	*/
	c_bkg.SaveAs("/eos/user/e/elfontan/www/LowMassDiPhoton/testing_BkgModelling/bkg_tests_pol4_plusErrFunction_largeFrac_m1065.png");
	//c_bkg.SaveAs("testing_bkgModelling/bkg_tests.png");

	/*
	//-------------------------
	// Save into ROO workspace
	//-------------------------
	RooWorkspace dpworkspace("dpworkspace", "");
	dpworkspace.import(bkg_model);
	dpworkspace.writeToFile("output/dpWorkspace.root");
	*/
}
	// ------- Custom function for the background modelling			
	// Define the parameters for the custom function
	/*
	RooArgList alist;
	RooRealVar p0("p0", "Param 0", 87);
	RooRealVar p1("p1", "Param 1", 0.6);
	RooRealVar p2("p2", "Param 2", 2.9);
	RooRealVar p3("p3", "Param 3", 6.1);
	RooRealVar p4("p4", "Param 4", -259.0);
	RooRealVar p5("p5", "Param 5", 122.0);
	RooRealVar p6("p6", "Param 6", 2.62);
	RooRealVar p7("p7", "Param 7", -0.02);
	RooRealVar p8("p8", "Param 8", -2.5);
	RooRealVar p9("p9", "Param 9", 0.66);
	RooRealVar p10("p10", "Param 10", 0.0027);
	RooRealVar p11("p11", "Param 11", -3.5);
	RooRealVar p12("p12", "Param 12", 6.16);
	alist.add(CMS_hgg_mass);
	alist.add(p0);
	alist.add(p1);
	alist.add(p2);
	alist.add(p3);
	alist.add(p4);
	alist.add(p5);
	alist.add(p6);
	alist.add(p7);
	alist.add(p8);
	alist.add(p9);
	alist.add(p10);
	alist.add(p11);
	alist.add(p12);
	// Create a RooAbsPdf that uses the RooFormulaVar as custom PDF
	RooGenericPdf* bkg_model = new RooGenericPdf("bkg_model", "Background model for the diphoton background", "p0*pow(CMS_hgg_mass, p1)*(1+p2*pow(CMS_hgg_mass, p3))^p4*(1+p5*pow(CMS_hgg_mass, p6))*(1+p7*pow(CMS_hgg_mass, p8))^p9*(1+p10*pow(CMS_hgg_mass, p11))^p12", RooArgSet(alist));
	//RooGenericPdf* bkg_model = new RooGenericPdf("bkg_model", "Background model for the diphoton background", "[0]*pow(CMS_hgg_mass, [1])*(1+[2]*pow(CMS_hgg_mass, [3]))^[4]*(1+[5]*pow(CMS_hgg_mass, [6]))*(1+[7]*pow(CMS_hgg_mass, [8]))^[9]*(1+[10]*pow(CMS_hgg_mass, [11]))^[12]", RooArgSet(alist));
	*/
	
	/* NOTE: David's implementation based on: 
	feta = "[0]*x^[1]*(1+[2]*x^[3])^[4]*(1+[5]*x^[6])*(1+[7]*x^[8])^[9]*(1+[10]*x^[11])^[12]")
	f1 = TF1("f1",feta,2.0*0.1057,0.55))
	f1.SetParameter(0,87)
	f1.SetParameter(1,0.6)
	f1.SetParameter(2,2.9)
	f1.SetParameter(3,6.1)
	f1.SetParameter(4,-259.)
	f1.SetParameter(5,122.0)
	f1.SetParameter(6,2.62)
	f1.SetParameter(7,-0.02)
	f1.SetParameter(8,-2.5)
	f1.SetParameter(9,0.66)
	f1.SetParameter(10,0.0027)
	f1.SetParameter(11,-3.5)
	f1.SetParameter(12,6.16)
	*/		
