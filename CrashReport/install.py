# requirement
#
# python3.6


import pip

def install(package):
    pip.main(['install', package])

## main ##
install('selenium')
