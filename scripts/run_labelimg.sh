docker pull tzutalin/py2qt4
echo "Starting lableimg at path $PWD"
docker run -it -v=$(pwd):$(pwd) --workdir=$(pwd)/tmp --rm tzutalin/py2qt4