#!/bin/sh
# Removing rows that contain " or '
sed -e "/'/d" -e '/"/d' ../Norms/AssociationNorms/strength.SWOW-EN.R123.csv > ../Norms/AssociationNorms/cleansedStrength.csv
