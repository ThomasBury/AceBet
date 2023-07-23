import pandas as pd

def prepare_data():
    """
    Prepare the ATP data for modeling.

    Returns
    -------
    df : pandas.DataFrame
        The prepared data.

    """

    data = pd.read_csv("../data/atp_data.csv", low_memory=False)
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values('Date', inplace=True)

    df = data.copy()
    df.columns = df.columns.str.lower()
    df.rename(columns={'wrank': 'rank_p1',
                       'lrank': 'rank_p2',
                       'wsets': 'sets_p1',
                       'lsets': 'sets_p2',
                       'psw': 'ps_p1',
                       'psl': 'ps_p2',
                       'b365w': 'b365_p1',
                       'b365l': 'b365_p2'},
              inplace=True)
    df.columns = df.columns.str.lower()
    df.rename(columns=lambda x: x.replace('winner', 'p1').replace('loser', 'p2'), inplace=True)

    p1_columns = df.filter(like='p1').columns
    p2_columns = df.filter(like='p2').columns

    mask = df.index % 2 == 1
    df.loc[mask, p1_columns], df.loc[mask, p2_columns] = df.loc[mask, p2_columns].values, df.loc[mask, p1_columns].values
    df.loc[mask, "proba_elo"] = 1 - df.loc[mask, "proba_elo"].values

    df['target'] = ~mask
    # some naive feature engineering
    # Extract year, month, and day into separate columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['rank_diff'] = df['rank_p1'] - df['rank_p2']

    # this column is forbidden, 
    # to illustrate data leakage leading to 98% accuracy
    #df["p1_won_more_sets"] = 1*(df['sets_p1'] > df['sets_p2'])

    df['best_ranked'] = 'p1'
    df.loc[df['rank_diff'] > 0, 'best_ranked'] = 'p2'

    # write the "production" data
    df.to_feather("../data/atp_data_production.csv", low_memory=False)

