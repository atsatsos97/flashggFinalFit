# Plotting

Apologies for the lack of documentation for all the different plotting scripts!

## Final signal+background fit for very low mass analysis

   0) Make a directory where to work:

   ```
   mkdir SplusBModels_AllData_cat0
   ```

   ---------------------------------

   1) Fit the workspace in the datacard

   ```
   cd SplusBModels_AllData_cat0
   cp ../../../Combine/cards/AllData/sliding_50.0GeV_cat0.txt .
   text2workspace.py sliding_50.0GeV_cat0.txt sliding_50.0GeV_cat0.root
   combine sliding_50.0GeV_cat0.root -m 50.000 -M MultiDimFit -P r --floatOtherPOIs=1 --freezeParameters MH --saveWorkspace  -n _initialSnapshot --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2
   ```

   ------------------------------------------------------

   2) Throw toys starting from the snapshot of previous step

   ```
   cd ..
   python makeToys.py --inputWSFile SplusBModels_AllData_cat0/higgsCombine_initialSnapshot.MultiDimFit.mH50.root --loadSnapshot MultiDimFit --ext _AllData_cat0 --nToys 500 --dryRun --batch condor
   cd SplusBModels_AllData_cat0/toys/jobs/
   condor_submit sub_toys.sub
   ```

   --------------

   3) Plotting step: 

   ```
   python makeSplusBModelPlot.py --inputWSFile SplusBModels_AllData_cat0/higgsCombine_initialSnapshot.MultiDimFit.mH50.root --loadSnapshot MultiDimFit --cats all --ext _AllData_cat0 --mass 50  --unblind  --doBkgRenormalization --nBins 60 --doZeroes --doBands
   ```
   --------------

# Commands for making plotting figures:

Note that connection to the slc7 Singularity container and the flashggFinalFit environment need to be set up before running these commands!

## Full Range Plot

   ```
   python makeSplusBPlotFullRange.py
   ```
   --------------

## Plots for certain mass points in each window (after toys are created for each one)

   ```
   python makeSplusBModelPlot.py --inputWSFile SplusBModels_AllData_cat0/higgsCombine_initialSnapshot.MultiDimFit.mH13.6.root --loadSnapshot MultiDimFit --cats all --ext _AllData_cat0 --mass 13.6 --unblind --doBkgRenormalization --nBins 70 --pdfNBins 2800 --doZeroes --doBands

   python makeSplusBModelPlot.py --inputWSFile SplusBModels_AllData_cat0/higgsCombine_initialSnapshot.MultiDimFit.mH12.root --loadSnapshot MultiDimFit --cats all --ext _AllData_cat0 --mass 12 --unblind --doBkgRenormalization --nBins 70 --pdfNBins 2800 --doZeroes --doBands
   python makeSplusBModelPlot.py --inputWSFile SplusBModels_AllData_cat0/higgsCombine_initialSnapshot.MultiDimFit.mH35.root --loadSnapshot MultiDimFit --cats all --ext _AllData_cat0 --mass 35 --unblind --doBkgRenormalization --nBins 155 --pdfNBins 6200 --doZeroes --doBands
   python makeSplusBModelPlot.py --inputWSFile SplusBModels_AllData_cat0/higgsCombine_initialSnapshot.MultiDimFit.mH46.root --loadSnapshot MultiDimFit --cats all --ext _AllData_cat0 --mass 46 --unblind --doBkgRenormalization --nBins 60 --pdfNBins 2400 --doZeroes --doBands
   python makeSplusBModelPlot.py --inputWSFile SplusBModels_AllData_cat0/higgsCombine_initialSnapshot.MultiDimFit.mH64.5.root --loadSnapshot MultiDimFit --cats all --ext _AllData_cat0 --mass 64.5 --unblind --doBkgRenormalization --nBins 56 --pdfNBins 2240 --doZeroes --doBands
   ```
   --------------
