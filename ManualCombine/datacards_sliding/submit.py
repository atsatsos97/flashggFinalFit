import os

# Define paths
# Put shell script lines here
executable_template = """condor_submit ./condorSub/cat{cat}/gof_study_{mass}.submit
"""

# Generate executable script and run it
for mass in range(10,71):
  for cat in range(0,2):
    # Write executable
    with open("./submit.sh", "a") as f:
        f.write(executable_template.format(mass=mass, cat=cat))
  print mass," is done"
