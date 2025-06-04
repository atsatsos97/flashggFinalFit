import os

#mass_points = [10,15,20,25,30,35,40,45,50,55,60,65,70] 
#mass_points = [10,30] 

# Define paths
# Put shell script lines here
executable_template = """python RunWSScripts.py --inputConfig config_simple.py --inputDir /eos/user/e/elfontan/DiPhotonAnalysis/diphotonBDT/NTUPLES_May2024/nearest_flat/Categorization/ --mode "trees2ws_data" --mass "{mass}GeV" --modeOpts "--outputWSDir /eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/SEP2024FITWS_SIGEXT/10pData_SlidingWindow/ --mgg-range {masslow10} {masshigh10}" \n"""

# Generate executable script and run it
for debulk in range(1,7):
   for m in range(0,100):
      mass = (m+100*debulk)/10.0
      masslow10 = 0.9*mass
      masshigh10 = 1.1*mass

      # Write executable
      with open("./runTreetoWS_sliding_sigext_condor_"+str(debulk)+".sh", "a") as f:
        f.write(executable_template.format(masslow10=masslow10, masshigh10=masshigh10, mass=mass))

      print mass," is done"

with open("./runTreetoWS_sliding_sigext_condor_6.sh", "a") as f:
  f.write(executable_template.format(masslow10=63.0, masshigh10=77.0, mass=70.0))

print "70.0 is done"


#for m in range(100,701):
#    mass = m/10.0
#    masslow10 = 0.9*mass
#    masshigh10 = 1.1*mass

    # Write executable
#    with open("./runTreetoWS_sliding_sigext_condor.sh", "a") as f:
#        f.write(executable_template.format(masslow10=masslow10, masshigh10=masshigh10, mass=mass))

#    print mass," is done"
