import os
import glob
import pandas as pd
os.chdir("/Data Scrapping")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "dataset_temp.csv", index=False, encoding='utf-8-sig')



df = pd.read_csv("dataset.csv") # avoid header=None. 
shuffled_df = df.sample(frac=1)
shuffled_df.to_csv("dataset.csv", index=False)