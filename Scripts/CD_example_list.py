import pandas as pd
from grocio_utils import *

ASSOCIATION_NROMS_PATH = '../Norms/AssociationNorms/association_matrix.csv' #Preprocessed data
association_df = pd.read_csv(ASSOCIATION_NROMS_PATH, index_col=0)

example_list = ['apple', 'banana', 'orange']
#association_df = association_df.loc[example_list, example_list]
#print(association_df)

diag = []
for i in range(3):
    diag.append(association_df.iloc[i,i])

print("Manual")
print('diag sum:', sum(diag))
print('all sum:', sum(association_df.sum()))

print( (sum(association_df.sum()) - sum(diag)) / 6 )

li = [0.0203,0.0845,0.0340,0.0136,0.0612,0.0136]
print(sum(li)/6)

#print(connectivity_calc(cueres_df=association_df, multi_li=[example_list]))

multi_li = [['apple','banana','orange'], ['cat', 'dog', 'lion']]

# Check validity of the function, connectivity_calc
print(connectivity4grouped_lists(cueres_df=association_df,
    multi_li=multi_li))

flatten_words = sum(multi_li, [])
association_df = association_df.loc[flatten_words, flatten_words]
print(association_df)
