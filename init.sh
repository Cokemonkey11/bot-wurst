#!/bin/bash

# Fetch a sparse checkout of the STL.
echo "Checking out the STL..."
mkdir WurstScript
cd    WurstScript
git init
git remote add origin git@github.com:peq/WurstScript.git
git config core.sparseCheckout true
echo "Wurstpack/wurstscript/lib" > .git/info/sparse-checkout
git pull origin master --depth 1
cd ..
echo "Done."
echo " "

# Build cache of public functions.
echo "Caching public functions..."
python build-cache.py > stl.txt
echo "Done."
echo " "

echo "Use \`./wurst saveReal\` to search for \`saveReal\` in public functions."
echo " "
