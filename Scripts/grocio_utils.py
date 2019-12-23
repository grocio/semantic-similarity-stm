import sys

sys.path.append('../../Manuscript/')

import random as rnd
import xlrd
from pprint import pprint
import pandas as pd
import numpy as np
from scipy.spatial import distance
import itertools
from tqdm import tqdm
import csv
from datetime import datetime

# SETTING
AFFECT_NORMS_PATH = '../Norms/AffectiveNorms/BRM-emot-submit.csv'
ASSOCIATION_NROMS_PATH = '../Norms/AssociationNorms/association_matrix.csv' #Preprocessed data
MATERIAL_PATH = '../Materials/'
ITERATION_N = 10000 # 10000

affect_df = pd.read_csv(AFFECT_NORMS_PATH)

def words2affect_df(word_li):
    """
    Return a dataframe of word, valence, arousal, and dominance.
    Takes a word list and a dataframe of affective norms.
    Words that do not exist in the affective norms are omitted.
    """
    _affect_df = affect_df[['Word','V.Mean.Sum','A.Mean.Sum','D.Mean.Sum']]
    _affect_df = _affect_df[_affect_df['Word'].isin(word_li)]

    return _affect_df

def affective_centroid(a_df):
    """
    Calculate the centroid of a given list in terms of affective dimensions.
    It takes a dataframe and returns a tuple, (mean_valence, mean_arousal, mean_dominance).
    """
    length = len(a_df['Word'])

    # N should be greater than or equal to 2
    if length < 2:
        return np.nan

    else:
        centroid = (np.nanmean(a_df['V.Mean.Sum']),
                    np.nanmean(a_df['A.Mean.Sum']),
                    np.nanmean(a_df['D.Mean.Sum']))

        return centroid

def dists_from_centroid(word_li, dist_func=distance.euclidean):
    """
    Return a list of distances between each words and the centroid.
    It takes a list of words. By default, it uses euclidean distance calculation.
    Use dist_func option for another distance. For example, dist_func = distance.cityblock works.
    """
    current_df = words2affect_df(word_li)
    centroid = affective_centroid(current_df)

    # Centroid cannot be canculated
    if len(current_df['Word']) < 2:
        return [np.nan]

    else:
        dist_li = []
        for i in range(len(current_df['Word'])):
            three_dim_val = tuple(current_df.iloc[i, j] for j in range(1,4))
            dist_li.append(dist_func(centroid, three_dim_val))
        return dist_li

def materials2lists(f_name, row_len_set=None):
    """
    Takes an xlsx file (path) and returns similar and disimilar lists.

    Note that a list length might not be the same as the row number.
    For example, 8 words belong to a category but 6 out of 8 words might have been used in an experiment.
    Set row_len_set = 6 in that situation.

    Two kinds of xlsx files are assumed.
    1) Book with similar sheet & dissimilar sheet
        corresponding fixed similar lists vs. fixed dissimilar lists
    2) Book with group sheet
        corresponding categorically and/or associatively grouped lists vs. randomized lists
    """
    iter_n = ITERATION_N

    sim_mld_li = []
    dsim_mld_li = []

    book = xlrd.open_workbook(f_name)
    sheet_names = book.sheet_names()

    if 'similar' in sheet_names and 'dissimilar' in sheet_names:
        for sheet_name in ['similar', 'dissimilar']:
            selected_sheet = book.sheet_by_name(sheet_name)

            all_row_len = selected_sheet.nrows
            all_col_len = selected_sheet.ncols

            if all_row_len == row_len_set:
                row_len_set = None

            if row_len_set == None:
                for col_n in range(all_col_len):
                    one_col = []
                    for row_n in range(all_row_len):
                        one_col.append(selected_sheet.cell_value(row_n,col_n))
                    if sheet_name == 'similar':
                        sim_mld_li.append(one_col)
                    else:
                        dsim_mld_li.append(one_col)

            # Custom list length
            else:
                for col_n in range(all_col_len):
                    # All combinations are calculated
                    # nCm, where n = all_row_len, m = row_len_set
                    for a_combi in itertools.combinations(range(all_row_len), row_len_set):
                        one_col = []
                        for row_n in a_combi:
                            one_col.append(selected_sheet.cell_value(row_n,col_n))
                        if sheet_name == 'similar':
                            sim_mld_li.append(one_col)
                        else:
                            dsim_mld_li.append(one_col)

    elif 'group' in sheet_names:
        selected_sheet = book.sheet_by_name('group')

        all_row_len = selected_sheet.nrows
        all_col_len = selected_sheet.ncols

        if all_row_len == row_len_set:
            row_len_set = None

        # For similar lists, the procedure is the same as in the above
        if row_len_set == None:
            for col_n in range(all_col_len):
                one_col = []
                for row_n in range(all_row_len):
                    one_col.append(selected_sheet.cell_value(row_n,col_n))
                sim_mld_li.append(one_col)
        else:
            for col_n in range(all_col_len):
                for a_combi in itertools.combinations(range(all_row_len), row_len_set):
                    one_col = []
                    for row_n in a_combi:
                        one_col.append(selected_sheet.cell_value(row_n,col_n))
                    sim_mld_li.append(one_col)

        # Creating dissimilar list based on grouped lists
        # It takes some time. Thus, it shows a progress bar
        if row_len_set == None:
            for run_n in tqdm(range(iter_n), desc = 'Randomized Lists Creation: {}'.format(f_name)):
                one_col = []

                # N different groups are selected without replacement
                col_ns = rnd.sample(range(all_col_len), all_row_len)
                # As different groups are selected with replacement, repetition of the same row number is OK
                row_ns = rnd.choices(range(all_row_len), k=all_row_len)

                for i in range(all_row_len):
                    one_col.append(selected_sheet.cell_value(row_ns[i],col_ns[i]))
                dsim_mld_li.append(one_col)

        else:
            for run_n in tqdm(range(iter_n), desc = 'Randomized Lists Creation: {}'.format(f_name)):
                one_col = []

                col_ns = rnd.sample(range(all_col_len), row_len_set) # all_row_len in the above block
                row_ns = rnd.choices(range(all_row_len), k=row_len_set)

                for i in range(row_len_set):
                    one_col.append(selected_sheet.cell_value(row_ns[i],col_ns[i]))
                dsim_mld_li.append(one_col)

    else:
        print('WARNING\n{} does not have similar/dissimilar or group sheet'.format(f_name))

    return sim_mld_li, dsim_mld_li


def intersection_li_cueres(exp_li, df_col_names):
    """
    It returns a nested list of lists of intersections of two lists.
    For calculation of connectivity (cue-response associative strength),
    Simply, dropping items of a list that are missing in the cue-response matrix
    """
    intersection_li  = []

    for li in exp_li:
        intersect_li = [item for item in li if item in df_col_names]
        intersection_li.append(intersect_li)

    return intersection_li

def connectivity4fixed_lists(cueres_df, file_name_path, sheet_name):
    """
    Calculate mean associative strength for a similar or dissimilar sheet.
    For grouped sheets, use connectivity4grouped_lists.
    """
    print('Connectivity Calculation {}: {}'.format(sheet_name, file_name_path))

    associ_columns = cueres_df.columns

    book = xlrd.open_workbook(file_name_path)
    selected_sheet = book.sheet_by_name(sheet_name)

    all_row_len = selected_sheet.nrows
    all_col_len = selected_sheet.ncols

    mean_by_lists = []

    for col_n in range(all_col_len):
        one_col = []
        for row_n in range(all_row_len):
            one_col.append(selected_sheet.cell_value(row_n,col_n))

        current_cols = set(one_col) & set(associ_columns)
        current_cols = list(current_cols)
        current_df = cueres_df.loc[current_cols, current_cols]

        # print(file_name_path, current_df)
        length = len(current_df)

        if length > 1:
            diag_elems = [current_df.iloc[i, i] for i in range(length)]
            diag_sum = np.nansum(diag_elems)
            all_sum = sum(current_df.sum())
            mean_by_one_list = (all_sum - diag_sum) / (length * length - length)
        else:
            mean_by_one_list = np.nan

        mean_by_lists.append(mean_by_one_list)

    # print('mean by lists:', np.nanmean(mean_by_lists))
    return np.nanmean(mean_by_lists)

def connectivity4grouped_lists(cueres_df, multi_li):
    """
    Calculate mean associative strength of a given list.
    It takes cue-response probability matrix (DataFrame) and nested list of lists of words.
    Nested list is a list of lists of grouped words NOT randomized list.
    """

    df_col_names = cueres_df.columns
    # When df contains the all words of multi_li, intercections_li_cueres is redundant.
    inter_multi = intersection_li_cueres(multi_li, df_col_names)
    # print(inter_multi)
    flatten_words = sum(inter_multi, [])

    grouped_strengths = []
    grouped_simple_sums = []
    grouped_li_lengths = []

    for li in tqdm(inter_multi, 'Connectivity Calculation by Groups'):
        # Create DataFrame that contains words of li
        current_df = cueres_df.loc[li, li]
        length = len(current_df)

        # Note. Diagonal elements should be dropped: e.g., a pair of Cue - Response, Banana - Banana, is innapropriate.
        # Sum of diagonal elements are calculated, which is used to subtrast from the sum
        diag_elems = [current_df.iloc[j, j] for j in range(length)]
        diag_sum = np.nansum(diag_elems)

        if length > 1:
            grouped_li_lengths.append(length)
            grouped_simple_sums.append(sum(current_df.sum()))

            #print('diag sum:', diag_sum)
            #print('all sum:', sum(current_df.sum()))

            grouped_strengths.append((sum(current_df.sum()) - diag_sum) / (length * length - length)) # Append a scalar to the list

        elif length == 1:
            grouped_li_lengths.append(length)
            grouped_simple_sums.append(current_df.iloc[0,0])

    # Ungrouped_strength = mean(All strengths - each strength of grouped list)
    all_df = cueres_df.loc[flatten_words, flatten_words]
    all_length = len(all_df)

    if all_length**2 - sum([i**2 for i in grouped_li_lengths]) == 0: # When a matrix contains only cells for grouped words
        print('Warning: all_length is {}, grouped_li_lengths is {}\nThis is quite unlikely\nInspect data\n'.format(all_length, grouped_li_lengths))
        pprint(all_df)
        ungrouped_strength = np.nan
    else:
        ungrouped_strength = (sum(all_df.sum()) - sum(grouped_simple_sums)) / \
            (all_length**2 - sum([i**2 for i in grouped_li_lengths]) )

    return np.nanmean(grouped_strengths), ungrouped_strength

def materials4groupedlist(f_name):
    """
    It transforms a sheet to a simple multidimensional list for calculating connectivity
    For calculatiing connectivity, randomized lists are not necessary
    """
    book = xlrd.open_workbook(f_name)
    sheet_names = book.sheet_names()

    multi_li = []

    if 'group' in sheet_names:
        selected_sheet = book.sheet_by_name('group')

        all_row_len = selected_sheet.nrows
        all_col_len = selected_sheet.ncols

        multi_li = []

        for col_n in range(all_col_len):
            one_col = []
            for row_n in range(all_row_len):
                one_col.append(selected_sheet.cell_value(row_n,col_n))
            multi_li.append(one_col)

    else:
        print('WARNING\n{} does not have a group sheet'.format(f_name))

    return multi_li

def similarity_connectivity_calc(excel_book, sheet_name, material_path = MATERIAL_PATH, name_option=None):
    """
    It takes a summary table of experiments,
    calculating similarity and connectivity for each experiment.
    """

    df = pd.read_excel(excel_book, sheet_name = sheet_name)

    material_list = df['MaterialFile']
    length_list = df['ListLength']

    material_length_pairs = [(material_list[i], length_list[i]) for i in range(len(material_list))]

    # Similarity
    for i in range(len(material_list)):
        if not material_length_pairs[i] in material_length_pairs[:i]:
            current_material_file = material_path + material_list[i]
            sim_mld, dsim_mld = materials2lists(f_name = current_material_file,
                                                row_len_set = length_list[i])
            sim_mean_dists = []
            dsim_mean_dists = []

            for one_sim_li in tqdm(sim_mld, desc = 'Similarity Calculation Sim: {}'.format(current_material_file)):
                word_affect_df = words2affect_df(one_sim_li)
                if len(word_affect_df['Word']) > 1:
                    sim_mean_dists.append(np.nanmean(dists_from_centroid(one_sim_li)))

            for one_dsim_li in tqdm(dsim_mld, desc = 'Similarity Calculation Dsim: {}'.format(current_material_file)):
                word_affect_df = words2affect_df(one_dsim_li)
                if len(word_affect_df['Word']) > 1:
                    dsim_mean_dists.append(np.nanmean(dists_from_centroid(one_dsim_li)))

            sim_mean_mean = np.nanmean(sim_mean_dists)
            dsim_mean_mean = np.nanmean(dsim_mean_dists)

            # CHECK_UP
            # print( material_list[i], sim_mean_dists, sim_mean_mean)
            # print( material_list[i], dsim_mean_dists, dsim_mean_mean)

            df.loc[i,'Sim'] = sim_mean_mean
            df.loc[i,'Dsim'] = dsim_mean_mean

        else: # calculation for the material & length pair has been done
            print('Skipped {}'.format(material_list[i]))
            where_pair = material_length_pairs.index(material_length_pairs[i])

            df.loc[i,'Sim'] = df.loc[where_pair, 'Sim']
            df.loc[i,'Dsim'] = df.loc[where_pair, 'Dsim']

    print('Similarity Done')

    # Connectivity, which is based on material, ignoring length
    association_df = pd.read_csv(ASSOCIATION_NROMS_PATH, index_col=0)

    material_list = list(material_list)

    for i in range(len(material_list)):
        if not material_list[i] in material_list[:i]:
            file_name_path = MATERIAL_PATH + material_list[i]
            book = xlrd.open_workbook(file_name_path)
            sheet_names = book.sheet_names()

            if 'group' in sheet_names:
                material_multili = materials4groupedlist(file_name_path)
                aso, unaso = connectivity4grouped_lists(association_df, material_multili)
            elif 'similar' in sheet_names and 'dissimilar' in sheet_names:
                aso = connectivity4fixed_lists(association_df, file_name_path, 'similar')
                unaso = connectivity4fixed_lists(association_df, file_name_path, 'dissimilar')

            df.loc[i, 'Aso'] = aso
            df.loc[i, 'Unaso'] = unaso

        else: # calculation for the material & length pair has been done
            print('Skipped {}'.format(material_list[i]))
            where_material = material_list.index(material_list[i])

            df.loc[i,'Aso'] = df.loc[where_material, 'Aso']
            df.loc[i,'Unaso'] = df.loc[where_material, 'Unaso']

    print('Connectivity Done')

    # Process AdditionalKey

    if name_option != None:
        df.to_csv('../Results/results_{}_{}.csv'.format(sheet_name, name_option))
    else:
        df.to_csv('../Results/results_{}.csv'.format(sheet_name))
