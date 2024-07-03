import os

#mass_points = [10]
mass_points = [10, 12.25, 15, 18.5, 22.75, 27.75, 34, 41.75, 51, 62.25]

# Define paths
executable_template = """#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {base_path}
eval `scramv1 runtime -sh`

cd {mass_path}

combine -m {mass} -M FitDiagnostics {base_path}window{window}_cat{cat}.txt --expectSignal=0 --freezeParameters MH --saveWorkspace --X-rtd MINIMIZER_freezeDisassociatedParam --rMin -10 --rMax 10  --cminDefaultMinimizerStrategy 0 -t 1000 --toysFrequentist --toysFile {mass_path}higgsCombineEnvelopeCat{cat}.GenerateOnly.mH{mass}.123456.root --keepFailures -n EnvelopeCat{cat}W{window}

"""

submission_template = """universe = vanilla
executable = {executable_path}
output = {mass_path}/bias_study.$(ClusterId).$(ProcId).out
error = {mass_path}/bias_study.$(ClusterId).$(ProcId).err
log = {mass_path}/bias_study.$(ClusterId).log
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
requirements = (OpSysAndVer =?= "CentOS7")
transfer_input_files = {executable_path},{base_path}window{window}_cat{cat}.txt, {mass_path}higgsCombineEnvelopeCat{cat}.GenerateOnly.mH{mass}.123456.root
+JobFlavour = "longlunch"
queue 1
"""

# Generate directories, submission files, and executables
base_path = "/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_11_3_4/src/flashggFinalFit/Combine/datacards_piecewise/"
exe_path = "/afs/cern.ch/work/a/atsatsos/ULLowmassFGG/CMSSW_11_3_4/src/flashggFinalFit/Combine/datacards_piecewise/"
#for mass in mass_points:
for cat in range(0,2):
  for i,mass in enumerate(mass_points):
    window=i+1
    mass_path = os.path.join(exe_path, "envelope_cat"+str(cat)+"/")
    os.makedirs(mass_path, exist_ok=True)
    print("base_path = ", base_path)
    print("exe_path = ", exe_path)
    print("mass_path = ", mass_path)

    # Write executable
    executable_path = os.path.join(mass_path, f"bias_study_W{window}.sh")
    print("executable_path = ", executable_path)
    with open(executable_path, "w") as f:
        f.write(executable_template.format(base_path=base_path,exe_path=exe_path, mass_path=mass_path, mass=mass, window=window, cat=cat))

    # Write submission file
    submission_path = os.path.join(mass_path, f"bias_study_W{window}.submit")
    with open(submission_path, "w") as f:
        f.write(submission_template.format(executable_path=executable_path, base_path=base_path, mass_path=mass_path, mass=mass, exe_path=exe_path, window=window, cat=cat))

    print(f"Created directory, executable, and submission file for mass point {mass}.")

print("All directories, executables, and submission files created successfully.")
