#!/bin/sh

zip -r ../dev_gen.zip *
cd ..
echo '#!/usr/bin/env python' | cat - dev_gen.zip > dev_gen
rm dev_gen.zip
chmod +x dev_gen
