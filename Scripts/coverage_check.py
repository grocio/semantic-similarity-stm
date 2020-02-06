from grocio_utils import *
import pandas as pd
import xlrd
from pprint import pprint

print(affect_df.head())
associ_df = pd.read_csv(ASSOCIATION_NROMS_PATH)
print(associ_df.head())


strength_df = pd.read_csv('../Norms/AssociationNorms/cleansedStrength.csv', sep='\t')

df = pd.read_excel('../SummaryTable/SummaryTable.xlsx', sheet_name = 'AllMaterials')
material_list = df['MaterialFile']

all_words = []
dict_chan = {}

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
all_words = list(set(all_words))
all_words_count = len(all_words)
print('all_words count:', all_words_count)

print('Not Available words in Affective norms')
avl_affect = 0
out_affect_words = []

for w in all_words:
    if w in list(affect_df['Word']):
        avl_affect += 1
    else:
        out_affect_words.append(w)

for i, word in enumerate(out_affect_words, 1):
    print('{:03} {}'.format(i, word))

print('available:{}, all:{}'.format(avl_affect, all_words_count))
print('Coverage:', avl_affect / all_words_count)

print('Not Available words in Association norms')
avl_associ = 0
out_asso_words = []
for w in all_words:
    if (w in list(strength_df['cue'])) or (w in list(strength_df['response'])):
        avl_associ += 1
    else:
        out_asso_words.append(w)
print('available:{}, all:{}'.format(avl_associ, all_words_count))
print('Coverage:', avl_associ / all_words_count)
for i, word in enumerate(out_asso_words, 1):
    print('{:03} {}'.format(i, word))
