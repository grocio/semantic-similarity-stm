import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

def half_up_round(i, n_digits):
    return Decimal(i).quantize(Decimal(n_digits), rounding=ROUND_HALF_UP)

target_li = ['results_SerialReconstruction_preprocessed',
             'results_SerialRecall_preprocessed',
             'results_ItemCorrect_preprocessed',
             'results_OrderErrors_preprocessed']

for f in target_li:
    df = pd.read_csv('./{}.csv'.format(f), index_col = 0)

    SMS = df['Dsim'] - df['Sim']
    CD = df['CONSim'] - df['CONDsim']
    SMSw2v = df['W2VSim'] - df['W2VDsim']

    df['SMS'] = [half_up_round(i, '0.01') for i in SMS]
    df['CD'] = [half_up_round(i, '0.001') for i in CD]
    df['SMSw2v'] = [half_up_round(i, '0.01') for i in SMSw2v]

    new_N = []
    for i in df['N']:
        if type(i) == float:
            new_N.append(int(i))
        else:
            new_N.append(i)

    df['N'] = new_N

    new_Direction = []
    for i in df['Direction']:
        if type(i) == float:
            new_Direction.append(int(i))
        else:
            new_Direction.append(i)

    df['Direction'] = new_Direction

    df = df[['Study', 'SMS', 'SMSw2v', 'CD', 'Direction', 'Statistics', 'Design', 'N', 'Set']]
    file_stem = f.strip("preprocessed").strip("results")
    df.to_csv('../Fig_Table/TABLE{}.csv'.format(file_stem), index=False)
