#!/bin/bash


find -name 'SnO2_110_water_1-r2scan-NVT-1.ener'|sort -r

echo 'Remove energie.dat and position.pdb forces.xyz (yes/other)?'
read answer
if [ ${answer} == 'yes' ]; then
rm -v energie.dat position.pdb forces.xyz
fi

for i in $(find -name 'SnO2_110_water_1-r2scan-NVT-1.ener'|sort -r) ; do cat $i >> energie.dat ; done
for i in $(find -name 'SnO2_110_water_1-r2scan-NVT-pos-1.pdb'|sort -r) ; do cat $i >> position.pdb ; done
for i in $(find -name 'SnO2_110_water_1-r2scan-NVT-frc-1.xyz'|sort -r) ; do cat $i >> forces.xyz ; done

echo 'File compiled'

gnuplot << EOF
set terminal pdf truecolor
set output "plot_energie_temperature.pdf"
set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
set xtic auto                          # set xtics automatically
set ytic auto                          # set ytics automatically
set xlabel "Timestep (fs)"
set key on inside r t


set ylabel "Temperature (K)"
p 'energie.dat'u 2:4 w lp ,\
'energie.dat' u 2:4  smooth bezier lt rgb '#000000' t 'Temperature'

set ylabel "Ekin (eV)"
p 'energie.dat'u 2:3 w lp ,\
'energie.dat' u 2:3  smooth bezier lt rgb '#000000' t 'Ekin'

set ylabel "Epot (eV)"
p 'energie.dat'u 2:5 w lp ,\
'energie.dat' u 2:5  smooth bezier lt rgb '#000000' t 'Epot'

set ylabel "Etot (eV)"
p 'energie.dat'u 2:6 w lp ,\
'energie.dat' u 2:6  smooth bezier lt rgb '#000000' t 'Etot'

set ylabel "Time (s)"
p 'energie.dat'u 2:7 w lp ,\
'energie.dat' u 2:7  smooth bezier lt rgb '#000000' t ' Time'


EOF


