Preliminary Limit Estimations

This directory contains C++ files that were taken from a different framework made for running sliding window limit estimates on input histograms.
You can find the code for producing these input histograms in the AnalysisTools directory of atsatsos97's flashgg repository. [TO BE COMMITTED SOON]

To set up the framework:
```cmsenv
source setup.sh```

To create the datacards and workspaces from input histograms: `root -l makeCardsandWS.cpp`
This will produce histograms with fits, datacards, and workspaces in the output directory.
Fits are based on a sliding window mass range, using triple Gaussian or DCB+Gaussian for signal and using Bernstein polynomials for background.

To run limits on the output datacards run `./limitest.sh` in the output directory
This will run combine using AsymptoticLimits for each mass point.
