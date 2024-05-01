#include <iostream>
#include <TLegend.h>
#include <sstream>
#include <string>
#include <cstring>
#include <fstream>
#include <cstdlib>
#include "TH1D.h"
#include "TH2D.h"
#include <THStack.h>
#include "TProfile.h"
#include "TGraph.h"
#include "TFile.h"
#include "TTree.h"
#include "TF1.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TFractionFitter.h"
#include <string>
#include <vector>
#include <math.h>
#include <TLatex.h>
#include <TLine.h>
#include <TMarker.h>
#include <TPave.h>
#include <TPaveStats.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <TString.h>
#include <TGraphErrors.h>
#include <TGraphAsymmErrors.h>
#include "TF1.h"
#include "TEfficiency.h"

#include <vector>
#include <map>
#include <utility>
#include <algorithm>
#include <iostream>
#include <string>
#include <sstream>
#include <iostream>
#include <valarray>

#include <RooAbsPdf.h>
#include <RooPlot.h>
#include <RooArgSet.h>
#include <RooArgList.h>
#include <RooDataSet.h>
#include <RooDataHist.h>
#include <RooGaussian.h>
#include <RooPolynomial.h>
#include <RooBernstein.h>
#include <RooRealVar.h>
#include <RooFormulaVar.h>
#include <RooWorkspace.h>
#include <RooMsgService.h>
#include <RooAddPdf.h>
#include <TROOT.h>
#include "../../HiggsAnalysis/CombinedLimit/interface/RooDoubleCBFast.h"
//#include "pdfs.h"

//#include <RooDoubleCBFast.h>

using namespace std;

void makeCardsAndWS(TString year="2018"){
	for(int mass=10; mass<75; mass+=5){
  //WHICH YEAR
		TString suff="MGGHistos";
		TString mass_s;
		mass_s = Form("%i_",mass);
  //INPUT FILE WITH HISTOGRAMS TO FIT BACKGROUND
	  	TFile* file = NULL;
	        //file=TFile::Open("/eos/user/a/atsatsos/L1HLTRates/CMSSW_12_4_0/src/FlashGGPython3/NewVersion/histogramtest_data_"+mass_s+"cat0.root");
	        file=TFile::Open("/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_12_4_8/src/MassPlots_NN0.78/histogramtest_data_"+mass_s+"cat0.root");
  //INPUT FILE WITH HISTOGRAMS TO FIT SIGNAL
	        TFile* sig_file = NULL;
	        //sig_file=TFile::Open("/eos/user/a/atsatsos/L1HLTRates/CMSSW_12_4_0/src/FlashGGPython3/NewVersion/histogramtest_sig_"+mass_s+"cat0.root");
	        sig_file=TFile::Open("/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_12_4_8/src/MassPlots_NN0.78/histogramtest_sig_"+mass_s+"cat0.root");
  //PREPARE EXPECTED NUMBER OF SIGNAL EVENTS PER CATEGORY
		//X-SECTION GRAPH
		//double m[1]		= {10.0};
		//double xSec[1]	= {1.0};
		//TGraph* xsecgraph	= new TGraph(1,m,xSec);

		//scale
		double eps2scale = 1;//0.01;//1;//0.1;//0.002; //this scales eps 0.02 ->
		double unfittable_regions[0][0] = {};

   //LOOP OVER MASS INDICES AND MAKE THE CARDS/WORKSPACES
		double rel_reso=0.013;//temporary

		for(int i=0; i<1; i++){

		  	//get the histograms
	  		TH1D* catA=(TH1D*)file->Get("data_M"+mass_s+"cat0");
                	TH1D* cat_sig=(TH1D*)sig_file->Get("ggh_M"+mass_s+"cat0");

	  		double massLow  =  catA->GetXaxis()->GetXmin();
			double massHigh =  catA->GetXaxis()->GetXmax();
			double massBinWidth = massHigh-massLow;

			//compute mass point and define ROOFit variables
	  		bool dontfit=false;

			double mass_d = double(mass);

			RooRealVar CMS_Hgg_mass("CMS_Hgg_mass", "CMS_Hgg_mass", massLow, massHigh);

			//Triple Gauss variables
			/*RooRealVar mean1("mean1", "mean1", 0.95*mass, massLow, massHigh);
                	RooRealVar sigma1("sigma1", "sigma1", 0.3, 0.001, 1);
			RooRealVar mean2("mean2", "mean2", mass, massLow, massHigh);
                	RooRealVar sigma2("sigma2", "sigma2", 0.3, 0.001, 1);
			RooRealVar mean3("mean3", "mean3", 1.05*mass, massLow, massHigh);
                	RooRealVar sigma3("sigma3", "sigma3", 1, 0.001, 3);*/

			RooRealVar frac1("frac1", "frac1", 0.45, 0, 1);
                	RooRealVar frac2("frac2", "frac2", 0.45, 0, 1);

			//DCB Variables
			RooRealVar mean_dcb("mean_dcb", "mean_dcb", mass, massLow, massHigh);
			RooRealVar sigma_dcb("sigma_dcb", "sigma_dcb", 0.4, 0.01, 4.);
			RooRealVar a1("a1", "a1", 0.5, 0.1, 5.);
			RooRealVar n1("n1", "n1", 10.0, 0.1, 20.);
			RooRealVar a2("a2", "a2", 0.3, 0.1, 5.);
			RooRealVar n2("n2", "n2", 10.0, 0.1, 25.);
			RooRealVar frac("frac", "frac", 0.2, 0., 1.);
			RooRealVar sigma_gaus("sigma_gaus", "sigma_gaus", 0.3, 0.05, 1.5);

			//define the signal model
			//in pdf.h aggiungi una pdf generica e salvala nel workspace con tutti i param già fissati. poi riprendila da qui, e usa dirett
			//la sua variabile massa osservabile come massa qui, semplicemente cambiandogli il range.

			RooDataHist data_obs("data_obs", "", RooArgList(CMS_Hgg_mass), catA);
			RooRealVar bkg_norm("bkg_norm", "",catA->Integral());

			RooDataHist data_sig("data_sig", "", RooArgList(CMS_Hgg_mass), cat_sig);
			RooRealVar sig_norm("sig_norm", "",cat_sig->Integral());

			RooRealVar par1("par1", "par1", 0.2, 0, 10);
			RooRealVar par2("par2", "par2", 1.5, 0, 10);
			RooArgList alist(par1, par2);
			RooBernstein bkg_model("bkg_model", "bkg_model", CMS_Hgg_mass, alist);

			/*RooRealVar par1("par1", "par1", 0.2, 0, 10);
			RooRealVar par2("par2", "par2", 1.5, 0, 10);
			RooRealVar par3("par3", "par3", 2.0, 0, 10);
			//RooRealVar par4("par4", "par4", 2.0, 0, 10);
			RooArgList alist(par1, par2, par3);
			RooBernstein bkg_model("bkg_model", "bkg_model", CMS_Hgg_mass, alist);*/

			//Triple Gauss modelling
			/*RooGaussian gauss1("gauss1", "gauss1", CMS_Hgg_mass, mean1, sigma1);
                	RooGaussian gauss2("gauss2", "gauss2", CMS_Hgg_mass, mean2, sigma2);
                	RooGaussian gauss3("gauss3", "gauss3", CMS_Hgg_mass, mean3, sigma3);
			RooAddPdf sig_model("sig_model", "sig_model", RooArgList(gauss1,gauss2,gauss3), RooArgList(frac1,frac2));*/

			//DCB+Gauss modelling
			RooDoubleCBFast doubleCB("doubleCB", "doubleCB", CMS_Hgg_mass, mean_dcb, sigma_dcb, a1, n1, a2, n2);
			RooGaussian gauss("gauss", "gauss", CMS_Hgg_mass, mean_dcb, sigma_gaus);
			RooAddPdf sig_model("sig_model", "sig_model", RooArgList(doubleCB, gauss), RooArgList(frac), true);

			bkg_model.fitTo(data_obs);

			RooPlot *frame = CMS_Hgg_mass.frame();
			data_obs.plotOn(frame);
			bkg_model.plotOn(frame);
			TCanvas c_all("c_all", "c_all", 800, 500);
			frame->Draw("goff");
			frame->SetXTitle("CMS ALP Mass [GeV]");
			frame->SetYTitle("Events");
			frame->SetTitle("Background Fit");
			c_all.SaveAs(Form("output/NN0.78DCB/catA_%d_"+year+"_sig1bkg3_M"+mass_s+"cat0.png",i));

                	sig_model.fitTo(data_sig);

			//Triple Gauss constants
			/*mean1.setConstant(kTRUE);
			mean2.setConstant(kTRUE);
			mean3.setConstant(kTRUE);
			sigma1.setConstant(kTRUE);
			sigma2.setConstant(kTRUE);
			sigma3.setConstant(kTRUE);
			frac1.setConstant(kTRUE);
			frac2.setConstant(kTRUE);*/

			//DCB constants
                        mean_dcb.setConstant(kTRUE);
                        sigma_dcb.setConstant(kTRUE);
                        a1.setConstant(kTRUE);
                        n1.setConstant(kTRUE);
                        a2.setConstant(kTRUE);
                        n2.setConstant(kTRUE);
                        frac.setConstant(kTRUE);
                        sigma_gaus.setConstant(kTRUE);

                	RooPlot *sig_frame = CMS_Hgg_mass.frame();
                	data_sig.plotOn(sig_frame);
                	sig_model.plotOn(sig_frame);
                	TCanvas c_sig("c_sig", "c_sig", 800, 500);
                	sig_frame->Draw("goff");
			sig_frame->SetXTitle("CMS ALP Mass [GeV]");
			sig_frame->SetYTitle("Events");
			sig_frame->SetTitle("Signal Fit");
                	c_sig.SaveAs(Form("output/NN0.78DCB/cat_sig_%d_"+year+"_sig1bkg3_M"+mass_s+"cat0.png",i));

			//save into ROO workspace
			RooWorkspace dpworkspace("dpworkspace", "");
			dpworkspace.import(data_obs);
			//dpworkspace.import(data_sig);
			dpworkspace.import(sig_model);
			dpworkspace.import(bkg_model);
			dpworkspace.writeToFile(Form("output/NN0.78DCB/dpWorkspace"+year+suff+"_%d_sig1bkg3_M"+mass_s+"cat0.root",i));

			//write the datacard
			char inputShape[200];
			sprintf(inputShape,"output/NN0.78DCB/dpCard_"+year+suff+"_%d_sig1bkg3_"+mass_s+"cat0.txt",i);
			ofstream newcardShape;
			newcardShape.open(inputShape);
			newcardShape << Form("imax * number of channels\n");
			newcardShape << Form("jmax * number of background\n");
			newcardShape << Form("kmax * number of nuisance parameters\n");
			newcardShape << Form("shapes data_obs	CatAB dpWorkspace"+year+suff+"_%d_sig1bkg3_M"+mass_s+"cat0.root dpworkspace:data_obs\n",i);
			newcardShape << Form("shapes bkg_mass	CatAB dpWorkspace"+year+suff+"_%d_sig1bkg3_M"+mass_s+"cat0.root dpworkspace:bkg_model\n",i);
			newcardShape << Form("shapes signalModel_generic	CatAB dpWorkspace"+year+suff+"_%d_sig1bkg3_M"+mass_s+"cat0.root dpworkspace:sig_model\n",i);
			newcardShape << Form("bin		CatAB\n");
			newcardShape << Form("observation 	-1.0\n");
			newcardShape << Form("bin     		CatAB		CatAB		\n");
			newcardShape << Form("process 		signalModel_generic  	bkg_mass	\n");
			newcardShape << Form("process 		0    		1	   	\n");
			newcardShape << Form("rate    		%f  		%f		\n",
					     cat_sig->Integral(), catA->Integral());
			//newcardShape << Form("lumi13TeV_2017 lnN 	1.023 	-\n");
			//newcardShape << Form("eff_mu_13TeV_2017 lnN	1.015 	-\n");
			//newcardShape << Form("bkg_norm rateParam CatA bkg_mass %f\n",catA->Integral());
			//newcardShape << Form("resA param %f %f\n",resA.getValV(),resA.getValV()*0.1);
			newcardShape.close();
		}
	}
}
