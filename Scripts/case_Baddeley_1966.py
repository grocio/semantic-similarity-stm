from grocio_utils import *
from pprint import pprint
from scipy.spatial import distance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# the word, long is missing in the affective norms!

AFFECT_NORMS_PATH = '../Norms/AffectiveNorms/BRM-emot-submit.csv'

B5_sim, B5_dis = materials2lists(f_name='../Materials/Baddeley_1966a_Exp1.xlsx',
                                 row_len_set=5)
B10_sim, B10_dis = materials2lists(f_name='../Materials/Baddeley_1966b_Exp1.xlsx',
                                   row_len_set=10)

affect_df = pd.read_csv(AFFECT_NORMS_PATH, index_col=0)

"""
print(B5_sim[0], words2affect_df(B5_sim[0]))
print(B5_dis[0], words2affect_df(B5_dis[0]))
print(B10_sim[0], words2affect_df(B10_sim[0]))
print(B10_dis[0], words2affect_df(B10_dis[0]))
"""

B5_with_mean_distance_sim = []
for li in B5_sim:
    li_distance_item = (np.mean(dists_from_centroid(li)), li)
    B5_with_mean_distance_sim.append(li_distance_item)

B5_with_mean_distance_sim = sorted(B5_with_mean_distance_sim, key = lambda li:li[0])

B5_with_mean_distance_dis = []
for li in B5_dis:
    li_distance_item = (np.mean(dists_from_centroid(li)), li)
    B5_with_mean_distance_dis.append(li_distance_item)

B5_with_mean_distance_dis = sorted(B5_with_mean_distance_dis, key = lambda li:li[0])

B5_sim_vals = []
for i in range(len(B5_with_mean_distance_sim)):
    B5_sim_vals.append(B5_with_mean_distance_sim[i][0])

print('Mean:', np.mean(B5_sim_vals), '\n', 'sd:', np.std(B5_sim_vals))

B5_dis_vals = []
for i in range(len(B5_with_mean_distance_dis)):
    B5_dis_vals.append(B5_with_mean_distance_dis[i][0])

print('Mean:', np.mean(B5_dis_vals), '\n', 'sd:', np.std(B5_dis_vals))

print('B5 lens:', len(B5_sim_vals), len(B5_dis_vals))

print('B10 Sim Mean')
B10_sim_m = np.mean(dists_from_centroid(B10_sim[0]))
print(B10_sim_m, B10_sim[0])

print('B10 Dis Mean')
B10_dis_m = np.mean(dists_from_centroid(B10_dis[0]))
print(B10_dis_m, B10_dis[0])

sns.set()
sns.set_style('whitegrid')
bins = [0.75 + 0.25/2*i for i in range(16)]
sns.distplot(B5_sim_vals, kde=False,norm_hist=False, color='red', bins=bins)
sns.distplot(B5_dis_vals, kde=False, norm_hist=False, color='blue', bins=bins)
plt.xlabel('Mean distance from centroid')
plt.ylabel('Count')

plt.axvline(B10_sim_m, 0, 2, color='red', linestyle='--')
plt.axvline(B10_dis_m, 0, 2, color='blue', linestyle='--')

plt.savefig('../Fig_Table/FigDistributionBaddeley.png')
plt.close()
