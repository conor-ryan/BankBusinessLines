-The programs data_collect.py and deposit_loan_program.py are responsible
	for compiling/cleaning the bank data

	- data_collect.py inputs bank text files to output frdata.csv
	- deposit_loan_program.py inputs frdata.csv to output a 
		refined data series for deposits, consumer loans and
		commercial loans (frdata_refined.csv)

- I have put the bank text files in the Shared Drive-->Data-->BankData.zip

- Guide/Steps to using

	(1) Download and unzip BankData.zip to local directory

	(2) Set appropriate path (line 139) to input data in data_collect.py

	(3) Set appropriate path (line 204) to output frdata.csv in
		data_collect.py

	(4) Run data_collect.py --> creates frdata.csv

	(5) Set appropriate path (line 12) to input frdata.csv in 
		deposit_loan_program.py

	(6) Set appropriate path (line 490) to output frdata_refined.csv 
		in deposit_loan_program.py

	(7) Run deposit_loan_program.py for illustration of data/stats
		and to create frdata_refined.csv  
