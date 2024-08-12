import os

#mass_points = [10,15,20,25,30,35,40,45,50,55,60,65,70] 
#mass_points = [10,30] 

# Define paths
# Put shell script lines here
executable_template = """python RunBackgroundScripts_lite.py --inputConfig SlidingWindowConfigs_SigExt_AllData_HighGran/config_{mass}.py --mode fTest --modeOpts "--gofCriteria 0.00 --pvalFTest 1.01 --maxOrder 3 --nBins {nbins}"
"""

# Generate executable script and run it
for m in range(100,701):
    mass = m/10.0
    nbins=int(4*mass)

    # Write executable
    with open("./runSlidingWindows_SigExt_highgran.sh", "a") as f:
        f.write(executable_template.format(mass=mass, nbins=nbins))
