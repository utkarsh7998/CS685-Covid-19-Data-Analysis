Language Used : Python 3.8

Python Libraries used:
numpy
pandas
json
datetime
openpyxl
warnings

Prerequisites: 

1. The above language and all the mentioned libraries must be installed in your local machine before proceeding further.
2. Patience because sometimes it takes a bit longer longer than usual to complete execution.


Datasets/ Input Files

neighbor-districts.json
http://data.covid19india.org/csv/latest/cowin_vaccine_data_districtwise.csv
http://censusindia.gov.in/pca/DDW_PCA0000_2011_Indiastatedist.xlsx
https://data.covid19india.org/csv/latest/districts.csv


Instructions to run:-

Step 1: Extract 21111063-assign1.zip in your local machine

Step 2: Open Terminal in Ubuntu by pressing 'Ctrl + Shift + T'

Step 3: Navigate to the folder where your files are extracted
        For example: cd path/21111062-assign1/

Step 4: Type the following command to give permission to the sh file to be executed
        chmod +x ./assign1.sh
            
Step 5: Type the following command to run the file. This command will run all the files one by one automatically.
        After a few minutes you will see a number of output files generated in the same directory. 
        ./assign1.sh


Output Files:-

For Question_1 : neighbor-districts-modified.json

For Question_2 : edge-graph.csv

For Question_3 : cases-week.csv
                 cases-month.csv
                 cases-overall.csv

For Question_4 : district-peaks.csv
                 state-peaks.csv
                 overall-peaks.csv

For Question_5 : district-vaccinated-count-week.csv
                 district-vaccinated-count-month.csv
                 district-vaccinated-count-overall.csv
                 state-vaccinated-count-week.csv
                 state-vaccinated-count-month.csv
                 state-vaccinated-count-overall.csv

For Question_6 : district-vaccination-population-ratio.csv
                 state-vaccination-population-ratio.csv
                 overall-vaccination-population-ratio.csv

For Question_7 : district-vaccine-type-ratio.csv
                 state-vaccine-type-ratio.csv
                 overall-vaccine-type-ratio.csv

For Question_8 : district-vaccinated-dose-ratio.csv
                 state-vaccinated-dose-ratio.csv
                 overall-vaccinated-dose-ratio.csv

For Question_9 : complete-vaccination.csv


