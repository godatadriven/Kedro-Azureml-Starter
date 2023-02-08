"""
This is a boilerplate pipeline 'iris_example'
generated using Kedro {{ cookiecutter.kedro_version }}
"""
import logging
from typing import Any, Dict, Tuple

import mlflow
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def split_data(
    data: pd.DataFrame, parameters: Dict[str, Any]
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    data_train, data_test = train_test_split(
        data,
        test_size=parameters["test_size"],
        stratify=data["species"],
        random_state=parameters["random_state"],
    )

    return data_train, data_test


def train_model(
    data_train: pd.DataFrame, parameters: Dict[str, Any]
) -> LogisticRegression:
    x = data_train.drop("species", axis=1).to_numpy()
    y = data_train["species"]

    logger = logging.getLogger(__name__)

    for key, value in parameters.items():
        logger.info(f"Parameter {key}: {value}")
        mlflow.log_param(key, value)

    model = LogisticRegression(
        solver=parameters["solver"],
        C=parameters["C"],
        random_state=parameters["random_state"],
    )
    model.fit(x, y)

    accuracy = model.score(x, y)
    logging.info(f"Training Accuracy: {accuracy}")
    mlflow.log_metric("training/accuracy", accuracy)

    return model


def evaluate_model(
    model: LogisticRegression,
    data_test: pd.DataFrame,
) -> pd.DataFrame:
    x = data_test.drop("species", axis=1).to_numpy()
    y = data_test["species"]

    predictions = model.predict(x)
    accuracy = model.score(x, y)

    logger = logging.getLogger(__name__)
    logger.info(f"Test Accuracy: {accuracy}")
    mlflow.log_metric("test/accuracy", accuracy)

    return pd.DataFrame({"predictions": predictions, "y_true": y})
