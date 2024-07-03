import shutil
import fileinput

for m in range(11,71):
  mass = str(m)
  shutil.copy('config_10.py', 'config_'+mass+'.py')

  f = fileinput.input('config_'+mass+'.py', inplace=True)
  for line in f:
    print(line.replace("10GeV", mass+"GeV"))
  f.close()
