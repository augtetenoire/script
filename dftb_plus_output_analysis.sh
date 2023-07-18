#!/bin/bash

if [ -z ${1} ] ; then
echo ''
echo 'Please specify as input a DFTB+ output file to be analysed'
echo ''
exit 0
fi

# the first input is the name of the output file from DFTB+ to get the energies
grep 'total energy' ${1} | awk '{print $3}' > extracted_energies.out
if ! [ -s extracted_energies.out ] ; then
grep 'Total Energy' ${1} | awk '{print $3}' > extracted_energies.out
fi
grep 'gradient norm' ${1} | awk '{print $7}' > extracted_gradient_norm.out
if ! [ -s extracted_gradient_norm.out ] ;then
grep 'Maximal force component' ${1} | awk '{print $4}' > extracted_gradient_norm.out
fi
