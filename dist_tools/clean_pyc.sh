#!/bin/bash

echo ""
for i in `find ./ -name \*.pyc -print`; do
    echo "[+] cleaning $i"
    rm $i;
done
