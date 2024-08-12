import os

#mass_points = [10,15,20,25,30,35,40,45,50,55,60,65,70] 
#mass_points = [10,30] 

# Define paths
# Put shell script lines here
executable_template = """python trees2ws_data.py --inputConfig config_simple.py --inputTreeFile /eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/TensorFlow/ParamNN_ntuples/newNtuples_2024May30_4Categories_0p8_0p6_0p5_0/all2018data.root --outputWSDir /eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/MAY2024FITWS_SIGEXT/AllData_12p5pSlidingWindow/ --mgg-range {masslow10} {masshigh10}
mv /eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/MAY2024FITWS_SIGEXT/AllData_12p5pSlidingWindow/ws/all2018data.root /eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/MAY2024FITWS_SIGEXT/AllData_12p5pSlidingWindow/ws/all2018data_{mass}GeV.root\n
"""

# Generate executable script and run it
for mass in range(10,71):
#    masslow10 = 0.9*mass
#    masshigh10 = 1.1*mass
    masslow10 = 0.875*mass
    masshigh10 = 1.125*mass

    # Write executable
    with open("./runTreetoWS_12p5sliding_sigext.sh", "a") as f:
        f.write(executable_template.format(masslow10=masslow10, masshigh10=masshigh10, mass=mass))

    print mass," is done"
