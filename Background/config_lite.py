# Config file: options for signal fitting

backgroundScriptCfg = {
  
  # Setup
  'inputWSFile':'/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/Mar2024_ParametricNNNearest_NN0.780/10GeV/ws/out_all2018Data_bkg_v1.root', # location of 'allData.root' file
  'cats':'auto', # auto: automatically inferred from input ws
  'ext':'lite', # extension to add to output directory
  'year':'2018', # Use merged when merging all years in category (for plots)
  'mass':'10GeV', # Mass point for sliding window

  # Job submission options
  'batch':'local', # [condor,SGE,IC,local]
  'queue':'microcentury' # for condor e.g. microcentury
  
}
