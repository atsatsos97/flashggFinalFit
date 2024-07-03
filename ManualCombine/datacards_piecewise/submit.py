import os

# Define paths
# Put shell script lines here
executable_template = """condor_submit ./{freeze}_cat{cat}/bias_study_W{window}.submit
"""

# Generate executable script and run it
freeze_list = ["freezepdf0","freezepdf1","freezepdf2","freezepdf3","freezepdf4","envelope"]

for freeze in freeze_list:
  for cat in range(0,2):
    for window in range(1,11):
       # Write executable
       with open("./submit.sh", "a") as f:
        f.write(executable_template.format(freeze=freeze, cat=cat, window=window))
       print freeze,cat,window," is done"
