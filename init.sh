#!

# Fetch a sparse checkout of the STL.
mkdir WurstScript
cd    WurstScript
git init
git remote add -f origin git@github.com:peq/WurstScript.git
git config core.sparseCheckout true
chmod 777 .git/info/sparse-checkout
echo "Wurstpack/wurstscript/lib" > .git/info/sparse-checkout
git pull origin master
cd ..

# Build cache of public functions.
grep -rnw './Wurstpack/wurstscript/lib/' -e "public function .*$" > stl.txt
