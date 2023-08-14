import pandas as pd
import sklearn
from pathlib import Path
from joblib import load

def load_data(data_file):
    """
    Load the data from a feather file.

    Parameters
    ----------
    data_file : str
        The path to the data file.

    Returns
    -------
    df : pandas.DataFrame
        The loaded data.

    """

    try:
        # Read data from a feather file and convert the 'date' column to datetime format.
        df = pd.read_feather(data_file)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        # Raise an error if the specified data file is not found.
        raise FileNotFoundError(f"Data file '{data_file}' not found. Please check the file path.")
    except Exception as e:
        # Raise an error for any other loading-related exceptions.
        raise ValueError(f"Error occurred while loading data: {e}")

def query_data(df, p1_name, p2_name, date):
    """
    Query the data by player name and date.

    Parameters
    ----------
    df : pd.DataFrame
        The data to query.
    p1_name : str
        The name of player 1.
    p2_name : str
        The name of player 2.
    date : str
        The date of the match in 'YYYY-MM-DD' format.

    Returns
    -------
    df : pandas.DataFrame
        The data for the specified players and date.

    """

    try:
        # Query the DataFrame based on player names and date, handling both player order possibilities.
        query = f'(p1 == "{p1_name}" and p2 == "{p2_name}" and date == "{date}")' \
                f' or (p1 == "{p2_name}" and p2 == "{p1_name}" and date == "{date}")'
        return df.query(query)
    except KeyError:
        # Raise an error if the required columns are not present in the DataFrame.
        raise KeyError("Invalid column names in the data.")
    except Exception as e:
        # Raise an error for any other query-related exceptions.
        raise ValueError(f"Error occurred while querying data: {e}")

def predict(model, df):
    """
    Predict the probability and outcome (class) for the given data.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        The model to use for prediction.
    df : pandas.DataFrame
        The data to predict.

    Returns
    -------
    prob : float
        The probability of player 1 winning.
    class_ : int
        The class of the prediction (0 or 1).

    """
    # Create a list of predictors by excluding non-predictive columns.
    predictors = df.columns.drop(['target', 'date', 'sets_p1', 'sets_p2', 'b365_p1', 'b365_p2', 'ps_p1', 'ps_p2'])
    X = df[predictors].copy()
    try:
        # Use the trained model to predict the probability and class.
        prob = model.predict_proba(X)[:, 1]
        class_ = model.predict(X)
        return prob, class_, X["p1"].values[0]
    except Exception as e:
        # Raise an error if any prediction-related exceptions occur.
        raise ValueError(f"Error occurred during prediction: {e}")
    
def load_model(model_path):
    """
    Load the most recent model from a directory.

    Parameters
    ----------
    model_path : str
        The path to the directory containing the model files.

    Returns
    -------
    model : sklearn.base.BaseEstimator
        The loaded most recent model.

    """

    # Get a list of model files, identify the most recent one, and load the model.
    model_files = [file for file in Path(model_path).glob("model_*.joblib")]
    most_recent_model_file = max(model_files, key=lambda file: file.stat().st_mtime)
    return load(most_recent_model_file)

def make_prediction(data_file, model_path, p1_name, p2_name, date):
    """
    Load the model, load the data, query the data by player name and date, predict the probability and outcome (class).

    Parameters
    ----------
    data_file : str
        The path to the data file.
    model_path : str
        The path to the directory containing the model files.
    p1_name : str
        The name of player 1.
    p2_name : str
        The name of player 2.
    date : str
        The date of the match in 'YYYY-MM-DD' format.

    Returns
    -------
    prob : float
        The probability of player 1 winning.
    class_ : int
        The class of the prediction (0 or 1).

    """

    try:
        # Load the data, model, query data by player name and date, and make predictions.
        df = load_data(data_file)
        model = load_model(model_path)
        df_filtered = query_data(df, p1_name, p2_name, date)
        prob, class_, player_1 = predict(model, df_filtered)
        return prob, class_, player_1
    except Exception as e:
        # Print an error message and return None for prediction in case of exceptions.
        print(f"Error occurred: {e}")
        return None, None



# if __name__ == "__main__":
#     # Specify the correct paths to the data file and model directory
#     data_file = Path(__file__).resolve().parents[2] / 'data' / 'atp_data_production.feather'
#     model_path = Path(__file__).resolve().parents[2] 
#     prob, class_, player_1 = make_prediction(data_file=data_file, model_path=model_path, p2_name="Fognini F.", p1_name="Jarry N.", date="2018-03-04")
#     print(f"Winning probability of {player_1} is {100*prob[0]:.1f} %")