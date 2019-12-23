import pandas as pd
import os
import xlrd
import numpy as np
import grocio_utils as gutl

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

    # test = []
    if 'similar' in sheet_names and 'dissimilar' in sheet_names:
        for sheet_name in ['similar', 'dissimilar']:
            selected_sheet = book.sheet_by_name(sheet_name)

            all_row_len = selected_sheet.nrows
            all_col_len = selected_sheet.ncols

            for col_n in range(all_col_len):
                for row_n in range(all_row_len):
                    all_words.append(selected_sheet.cell_value(row_n, col_n))
                    # test.append(selected_sheet.cell_value(row_n, col_n))

    elif 'group' in sheet_names:
        selected_sheet = book.sheet_by_name('group')
        all_row_len = selected_sheet.nrows
        all_col_len = selected_sheet.ncols

        for col_n in range(all_col_len):
            for row_n in range(all_row_len):
                all_words.append(selected_sheet.cell_value(row_n, col_n))
                # test.append(selected_sheet.cell_value(row_n, col_n))

    # dict_chan[current_material_name] = test

# Unique words
words_in_exps = sorted(list(set(all_words)))

df = df[df['cue'].isin(words_in_exps)]
df = df[df['response'].isin(words_in_exps)]

association_matrix = pd.DataFrame(np.zeros((len(words_in_exps), len(words_in_exps))))
association_matrix.columns = words_in_exps
association_matrix.index = words_in_exps

for cue in words_in_exps:
    current_df = df[df['cue'] == cue]
    for response in current_df['response']:
        association_matrix.loc[cue, response] = current_df[current_df['response'] == response].iloc[0,4]

association_matrix.to_csv('../Norms/AssociationNorms/association_matrix.csv')

print(len(words_in_exps))
print(association_matrix.describe())
# print(association_matrix)
