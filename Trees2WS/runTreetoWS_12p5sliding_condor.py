import os

#mass_points = [10,15,20,25,30,35,40,45,50,55,60,65,70] 
#mass_points = [10,30] 

# Define paths
# Put shell script lines here
executable_template = """python RunWSScripts.py --inputConfig config_simple.py --inputDir /eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/Categorization/ --mode "trees2ws_data" --mass "{mass}GeV" --modeOpts "--outputWSDir /eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/JUL2024FITWS_SIGEXT/10pData_12p5SlidingWindow/ --mgg-range {masslow10} {masshigh10}" \n"""

# Generate executable script and run it
for m in range(10,71):
    mass = m
    masslow10 = 0.875*mass
    masshigh10 = 1.125*mass

    # Write executable
    with open("./runTreetoWS_12p5sliding_sigext_condor.sh", "a") as f:
        f.write(executable_template.format(masslow10=masslow10, masshigh10=masshigh10, mass=mass))

    print mass," is done"