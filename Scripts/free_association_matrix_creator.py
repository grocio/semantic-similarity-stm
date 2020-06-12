"""
This script creats a cue-response matrix for words used in our targeted (previous) studies on STM.
We focus on the intersect of a) cue words in norms and b) words in previous studies.
Some words appear only as responses but not as cues. For these words, forward associative strength is not available. We will drop these words.
In other words, our targeted responses (e.g., 'apple') were words that were used as cues in creating association norms (e.g., 'apple' was given as a cue word).
Accordingly, cue-response matrix's indexes are same as in columns.
"""

import pandas as pd
import os
import xlrd
import numpy as np
from tqdm import tqdm

# Run dataCleansing.sh and get cleansedStrength.csv
df = pd.read_csv('../Norms/AssociationNorms/cleansedStrength.csv', sep='\t')

mat_df = pd.read_excel('../SummaryTable/SummaryTable.xlsx', sheet_name = 'AllMaterials')
material_list = mat_df['MaterialFile']

all_words = []
for material_name in material_list:
    current_material_name = '../Materials/' + material_name

    book = xlrd.open_workbook(current_material_name)
    sheet_names = book.sheet_names()

    print(current_material_name)

    if 'similar' in sheet_names and 'dissimilar' in sheet_names:
        for sheet_name in ['similar', 'dissimilar']:
            selected_sheet = book.sheet_by_name(sheet_name)

            all_row_len = selected_sheet.nrows
            all_col_len = selected_sheet.ncols

            for col_n in range(all_col_len):
                for row_n in range(all_row_len):
                    all_words.append(selected_sheet.cell_value(row_n, col_n))

    elif 'group' in sheet_names:
        selected_sheet = book.sheet_by_name('group')
        all_row_len = selected_sheet.nrows
        all_col_len = selected_sheet.ncols

        for col_n in range(all_col_len):
            for row_n in range(all_row_len):
                all_words.append(selected_sheet.cell_value(row_n, col_n))

# Unique words
words_in_exps = sorted(list(set(all_words)))

# cue-response matrix construction
intersection_cues = sorted(list(set(df['cue']).intersection(set(words_in_exps))))

association_matrix = pd.DataFrame(np.zeros((len(intersection_cues), len(intersection_cues))))
association_matrix.index = intersection_cues
association_matrix.columns = intersection_cues

for cue_w in tqdm(intersection_cues):
    current_df = df.query('cue == @cue_w')
    for response_w in current_df['response']:
        if response_w in intersection_cues:
            response_match_df = current_df.query('response == @response_w')
            if len(response_match_df.index) != 0:
                association_matrix.loc[cue_w, response_w] = response_match_df.iat[0,4]

for n in range(len(association_matrix.index)):
    association_matrix.iat[n,n] = np.nan

association_matrix.to_csv('../Norms/AssociationNorms/association_matrix.csv')

print(association_matrix.describe())

print('Unique word count in experiments: {0}\nOut of {0}, {1} are in Norms as CUES\nNorms coverage: {2}'.format(
    len(words_in_exps),
    len(intersection_cues),
    len(intersection_cues) / len(words_in_exps)))
