#include <TString.h>

//write the datacard
void manual_fulltoydatacard10p_creation(){
  for (int mass=10; mass<71; mass++){
    TString mass_s;
    mass_s = Form("%iGeV_",mass);
    for(int cat=0; cat<1; cat++){
      TString cat_s;
      TString cat_n;
      cat_s = Form("cat%i",cat);
      cat_n = Form("_%i",cat);
      char inputShape[200];
      sprintf(inputShape,"datacards_fulltoy/fulltoy_"+mass_s+cat_s+".txt");
      ofstream newcardShape;
      newcardShape.open(inputShape);
      newcardShape << Form("imax * \n");
      newcardShape << Form("jmax * \n");
      newcardShape << Form("kmax * \n");
      newcardShape << Form("------------------------------------------      \n");
      newcardShape << Form("shapes     sig "+cat_s+" ../ws_sig/CMS-HGG_sigfit_LMAnalysis_May2024_newSignalNtuples_ggH_pNN_fourCat_0p8_0p6_0p5_2018_GG2H_2018_UntaggedTag"+cat_n+".root wsig_13TeV:hggpdfsmrel_GG2H_2018_UntaggedTag"+cat_n+"_13TeV\n");
      newcardShape << Form("shapes     bkg "+cat_s+" ../ws_10psliding/CMS-HGG_"+mass_s+"multipdf_UntaggedTag"+cat_n+".root multipdf:CMS_hgg_UntaggedTag"+cat_n+"_2018_13TeV_bkgshape\n");
      newcardShape << Form("shapes     data_obs "+cat_s+" ../ws_fulltoy/hggWorkspace_10percentData_7p5-72_fourCat_0p8_0p6_0p5_rooMultiPdf_"+cat_s+"_toy14232ev.root hgg_ws:toyData_Erf_"+cat_s+"\n");
      newcardShape << Form("bin                 "+cat_s+"\n");
      newcardShape << Form("observation         -1\n");
      newcardShape << Form("------------------------------------------      \n");
      newcardShape << Form("bin               "+cat_s+"      "+cat_s+"      \n");
      newcardShape << Form("process           sig            bkg            \n");
      newcardShape << Form("process           -1               1            \n");
      newcardShape << Form("rate              5440            1            \n");
      newcardShape << Form("------------------------------------------      \n");
      newcardShape << Form("pdfindex_UntaggedTag"+cat_n+"_2018_13TeV discrete      \n");
      newcardShape << Form("------------------------------------------      \n");
      newcardShape << Form("norm_"+cat_s+"     rateParam       "+cat_s+"       bkg     10000    [0.001,10000000000]            \n");
      newcardShape << Form("lumi                lnN             1.03    -    \n");
      newcardShape.close();
    }
  }
}