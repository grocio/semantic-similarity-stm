import pandas as pd

target_li = ['results_SerialReconstruction_preprocessed',
             'results_SerialRecall_preprocessed']

for f in target_li:
    df = pd.read_csv('./{}.csv'.format(f), index_col = 0)

    SMS = df['Dsim'] - df['Sim']
    CD = df['Aso'] - df['Unaso']

    df['SMS'] = SMS
    df['CD'] = CD

    df = df[['Study', 'SMS', 'CD', 'Direction', 'Statistics', 'Design', 'N']]
    file_stem = f.strip("preprocessed").strip("results")
    df.to_csv('./TABLE{}.csv'.format(file_stem))
