#! /bin/bash

for year in L3 M1 M2; do
  for semester in 1 2; do
    edt2ics --host localhost:2201 --semester $semester \
      --output "ics/${year}-S${semester}.ics" $year
  done
done
