# Config file: options for signal fitting

backgroundScriptCfg = {
  
  # Setup
  'inputWSFile':'/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/MAY2024FITWS/10pData_PiecewiseWindow1/ws/all2018data_v1.root', # location of 'allData.root' file
  'cats':'auto', # auto: automatically inferred from input ws
  'ext':'lite', # extension to add to output directory
  'year':'2018', # Use merged when merging all years in category (for plots)
  'mass':'Window1', # Mass point for sliding window

  # Job submission options
  'batch':'local', # [condor,SGE,IC,local]
  'queue':'microcentury' # for condor e.g. microcentury
  
}
