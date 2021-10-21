"""
Packages
"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

plt.style.use('seaborn')

#Import dataframehjkhj
#os.chdir('/home/pando004/Desktop/BankData/FRY15')
# os.chdir('G:/Shared drives/BankBusinessLines/Data/FRY15')
os.chdir('/home/ryan0463/Documents/Research/BankBusinessLines')

# import one file for now
FRY9_location = os.getcwd() + '/'
directory = os.fsencode(FRY9_location)

# 2d array where rows are banks, columns are (i) date (ii) id
#           (iii) payments activity RISK M390
#           (iv)  custody assets RISK M405
#           (v) total underwriting RISK M408

iterator = 0
#merge all data files in folder
for file in os.listdir(directory):

    print('Iteration',iterator,' out of', len(os.listdir(directory)) )
    iterator = iterator + 1

    # attain bank ID
    bank_id = int( str(file)[8:15] )

    # attain report date
    report_date = int( str(file)[16:24] )

    # read in the file
    filename = os.fsdecode(file)

    temp = pd.read_csv(FRY9_location+filename)

    try:
        payments     = np.float( temp[ temp.ItemName == 'RISKM390' ]['Value'] )
        underwriting = np.float( temp[ temp.ItemName == 'RISKM408' ]['Value'] )
        custody      = np.float( temp[ temp.ItemName == 'RISKM405' ]['Value'] )
    except:
        payments     = 0
        underwriting = 0
        custody      = 0

    if iterator == 1:
        bank_array = np.array(( report_date, bank_id, payments, underwriting, custody  )).reshape(1,5)

    else:

        bank_array = np.append( bank_array, np.array((report_date, bank_id, payments, underwriting, custody )).reshape(1,5), axis = 0 )

# convert to a dataframe and export
df = pd.DataFrame( bank_array, columns = ['date','id','payments','underwriting','custody'] )

df.to_csv('Data/fr15data.csv')
