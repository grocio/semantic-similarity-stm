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
import gensim.downloader as api

# SETTING
AFFECT_NORMS_PATH = '../Norms/AffectiveNorms/BRM-emot-submit.csv'
ASSOCIATION_NROMS_PATH = '../Norms/AssociationNorms/association_matrix.csv'
MATERIAL_PATH = '../Materials/'
ITERATION_N = 10000 # For random list creation
TRAINED_DATA = "word2vec-google-news-300" #word2vec model

affect_df = pd.read_csv(AFFECT_NORMS_PATH)
print('LOADED affect norms')


word_vectors = api.load(TRAINED_DATA)
print('LOADED word2vec vectors')

association_df = pd.read_csv(ASSOCIATION_NROMS_PATH, index_col=0)
print('LOADED association norms')

cues_in_norms = set(association_df.index)

def cos_sim(v1, v2):
    """
    Calculate cosine similarity.
    If vector's length == 0, it returns np.nan.
    """
    if (len(v1) == 0) or (len(v2) == 0):
        return np.nan
    else:
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def word2vec_sim_cal(word_li):
    """
    Return mean cosine similarity for a list of several words.
    """
    result = []
    list_length = len(word_li)

    for i in range(list_length):
        for j in range(list_length):
            if i < j:
                if word_li[i] in word_vectors and word_li[j] in word_vectors:
                    result.append(word_vectors.similarity(word_li[i], word_li[j]))

    if result != []:
        return np.nanmean(result)
    else:
        return np.nan

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
    # Otherwise the centroid == 0 or one word's point
    if length < 2:
        return np.nan
    else:
        centroid = (np.nanmean(a_df['V.Mean.Sum']),
                    np.nanmean(a_df['A.Mean.Sum']),
                    np.nanmean(a_df['D.Mean.Sum']))

        return centroid

def mean_dist_from_centroid(word_li, dist_func=distance.euclidean):
    """
    Return mean disttance from centroid for a list.
    It takes a list of words. By default, it uses euclidean distance calculation.
    Use dist_func option for another distance. For example, dist_func = distance.cityblock works.
    """
    current_df = words2affect_df(word_li)
    centroid = affective_centroid(current_df)

    # Centroid cannot be canculated when a list's length < 2
    if len(current_df['Word']) < 2:
        return np.nan
    else:
        dist_li = []
        for i in range(len(current_df['Word'])):
            three_dim_val = tuple(current_df.iloc[i, j] for j in range(1,4))
            dist_li.append(dist_func(centroid, three_dim_val))
        return np.nanmean(dist_li)

def connectivity_calc(word_li):
    """
    Return mean associative strength for a list (i.e., connectivity).
    """
    word_candidate = set(word_li).intersection(cues_in_norms)
    return np.nanmean(association_df.loc[word_candidate, word_candidate].to_numpy())

def materials2lists(f_name, row_len_set):
    """
    Takes an xlsx file (path) and returns similar and disimilar lists.

    Note that a list length might not be the same as the row number.
    For example, 8 words belong to a category but 6 out of 8 words might have been used in an experiment.
    Set row_len_set = 6 in that situation.

    Two kinds of xlsx files are assumed.
    a) Book with similar sheet & dissimilar sheet
        corresponding fixed similar lists vs. fixed dissimilar lists
    b) Book with group sheet
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

            # When all_row_len == row_len_set
            # e.g., 8 rows in materials and 8 words in a list in the experiment
            if all_row_len == row_len_set:
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

        # For similar lists, the procedure is the same as in the above
        if all_row_len == row_len_set:
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
        # It takes some time. So, it shows a progress bar
        if all_row_len == row_len_set:
            for run_n in tqdm(range(iter_n), desc = 'Randomized Lists Creation: {}'.format(f_name), position=1):
                one_col = []

                # N different groups are selected without replacement
                # N = all_row_len
                col_ns = rnd.sample(range(all_col_len), all_row_len)

                # N rows are slected
                # As different groups are selected with replacement, repetition of the same row number is OK
                row_ns = rnd.choices(range(all_row_len), k=all_row_len)

                for i in range(all_row_len):
                    one_col.append(selected_sheet.cell_value(row_ns[i],col_ns[i]))
                dsim_mld_li.append(one_col)
        else:
            for run_n in tqdm(range(iter_n), desc = 'Randomized Lists Creation: {}'.format(f_name), position=1):
                one_col = []

                # all_row len != row_len_set
                # N = row_len_set
                col_ns = rnd.sample(range(all_col_len), row_len_set) # all_row_len in the above block
                row_ns = rnd.choices(range(all_row_len), k=row_len_set)

                for i in range(row_len_set):
                    one_col.append(selected_sheet.cell_value(row_ns[i],col_ns[i]))
                dsim_mld_li.append(one_col)

    else:
        print('WARNING\n{} does not have similar/dissimilar or group sheets'.format(f_name))

    return sim_mld_li, dsim_mld_li

def similarity_connectivity_calc(summary_book, sheet_name, material_path = MATERIAL_PATH, name_option=None):
    """
    It takes a summary table of experiments,
    calculating similarity and connectivity for each experiment.
    """

    summary_df = pd.read_excel(summary_book, sheet_name = sheet_name)

    material_list = summary_df['MaterialFile']
    length_list = summary_df['ListLength']

    material_length_pairs = [(material_list[i], length_list[i]) for i in range(len(material_list))]

    # Similarity
    for i in tqdm(range(len(material_list)), desc ='Study', position=0):
        # First check materila_length_pairs
        # If a pair of material X and length Y has been calculated, calculation will be skipped
        if not material_length_pairs[i] in material_length_pairs[:i]:
            current_material_file = material_path + material_list[i]
            sim_mld, dsim_mld = materials2lists(f_name = current_material_file,
                                                row_len_set = length_list[i])
            sim_mean_li = []
            dsim_mean_li = []

            sim_w2v_li = []
            dsim_w2v_li = []

            sim_connec_li = []
            dsim_connec_li = []

            for one_sim_li in tqdm(sim_mld, desc = 'Calculation for sim lists: {}'.format(current_material_file), position=1):
                # Similarity
                sim_mean_li.append(mean_dist_from_centroid(one_sim_li))
                # word2vec similarity
                sim_w2v_li.append(word2vec_sim_cal(one_sim_li))
                # connectivity
                sim_connec_li.append(connectivity_calc(one_sim_li))

            for one_dsim_li in tqdm(dsim_mld, desc = 'Calculation for dsim lists: {}'.format(current_material_file), position=1):
                # Similarity
                dsim_mean_li.append(mean_dist_from_centroid(one_dsim_li))
                # word2vec similarity
                dsim_w2v_li.append(word2vec_sim_cal(one_dsim_li))
                # connectivity
                dsim_connec_li.append(connectivity_calc(one_dsim_li))

            summary_df.loc[i,'Sim'] = np.nanmean(sim_mean_li)
            summary_df.loc[i,'Dsim'] = np.nanmean(dsim_mean_li)

            summary_df.loc[i, 'W2VSim'] = np.nanmean(sim_w2v_li)
            summary_df.loc[i, 'W2VDsim'] = np.nanmean(dsim_w2v_li)

            summary_df.loc[i, 'CONSim'] = np.nanmean(sim_connec_li)
            summary_df.loc[i, 'CONDsim'] = np.nanmean(dsim_connec_li)


        else: # calculation for the material & length pair has been done
            print('Skipped {}'.format(material_list[i]))
            where_pair = material_length_pairs.index(material_length_pairs[i])

            summary_df.loc[i,'Sim'] = summary_df.loc[where_pair, 'Sim']
            summary_df.loc[i,'Dsim'] = summary_df.loc[where_pair, 'Dsim']

            summary_df.loc[i,'W2VSim'] = summary_df.loc[where_pair, 'W2VSim']
            summary_df.loc[i,'W2VDsim'] = summary_df.loc[where_pair, 'W2VDsim']

            summary_df.loc[i, 'CONSim'] = summary_df.loc[where_pair, 'CONSim']
            summary_df.loc[i, 'CONDsim'] = summary_df.loc[where_pair, 'CONDsim']

    # Process AdditionalKey
    if name_option != None:
        summary_df.to_csv('../Results/results_{}_{}.csv'.format(sheet_name, name_option))
    else:
        summary_df.to_csv('../Results/results_{}.csv'.format(sheet_name))
