import os
import shutil


def main() -> None:
    include_iris_example = "{{ cookiecutter.include_iris_example }}".strip() in [
        "yes",
        "True",
    ]

    if not include_iris_example:
        shutil.rmtree("src/{{ cookiecutter.python_package }}/pipelines/iris_example")
        os.remove("conf/base/parameters/iris_example.yml")
        os.remove("data/01_raw/iris.csv")


if __name__ == "__main__":
    main()
