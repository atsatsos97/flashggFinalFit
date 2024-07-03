import os

#mass_points = [10,15,20,25,30,35,40,45,50,55,60,65,70] 
mass_points = [10,30] 

# Define paths
executable_template = """#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {base_path}
eval `scramv1 runtime -sh`

cd {mass_path}

combine -m {mass} -M GoodnessOfFit --algorithm KS {base_path}/sliding_{mass}GeV_cat0.txt --freezeParameters MH  --saveWorkspace --X-rtd MINIMIZER_MaxCalls=99999999 --X-rtd MINIMIZER_optimizeConst=1 --rMin -7 --rMax 7 --cminDefaultMinimizerStrategy 1 --cminDefaultMinimizerTolerance 1 --X-rtd MINIMIZER_freezeDisassociatedParams -t 1000 --toysFrequentist --saveToys -n Toys 

combine -m {mass} -M GoodnessOfFit --algorithm KS {base_path}/sliding_{mass}GeV_cat0.txt --freezeParameters MH  --saveWorkspace --X-rtd MINIMIZER_MaxCalls=99999999 --X-rtd MINIMIZER_optimizeConst=1 --rMin -7 --rMax 7 --cminDefaultMinimizerStrategy 1 --cminDefaultMinimizerTolerance 1 --X-rtd MINIMIZER_freezeDisassociatedParams 
"""

submission_template = """universe = vanilla
executable = {executable_path}
output = {mass_path}/gof_study.$(ClusterId).$(ProcId).out
error = {mass_path}/gof_study.$(ClusterId).$(ProcId).err
log = {mass_path}/gof_study.$(ClusterId).log
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
requirements = (OpSysAndVer =?= "CentOS7")
transfer_input_files = {executable_path},{base_path}/sliding_{mass}GeV_cat0.txt
+JobFlavour = "longlunch"
queue 1
"""

# Generate directories, submission files, and executables
base_path = "/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_11_3_4/src/flashggFinalFit/Combine/datacards_sliding/"
exe_path = "/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_11_3_4/src/flashggFinalFit/Combine/datacards_sliding/condorSub/"
#for mass in mass_points:
for mass in range(10,71):
    mass_path = os.path.join(exe_path, "cat0/")
    os.makedirs(mass_path, exist_ok=True)
    print("base_path = ", base_path)
    print("exe_path = ", exe_path)
    print("mass_path = ", mass_path)

    # Write executable
    executable_path = os.path.join(mass_path, f"gof_study_{mass}.sh")
    print("executable_path = ", executable_path)
    with open(executable_path, "w") as f:
        f.write(executable_template.format(base_path=base_path,exe_path=exe_path, mass_path=mass_path, mass=mass))

    # Write submission file
    #output_root_file = os.path.join(mass_path, f"higgsCombineTest.GenerateOnly.mH{mass}.123456.root")
    submission_path = os.path.join(mass_path, f"gof_study_{mass}.submit")
    with open(submission_path, "w") as f:
        f.write(submission_template.format(executable_path=executable_path, base_path=base_path, mass_path=mass_path, mass=mass, exe_path=exe_path))

    print(f"Created directory, executable, and submission file for mass point {mass}.")

print("All directories, executables, and submission files created successfully.")
