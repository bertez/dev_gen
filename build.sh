#!/bin/sh

if [ -d "build" ]; then
    rm -rfv build
fi

mkdir build
zip -r build/dev_gen.zip * --exclude "*build*" --exclude "*.pyc" --exclude "README.md"
cd build
echo '#!/usr/bin/env python' | cat - dev_gen.zip > dev_gen
rm dev_gen.zip
chmod +x dev_gen
