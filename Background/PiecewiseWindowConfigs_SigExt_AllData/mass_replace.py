import shutil
import argparse
import fileinput

parser = argparse.ArgumentParser()
parser.add_argument('--mass', type=str, help='mass point')
args = parser.parse_args()

mass = args.mass

shutil.copy('config_1.py', 'config_'+mass+'.py')

f = fileinput.input('config_'+mass+'.py', inplace=True)
for line in f:
    print(line.replace("Window1", "Window"+mass))
f.close()
