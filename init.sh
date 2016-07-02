#!

# Fetch a sparse checkout of the STL.
mkdir WurstScript
cd    WurstScript
git init
git remote add origin git@github.com:peq/WurstScript.git
git config core.sparseCheckout true
echo "Wurstpack/wurstscript/lib" > .git/info/sparse-checkout
git pull origin master --depth 1
cd ..

# Build cache of public functions.
grep -rnw './WurstScript/Wurstpack/wurstscript/lib/' -e "public function .*$" > stl.txt
