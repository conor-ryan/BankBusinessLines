"""
Packages
"""
import numpy as np
import pandas as pd
import os

"""
Line Items
"""
#RIAD tags
rssd = ['9999'] # filing date,

bhck = [
                            ###  SCHEDULE HI   ###
        # interest income
        '4435','4436','F821','4059','4065','4115','B488','B489','4060','4069','4020','4518','4107','4230',
        # interest expense
        'HK03','HK04','6761','4172','4180','4185','4397','4398','4073','4074','JJ33',
        # noninterest income
        '4070','4483','A220','C886','C888','C887','C386','C387','KX46','KX47','B491','B492','B493','8560','8561','B496','B497','4079','3521','3196',
        # noninterest expense
        '4135','4217','C216','C232','4092','4093','HT69','HT70','4301','4302','4300','FT28','G104','G103','4340','4484',
        # other noninterest items
        'C013','C014','C016','4042','C015','F555','T047','C017','0497','4136','C018','8403','4141','4146','F556','F557','F558','F559','Y923','Y924','3200',
        # changes in equity capital
        'B508','3577','3578','3579','3580','4782','4783','4598','4460','B511',
                        ###    SCHEDULE HC    ###
        # assets
        '0081','0395','0397','JJ34','1773','JA22','B989','5369','B528','3123','B529','3545','2145','2150','2130','3656','2143','2160','2170',
        # liabilities
        'B995','3548','3190','4062','C699','2750','2948','3247','G105','3300',
                            ###    SCHEDULE HC-B    ###
        # sovereign securities
        '0211','0213','1286','1287','HT50','HT51','HT52','HT53','8496','8497','8498','8499',
        # mbs
        'G300','G301','G302','G303','G304','G305','G306','G307','G308','G309','G310','G311',
        'KX52','KX53','KX54','KX55','G312','G313','G314','G315','G316','G317','G318','G319',
        'G320','G321','G322','G323','K142','K143','K144','K145','K146','K147','K148','K149',
        'K150','K151','K152','K153','K154','K155','K156','K157','C026','C988','C989','C027',
        'HT58','HT59','HT60','HT61','1737','1738','1739','1741','1742','1743','1744','1746',
        'A510','A511','1754','1771','1772','1773'
                        ###    Schedule HC-C    ###
        '1410','1292','1296','1590','1763','2081','J454','1545','J451','KX57','F162','F163','KX58','2122',
                        ###    Schedule HC-V    ###
        'J981','JF84','HU20','HU21','HU22','HU23','K009','JF89','JF91','JF90','JF92','JF85','JF93','JF86','K030','JF87','K033','JF88','JF77','JF78',

        # pre-2001 variables
        '0278','0279','3210','2800','0276','0277','2332','2333','1350','4010','A517','A518','B490','3000', '3163','0426'
        ]

bhcb = [
                        ###    Schedule HC-E    ###
        '2210','3187','2389','HK29','J474'
        ]

bhod = [
                        ###    Schedule HC-E    ###
        '2210','3187','2389','HK29','J474'
        ]

bhct = [
        # equity capital, Schedule HI
        '4340','3210',
        # securities Schedule HC-B
        '1773'
        ]

bhfn = [
        #schedule HC, liabilities
        '6631','6636'
        ]
bhdm = [
        # Schedule HC assets and liabilities
        '6631','6636','B987','B993',
        # Schedule HC-C
        '1766','1975'
        ]

bhca = [
                        ###    Schedule HC-R    ###
        'P793','7206','7205','7204','H036','H311','H312'
        ]

bhcw = [
                        ###    Schedule HC-R    ###
        'P793','7206','7205'
        ]

# create list of RIAD, RCON, RCFD items
RSSD_items = []
BHCK_items = []
BHCB_items = []
BHOD_items = []
BHCT_items = []
BHFN_items = []
BHDM_items = []
BHCA_items = []
BHCW_items = []

for i in range(len(rssd)):
    RSSD_items.append( 'RSSD'+str(rssd[i]) )

for i in range(len(bhck)):
    BHCK_items.append( 'BHCK'+str(bhck[i]) )

for i in range(len(bhcb)):
    BHCK_items.append( 'BHCB'+str(bhcb[i]) )

for i in range(len(bhod)):
    BHCK_items.append( 'BHOD'+str(bhod[i]) )

for i in range(len(bhct)):
    BHCK_items.append( 'BHCT'+str(bhct[i]) )

for i in range(len(bhfn)):
    BHCK_items.append( 'BHFN'+str(bhfn[i]) )

for i in range(len(bhdm)):
    BHCK_items.append( 'BHDM'+str(bhdm[i]) )

for i in range(len(bhca)):
    BHCK_items.append( 'BHCA'+str(bhca[i]) )

for i in range(len(bhcw)):
    BHCK_items.append( 'BHCW'+str(bhcw[i]) )

# one long list
ItemList = np.concatenate(( RSSD_items,BHCK_items,BHCB_items,BHOD_items,BHCT_items,
                            BHFN_items,BHDM_items,BHCA_items,BHCW_items ))

#set directory
directory = os.fsencode('/home/pando004/Desktop/BankData/FRY9/')

"""
Filtering Data
"""
# initialize dataframe
GenDF = pd.DataFrame()

iterator = 1
#merge all data files in folder
for file in os.listdir(directory):

    print('Iteration',iterator,' out of', len(os.listdir(directory)) )
    iterator = iterator + 1

    #initialize temporary dataframe
    newDF = pd.DataFrame()

    filename = os.fsdecode(file)

    if 'bhcf' == filename[:4]:

        try:
            temp = pd.read_csv('/home/pando004/Desktop/BankData/FRY9/'+filename,delimiter='^',skiprows=[1],dtype=object,error_bad_lines=False,na_values='--------')
        except UnicodeDecodeError:
            temp = pd.read_csv('/home/pando004/Desktop/BankData/FRY9/'+filename,delimiter='^',skiprows=[1],dtype=object,error_bad_lines=False,na_values='--------',encoding = 'unicode_escape')

        try:
            temp = temp.set_index('RSSD9001')
        except KeyError:
            temp['RSSD9001'] = temp['rssd9001']
            temp['RSSD9999'] = temp['rssd9999']
            temp = temp.set_index('RSSD9001')

        #find titles that match list items
        matches = list( set(list(temp)) & set(ItemList))

        #extract reduced dataset
        temp_red = temp[ matches ]
        #merge to larger one
        newDF = pd.concat( [newDF,temp_red], axis=1)

        #Drop duplicate variables
        newDF = newDF.loc[:,~newDF.columns.duplicated() ]

        #Titles that were not found in call report file
        missing = list( set(ItemList) - set(list(newDF)) )

        for i in range(len(missing)):
            newDF['%s'%missing[i]] = np.nan


        #GenDF merge
        GenDF = pd.concat( [GenDF,newDF], axis = 0 )

# convert variables to numeric format
GenDF[ BHCK_items ] = GenDF[ BHCK_items ].apply( pd.to_numeric )
GenDF[ BHCB_items ] = GenDF[ BHCB_items ].apply( pd.to_numeric )
GenDF[ BHOD_items ] = GenDF[ BHOD_items ].apply( pd.to_numeric )
GenDF[ BHCT_items ] = GenDF[ BHCT_items ].apply( pd.to_numeric )
GenDF[ BHFN_items ] = GenDF[ BHFN_items ].apply( pd.to_numeric )
GenDF[ BHDM_items ] = GenDF[ BHDM_items ].apply( pd.to_numeric )
GenDF[ BHCA_items ] = GenDF[ BHCA_items ].apply( pd.to_numeric )
GenDF[ BHCW_items ] = GenDF[ BHCW_items ].apply( pd.to_numeric )

GenDF.to_csv('/home/pando004/Desktop/BankData/FRY9/frdata.csv')


# This is git test line.
