import pandas as pd
from pathlib import Path
from joblib import load


def query_data(p1_name, p2_name, date):
    """
    Query the data by player name and date.

    Parameters
    ----------
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

    # Assuming df contains the loaded DataFrame
    try:
        df = pd.read_feather("../data/atp_data_production.csv")
        df['date'] = pd.to_datetime(df['date'])
        df = df.query('p1 == @p1_name and p2 == @p2_name and date == @date or p2 == @p1_name and p1 == @p2_name and date == @date')
        return df
    except FileNotFoundError:
        raise FileNotFoundError("Data file not found. Please check the file path.")
    except KeyError:
        raise KeyError("Invalid column names in the data file.")
    except ValueError:
        raise ValueError("Invalid date format or data types in the data file.")


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

    try:
        prob = model.predict_proba(df)[:, 1]
        class_ = model.predict(df)
        return prob, class_
    except ValueError:
        raise ValueError("Inconsistent data types or dimensions for prediction.")


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

    try:
        model_files = [file for file in Path(model_path).glob("model_*.joblib")]
        most_recent_model_file = max(model_files, key=lambda file: file.stat().st_mtime)
        return load(most_recent_model_file)
    except FileNotFoundError:
        raise FileNotFoundError("No model files found in the specified directory.")
    except ValueError:
        raise ValueError("Invalid model files in the specified directory.")


def make_prediction(p1_name, p2_name, date):
    """
    Load the model, query the data by player name and date, predict the probability and outcome (class).

    Parameters
    ----------
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
        model = load_model("../data/models/")
        df = query_data(p1_name, p2_name, date)
        prob, class_ = predict(model, df)
        return prob, class_
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None
