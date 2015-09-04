#!/bin/sh

tar xvfz muscle3.8.31_src.tar.gz
cd muscle3.8.31/src
make
mkdir ../../bin
mv muscle ../../bin
cd ../..
rm -Rf muscle3.8.31

echo "Done"