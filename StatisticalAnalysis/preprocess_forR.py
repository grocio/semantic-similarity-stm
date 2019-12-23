import pandas as pd
import numpy as np
import pyper

# csvs
TARGET_FILES = ['results_SerialRecall',
                'results_SerialReconstruction'] #,
                # 'results_ItemCorrect',
                # 'results_OrderError']

def results_integrator(df):
    results_df = df
    
    for IntegKey in set(df['Integration']):
        if not pd.isnull(IntegKey):
            current_df = df[df['Integration'] == IntegKey]

            weights = current_df['IntegrationWeight'] / sum(current_df['IntegrationWeight'])

            mean_Sim = np.sum(weights * current_df['Sim'])
            mean_Dsim = np.sum(weights * current_df['Dsim'])
            mean_Aso = np.sum(weights * current_df['Aso'])
            mean_Unaso = np.sum(weights * current_df['Unaso'])

            # dzs should be the same across the rows in the current df
            # This is true for directions
            integ_dz = current_df['dz'].iloc[0]
            integ_direction = current_df['Direction'].iloc[0]
            integ_N = current_df['N'].iloc[0]
            integ_title = current_df['Title'].iloc[0]
            integ_material_file = current_df['MaterialFile'].iloc[0]
            integ_list_length = current_df['ListLength'].iloc[0]
            integ_study = current_df['Study'].iloc[0]
            integ_statistics = current_df['Statistics'].iloc[0]
            integ_design = current_df['Design'].iloc[0]

            # Since Index of IntegKey does not exist, it append a new row
            results_df.loc[IntegKey, 'Sim'] = mean_Sim
            results_df.loc[IntegKey, 'Dsim'] = mean_Dsim
            results_df.loc[IntegKey, 'Aso'] = mean_Aso
            results_df.loc[IntegKey, 'Unaso'] = mean_Unaso

            results_df.loc[IntegKey, 'Study'] = integ_study
            results_df.loc[IntegKey, 'N'] = integ_N
            results_df.loc[IntegKey, 'dz'] = integ_dz
            results_df.loc[IntegKey, 'Direction'] = integ_direction
            results_df.loc[IntegKey, 'Title'] = integ_title
            results_df.loc[IntegKey, 'MaterialFile'] = integ_material_file
            results_df.loc[IntegKey, 'ListLength'] = integ_list_length
            results_df.loc[IntegKey, 'Statistics'] = integ_statistics
            results_df.loc[IntegKey, 'Design'] = integ_design

            results_df.loc[IntegKey, 'Status'] = 'Integrated several results'

    return results_df


if __name__ == '__main__':
    """
    XYZ_IntegratedResults.csv file containes single rows of an experiment or
    integrated results (drops original data of experiments to be integrated)

    XYZ_forRegression.csv file only contains experiments with
    a) dirrection is reported
    b) Within subject design
    """

    for f in TARGET_FILES:
        df = pd.read_csv('../Results/{}.csv'.format(f), index_col = 0)
        results_integrator(df)

        df = df[pd.isna(df['Integration'])]
        
        df = df.sort_values('Study')

        df.to_csv('./{}_preprocessed.csv'.format(f))

        """
        direction_checker = []
        for item in df['Direction']:
            if str(item) == 'unclear':
                direction_checker.append(False)
            else:
                direction_checker.append(True)

        df = df[direction_checker]

        design_checker = []
        for i in range(len(df['N'])):
            item_N = str(df['N'].iloc[i])
            if item_N.startswith('Between'):
                design_checker.append(False)
            else:
                design_checker.append(True)

        df = df[design_checker]

        df.to_csv('./{}_preprocessed.csv'.format(f))
        """
