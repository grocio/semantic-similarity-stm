from grocio_utils import *
from pprint import pprint
from scipy.spatial import distance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

AFFECT_NORMS_PATH = '../Norms/AffectiveNorms/BRM-emot-submit.csv'

sim_li = ["diamond", "emerald", "opal", "pearl", "ruby", "sapphire"]
dsim_li = ["diamond", "aunt", "iron", "captain", "cat", "bishop"]

affect_df = pd.read_csv(AFFECT_NORMS_PATH, index_col=0)

def li_to_fig(li, f_name):
    df = words2affect_df(li)
    df.reset_index(inplace=True) # Reset index. Otherwise, indexed from 0 to about 14000!

    print(df)
    print('Centroid:', affective_centroid(df))
    print('Distance From Centroid:', dists_from_centroid(li))
    print('Mean Distance:', np.mean(dists_from_centroid(li)))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    ax.set_xlabel("V")
    ax.set_ylabel("A")
    ax.set_zlabel("D")

    ax.set_xlim3d(left=1, right=9)
    ax.set_ylim3d(bottom=1, top=9)
    ax.set_zlim3d(bottom=1, top=9)

    # plots on 3-dimensional space
    for i in range(len(df['V.Mean.Sum'])):
        ax.plot([df['V.Mean.Sum'][i]], [df['A.Mean.Sum'][i]], [df['D.Mean.Sum'][i]],
                marker='${}$'.format(df['Word'][i][:3]), color='black', linestyle='None', markersize=15)

    # plots on 2-dimensional planes
    ax.plot(df['V.Mean.Sum'], df['A.Mean.Sum'], [1 for i in range(len(df['V.Mean.Sum']))],
            marker='o', color='black', linestyle='None', markersize=5)
    ax.plot(df['V.Mean.Sum'], [9 for i in range(len(df['V.Mean.Sum']))], df['D.Mean.Sum'],
            marker='o', color='black', linestyle='None', markersize=5)
    ax.plot([1 for i in range(len(df['V.Mean.Sum']))], df['A.Mean.Sum'], df['D.Mean.Sum'],
            marker='o', color='black', linestyle='None', markersize=5)

    bbox = fig.bbox_inches.from_bounds(0.05,-0.05,6.7,4.7)
    plt.savefig('../Fig_Table/Fig{}.png'.format(f_name), bbox_inches=bbox)
    plt.close()

li_to_fig(sim_li, 'Tse_sim')
li_to_fig(dsim_li, 'Tse_dsim')
