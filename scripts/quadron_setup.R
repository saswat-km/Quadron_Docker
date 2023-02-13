# This script is to set up the environment that is needed to run
# Quadron. Namely, it requires the xgboost library with the specific version
# 0.4-4, which is possible to install with the renv and remotes packages.
# this only needs to be run once. Then quadron needs to be run in the same
# folder as this was run (there an 'renv' folder will appear). 

require(renv)
renv::settings$snapshot.type("all")
renv::restore()
install.packages('remotes')
require(remotes)
install_version('xgboost', version='0.4-4')
renv::snapshot()
