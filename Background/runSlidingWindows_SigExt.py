import os

#mass_points = [10,15,20,25,30,35,40,45,50,55,60,65,70] 
#mass_points = [10,30] 

# Define paths
# Put shell script lines here
executable_template = """python RunBackgroundScripts_lite.py --inputConfig SlidingWindowConfigs_1GeV/config_{mass}.py --mode fTest --modeOpts "--gofCriteria 0.00 --pvalFTest 1.01 --maxOrder 3 --nBins {nbins}"
"""

# Generate executable script and run it
for mass in range(10,71):
    nbins=4*mass

    # Write executable
    with open("./runSlidingWindows_SigExt.sh", "a") as f:
        f.write(executable_template.format(mass=mass, nbins=nbins))

    print mass," is done"
