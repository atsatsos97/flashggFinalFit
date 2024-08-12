import shutil
import argparse
import fileinput

for i in range(2,12):
  mass = str(i)
  shutil.copy('config_1.py', 'config_'+mass+'.py')

  f = fileinput.input('config_'+mass+'.py', inplace=True)
  for line in f:
    print(line.replace("Window1", "Window"+mass))
  f.close()
