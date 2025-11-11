#law run shi.HelloWorld \
#    --version dev \
#    --datacards $DHI_EXAMPLE_CARDS \
#    --custom-message "My custom analysis!" \
#    --xsec fb \
#    --y-log \
#    --print-output 0

law run shi.bbbbCommands \
    --version custom_arg_v2 \
    --datacards "datacard_bbbb/datacard.txt" \
    --custom-arg "--X-rtd TMCSO_AdaptivePseudoAsimov=0 --X-rtd TMCSO_PseudoAsimov=0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --freezeParameters lumiscale --setParameters lumiscale=21.8 " \
    --pois kl \
    --scan-parameters kl,-30,30,40

