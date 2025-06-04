# Config file: options for signal fitting

backgroundScriptCfg = {
  
  # Setup
  'inputWSFile':'/eos/user/a/atsatsos/ULFlashGG_Files/NewReleaseFiles/SEP2024FITWS_SIGEXT/10pData_SubRanges/ws/FullRange_all2018data.root', # location of 'allData.root' file
  'cats':'UntaggedTag_0', # auto: automatically inferred from input ws
  'ext':'lite', # extension to add to output directory
  'year':'2018', # Use merged when merging all years in category (for plots)
  'mass':'FullRange', # Mass point for sliding window

  # Job submission options
  'batch':'condor', # [condor,SGE,IC,local]
  'queue':'longlunch' # for condor e.g. microcentury
  
}
