SECONDS=0
echo "Assignment 1 starts. This may take a couple minutes. Please wait."
chmod +x ./Answer1.sh
./Answer1.sh
chmod +x ./edge-generator.sh
./edge-generator.sh
chmod +x ./case-generator.sh
./case-generator.sh
chmod +x ./peaks-generator.sh
./peaks-generator.sh
chmod +x ./vaccinated-count-generator.sh
./vaccinated-count-generator.sh
chmod +x ./vaccination-population-ratio-generator.sh
./vaccination-population-ratio-generator.sh
chmod +x ./vaccination-type-ratio-generator.sh
./vaccination-type-ratio-generator.sh
chmod +x ./vaccinated-ratio-generator.sh
./vaccinated-ratio-generator.sh
chmod +x ./complete-vaccination-generator.sh
./complete-vaccination-generator.sh
echo "Assignment 1 ends here. Thank you for the patience. Time taken is $SECONDS seconds."
