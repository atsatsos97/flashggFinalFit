import os

#mass_points = [10,15,20,25,30,35,40,45,50,55,60,65,70] 
#mass_points = [10,30] 

# Define paths
# Put shell script lines here
executable_template = """python RunBackgroundScripts_lite.py --inputConfig Sliding12p5WindowConfigs_SigExt_10pData/config_{mass}.py --mode fTest --modeOpts "--gofCriteria 0.05 --pvalFTest 0.05 --maxOrder 6 --nBins {nbins}"
"""

# Generate executable script and run it
for mass in range(10,71):
    nbins=5*mass

    # Write executable
    with open("./run12p5SlidingWindows_SigExt.sh", "a") as f:
        f.write(executable_template.format(mass=mass, nbins=nbins))

    print mass," is done"
