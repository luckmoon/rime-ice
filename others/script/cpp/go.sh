#!/bin/bash

set -x 
set -euo pipefail


rm -rf build
mkdir -p build
cd build
# cmake ..
#cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake -DCMAKE_BUILD_TYPE=RELEASE ..
make -j3
./app/main
