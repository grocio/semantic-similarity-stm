from grocio_utils import *
import numpy as np
import pandas as pd
import numpy.ma as ma
import copy
from pprint import pprint
import random

random.seed(1234)

cueres_df = pd.read_csv('../Norms/AssociationNorms/association_matrix.csv',
        index_col = 0)

def simple_connectivity(cueres_df, li):
    df_col_names = cueres_df.columns
    intersection_cols = set(df_col_names) & set(li)
    intersection_cols = sorted(list(intersection_cols))
    # print(intersection_cols)

    current_df = cueres_df.loc[intersection_cols, intersection_cols]
    length = len(current_df)
    diag_elems = [current_df.iloc[j,j] for j in range(length)]
    diag_sum = np.nansum(diag_elems)

    # print(diag_sum)
    # print(sum(current_df.sum()))

    # print(current_df)

    if length > 1:
        return (sum(current_df.sum()) - diag_sum) / (length * (length - 1))
    else:
        return np.nan

#test_li = ['apple', 'banana', 'orange']
#print(simple_connectivity(cueres_df, test_li))

def random_set_generator(multi_li):
    item_n = len(multi_li[0])
    group_n = len(multi_li)

    ungrouped_words = []

    for n in range(group_n):
        current_li = []
        if group_n >= item_n:
            rand_group_index = random.sample(range(group_n), k=item_n) #without replacement
        elif group_n < item_n:
            rand_group_index = random.choices(range(group_n), k=item_n) #with replacement

        rand_item_index = random.sample(range(item_n), k=item_n)

        for m in range(item_n):
            i = rand_group_index[m]
            j = rand_item_index[m]
            current_li.append(multi_li[i][j])

        ungrouped_words.append(current_li)

    return ungrouped_words

materials_names = ['Crowder_1979_Exp1_Noun.xlsx',
                   'Crowder_1979_Exp2_Adjective.xlsx',
                   'Saint-Aubin_1995_Exp12.xlsx',
                   'Saint-Aubin_1995_Exp3.xlsx',
                   'Saint-Aubin_1999a_Exp1.xlsx',
                   'Saint-Aubin_1999a_Exp23.xlsx',
                   'Tse_2011_Associative.xlsx',
                   'Tse_2011_Categorical.xlsx']

materials_path = '../Materials/'

all_sets = []
for m_name in materials_names:
    all_sets.append(materials4groupedlist(materials_path + m_name))

random_all_sets = []
for mul_li in all_sets:
    random_all_sets.append(random_set_generator(mul_li))

flatten_sim_lists = []
for li in all_sets:
    for li2 in li:
        flatten_sim_lists.append(li2)


flatten_dissim_lists = []
for li in random_all_sets:
    for li2 in li:
        flatten_dissim_lists.append(li2)

"""
with open('sim.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    for li in all_sets:
        writer.writerows(['---------'])
        writer.writerows(li)

with open('dissim.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    for li in random_all_sets:
        writer.writerows(['---------'])
        writer.writerows(li)
"""

flatten_lists = flatten_sim_lists + flatten_dissim_lists

print('Number of grouped sets:', len(flatten_sim_lists))
print('Number of ungrouped sets:', len(flatten_dissim_lists))

def dissim_connect_calc(flatten_li):
    dissimilarity_li = []
    connectivity_li = []
    for li in flatten_li:
        dissimilarity_li.append(np.nanmean(dists_from_centroid(li)))
        connectivity_li.append(simple_connectivity(cueres_df, li))

    return np.nanmean(dissimilarity_li), np.nanstd(dissimilarity_li), np.nanmean(connectivity_li), np.nanstd(connectivity_li)

print('Grouped sets:', dissim_connect_calc(flatten_sim_lists))
print('Ungrouped sets:', dissim_connect_calc(flatten_dissim_lists))
