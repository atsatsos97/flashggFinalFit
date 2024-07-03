import os

mass_points = [10,15,20,25,30,35,40,45,50,55,60,65,70] 
#mass_points = [10,30] 

# Define paths
executable_template = """#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {base_path}
eval `scramv1 runtime -sh`

cd {mass_path}

combine -m {mass} -M GenerateOnly {base_path}/cards/lowmassDipho_fiveCat_cat0.txt --expectSignal=0 --freezeParameters MH  --saveWorkspace --X-rtd MINIMIZER_MaxCalls=99999999 --X-rtd MINIMIZER_optimizeConst=1 --rMin -5 --rMax 5 --setParameterRanges c_exp_cat0=-0.7,-0.03:coef0_cat0=1.0,10.0:coef1_cat0=-1.0,1.0:coef2_cat0=0.0,5.0:coef3_cat0=0.01,5.0:err_sigma_cat0=11.0,19.0:err_mean_cat0=40.0,55.0:frac_expBern_cat0=0.1,0.6  --cminDefaultMinimizerStrategy 0  --cminDefaultMinimizerTolerance 30 -t 1000 --toysNoSystematics --saveToys

combine -m {mass} -M FitDiagnostics {base_path}/cards/lowmassDipho_fiveCat_cat0.txt --expectSignal=0 --freezeParameters MH  --saveWorkspace --X-rtd MINIMIZER_MaxCalls=99999999 --X-rtd MINIMIZER_optimizeConst=1 --rMin -7 --rMax 7 --setParameterRanges c_exp_cat0=-0.7,-0.03:coef0_cat0=1.0,10.0:coef1_cat0=-1.0,1.0:coef2_cat0=0.0,5.0:coef3_cat0=0.01,5.0:err_sigma_cat0=11.0,19.0:err_mean_cat0=40.0,55.0:frac_expBern_cat0=0.1,0.6  --cminDefaultMinimizerStrategy 0  --cminDefaultMinimizerTolerance 10 -t 1000 --toysFile {exe_path}/outputFiles/higgsCombineTest.GenerateOnly.mH{mass}.123456.root --keepFailures
"""

submission_template = """universe = vanilla
executable = {executable_path}
output = {mass_path}/bias_study.$(ClusterId).$(ProcId).out
error = {mass_path}/bias_study.$(ClusterId).$(ProcId).err
log = {mass_path}/bias_study.$(ClusterId).log
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
requirements = (OpSysAndVer =?= "CentOS7")
transfer_input_files = {executable_path},{base_path}/cards/lowmassDipho_fiveCat_cat0.txt,{exe_path}/outputFiles/higgsCombineTest.GenerateOnly.mH{mass}.123456.root
+JobFlavour = "testmatch"
queue 1
"""
#transfer_output_files = {mass_path}/fitDiagnosticsTest.root,{mass_path}/higgsCombineTest.FitDiagnostics.mH{mass}.123456.root

# Generate directories, submission files, and executables
base_path = "/afs/cern.ch/work/e/elfontan/private/DiPhotonAnalysis/StatisticalAnalysis/CMSSW_11_3_4/src/Combine/"
exe_path = "/afs/cern.ch/work/e/elfontan/private/DiPhotonAnalysis/StatisticalAnalysis/CMSSW_11_3_4/src/Combine/BiasStudy/condorSub/"
for mass in mass_points:
    mass_path = os.path.join(exe_path, f"m{mass}/")
    os.makedirs(mass_path, exist_ok=True)
    print("base_path = ", base_path)
    print("exe_path = ", exe_path)
    print("mass_path = ", mass_path)

    # Write executable
    executable_path = os.path.join(mass_path, f"bias_study_{mass}.sh")
    with open(executable_path, "w") as f:
        f.write(executable_template.format(base_path=base_path,exe_path=exe_path, mass_path=mass_path, mass=mass))

    # Write submission file
    #output_root_file = os.path.join(mass_path, f"higgsCombineTest.GenerateOnly.mH{mass}.123456.root")
    submission_path = os.path.join(exe_path, f"m{mass}", f"bias_study_{mass}.submit")
    with open(submission_path, "w") as f:
        f.write(submission_template.format(executable_path=executable_path, base_path=base_path, mass_path=mass_path, mass=mass, exe_path=exe_path))

    print(f"Created directory, executable, and submission file for mass point {mass}.")

print("All directories, executables, and submission files created successfully.")
