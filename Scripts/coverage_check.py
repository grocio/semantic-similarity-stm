from grocio_utils import *
import pandas as pd
import xlrd
from pprint import pprint
import gensim.downloader as api

# affect_df, association_df, word_vectors are loaded in grocio_utils

df = pd.read_excel('../SummaryTable/SummaryTable.xlsx', sheet_name = 'AllMaterials')
material_list = df['MaterialFile']

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

# Unique words
all_words = set(all_words)
all_words_count = len(all_words)

print('all_words count:', all_words_count)
#print('all words', all_words)

print('@@@ SEMANTIC NORMS @@@')
print('Not Available words in Semantic norms')
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

print('@@@ ASSOCIATION NORMS @@@')
print('Not Available words in Association norms')
avl_associ = 0
out_asso_words = []
for w in all_words:
    if w in list(association_df.index):
        avl_associ += 1
    else:
        out_asso_words.append(w)
print('available:{}, all:{}'.format(avl_associ, all_words_count))
print('Coverage:', avl_associ / all_words_count)
for i, word in enumerate(out_asso_words, 1):
    print('{:03} {}'.format(i, word))

print('@@@ word2vec @@@')
print('Not Available words in word2vec')
avl_word2vec = 0
out_word2vec_words = []
for w in all_words:
    if w in word_vectors:
        avl_word2vec += 1
    else:
        out_word2vec_words.append(w)
print('available:{}, all:{}'.format(avl_word2vec, all_words_count))
print('Coverage:', avl_word2vec / all_words_count)
for i, word in enumerate(out_word2vec_words, 1):
    print('{:03} {}'.format(i, word))
