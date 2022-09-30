Authors: Vincent Klyverts Tofterup, vkt@mmmi.sdu.dk
Version: 1.1
Date: 03-27/2019 Original material
Date: 11-05/2020 Updated to IDT course

Description: IDT Course material for UAV attitude failure detection
License: BSD 3-Clause


Prerequisites:

python 2.7 with matplotlib, csv, numpy, and math libraries installed
ulog files can be reviewed at https://logs.px4.io/


Running python:

Linux:
In terminal run:
	python data_reader.py

Remember to be in the correct directory, or change paths in python file.

Video documentation of tests:

Test 5: https://youtu.be/raK2fnk5ULk
Test 8: https://youtu.be/gJK06kHUvz8
Test 9: https://youtu.be/opDSC2ox-c4


Folder structure:

-->csv_files
	-->TEST5_30-01-19: folder containing all logged data from test 5 seperated into csv files (done by using the ulog2csv python tool)
	-->TEST8_30-01-19: folder containing all logged data from test 8 seperated into csv files (done by using the ulog2csv python tool)
	-->TEST9_09-02-19: folder containing all logged data from test 9 seperated into csv files (done by using the ulog2csv python tool)
-->ulog_files
	-->TEST5_30-01-19.ulg: PixHawk log file from test 5
	-->TEST8_30-01-19.ulg: PixHawk log file from test 8
	-->TEST9_09-02-19.ulg: PixHawk log file from test 9
-->data_reader
	data_reader.py example python script/class for loading data from csv files and plotting them (it is for the moment created to work with test 9, change names in file)
	
readme.txt: this file
