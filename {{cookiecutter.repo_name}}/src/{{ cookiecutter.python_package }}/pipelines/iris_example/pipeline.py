"""
This is a boilerplate pipeline 'iris_example'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline
from {{ cookiecutter.python_package }}.pipelines.iris_example.nodes import (
    evaluate_model,
    split_data,
    train_model,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["iris_data", "params:iris_dataset"],
                outputs=["data_train", "data_test"],
                name="split_data",
            ),
            node(
                func=train_model,
                inputs=["data_train", "params:model"],
                outputs="model",
                name="make_predictions",
            ),
            node(
                func=evaluate_model,
                inputs=["model", "data_test"],
                outputs=None,
                name="report_accuracy",
            ),
        ]
    )
