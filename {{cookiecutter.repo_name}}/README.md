# {{ cookiecutter.project_name }}

This is your new kedro project, which was generated using `Kedro {{ cookiecutter.kedro_version }}`.

## Usage guidelines
In order to get the most out of this template:
- Don't remove any of the generated lines in the `.gitignore` file.
- Don't commit data to git. 
- Don't commit any credentials or your local configuration to git. Keep all your credentials like API keys in `conf/local/credentials.yml` and they will be ignored by git.
- General AzureML resource information is stored in `conf/base/azureml.yml`. Git does not ignore this file, so you can share it with your team. If you are uncomfortable adding this file to git, you can move the file`conf/local`. Now, everything will still work, but git will ignore the file. However, you will need to generate the file manually for each new team member. So probably the best approach is to add the file to git while ensuring the repo remains private.


## Setup

### Create virtual environment
First, you need to create a virtual environment.
Make sure you have the same Python version as the one used to generate this project.
This project was generated using Python {{cookiecutter.python_version}}.
You are free to use any Virtual Environment tool you like.
However, be careful due to a bug in AzureML SDK, your `.venv` or `venv` can not be in the root directory of your project (the folder that contains `pyproject.toml`).

### Install dependencies
All the dependencies are listed in `requirements.txt`.
You can install them using `pip`:
```bash
pip install -r requirements.txt
```
If you need to add a new dependency, make sure to add it to `requirements.txt` because the Dockerfile uses this file to install the dependencies.

{% if cookiecutter.include_iris_example == "true" +%}

## Example pipeline
We have included an example pipeline that you can use to get started.
This example pipeline does the following:
1. It reads the Iris dataset from `data/01_raw/iris.csv`.
2. It splits the dataset into a training and test set.
3. It trains a model on the training set.
4. It evaluates the model on the test set.

You can find the pipeline in `src/{{ cookiecutter.python_package }}/pipelines/iris_example`.
The usage section contains more information on how to run and visualize the pipeline.

{% endif +%}

## Usage
A nice feature of this template is that your pipelines run both locally and on AzureML.

### Run locally
Running locally works exactly the same as in a normal Kedro project:

```bash
kedro run
```

### Run on AzureML
We use the [kedro-azureml plugin](https://kedro-azureml.readthedocs.io/) in this project to translate our Kedro pipelines to AzureML pipelines.
Therefore, we don't need to write any AzureML-specific code; we only need to run `kedro azureml run`.

#### Environment preparation
Before you can run your pipeline on AzureML, you need to create a docker-based environment. 
You only need to do this when your Python version or dependencies change because the command `kedro azureml run` will upload all your local files and mount them into the docker container.
Creating a docker-based environment consist of the following steps:
1. Login to your Azure account using the Azure CLI.
2. Login to your Container Registry using the Azure CLI.
3. Build the docker image using the generated `Dockerfile`.
4. Push the docker image to your Container Registry.
5. Register you docker images as an AzureML environment.

```bash
# Login to your Azure account
az login
# Login to your Container Registry
az acr login --name {{cookiecutter.azureml_container_registry_name}}
# Build the docker image
docker build -t {{cookiecutter.azureml_container_registry_name}}.azurecr.io/kedro-base-image/{{cookiecutter.azureml_environment_name}}:latest .
# Push the docker image to your Container Registry
docker push {{cookiecutter.azureml_container_registry_name}}.azurecr.io/kedro-base-image/{{cookiecutter.azureml_environment_name}}:latest
# Register you docker images as an AzureML environment.
az ml environment create \
  --name {{cookiecutter.azureml_environment_name}} \
  --image {{cookiecutter.azureml_container_registry_name}}.azurecr.io/kedro-base-image/{{cookiecutter.azureml_environment_name}}:latest \
  --workspace-name {{ cookiecutter.azureml_workspace_name }} \
  --resource-group {{ cookiecutter.azureml_resource_group }}
```
Note: AzureML expects `linux/amd64` based images. That is why we added the `--platform linux/amd64` flag in the docker file.
As a result, building the image might take a while if you use a M1 Mac.

#### Submitting 
After you have created your environment, you can submit your pipeline to AzureML using the following command:

```bash
kedro azureml run 
```

Optionally, you can give the plugin additional information like:
- `--subscription_id <YOUR_AZURE_SUBSCRIPTION_ID>`: The Azure subscription ID to use. If not specified,  Defaults to value store in the `AZURE_SUBSCRIPTION_ID` environment variable.
- `--pipeline_name <NAME>`: The name of the pipeline to run. If not specified, all pipelines will be run. This is useful if you only want to run a specific pipeline.
- ` --params <PARAMS_IN_JSON>`: The parameters to use for the pipeline. If not specified, the default parameters in `conf/base` or `conf/local` will be used. This is useful if you want to experiment with different (hyper)parameters.
- `--azureml_environment <YOUR_ENV_NAME>`: The name of the AzureML environment using the syntax `<environment_name>@latest` or `<environment-name>:<version>`. If not specified, the default environment will be used. This useful if you want to try out a newer version of your environment.
- `--wait-for-completion`: If specified, the command will wait until the run is completed. By default, the command will return immediately after the run is submitted.
- `--help`: Show the additional options.


## FAQ

### Kedro asks for my Azure Storage Account Key, where can I find this?
You can find your Azure Storage Account Key in the [Azure Portal](https://portal.azure.com/).
Then, search for your storage account.
When you are in the storage account, click on `Access keys` in the left menu.
Here, you can find your storage account key.

### Kedro keeps asking for my Azure Storage Account Key, this is annoying!
The `kedro azureml run` can automatically read your Azure Storage Account Key from the environment variable `AZURE_STORAGE_KEY`.
So, you can set this environment variable once, and then you don't have to enter your key every time you run `kedro azureml run`.
Or, you can provide your key using the `AZURE_STORAGE_KEY="..." kedro azureml run` option.


### How do I solve the `AssetException`: Error with code: [Errno 2] No such file or directory: ...
This is a known bug in the AzureML SDK. 
For some reason, it does not resolve symlinks correctly.
So, make sure there are no symlinks in your project directory.
Typically, this happens when you have a `.venv` or `venv` directory in the root of your project.
Simply moving the folder containing the symlink to a different location will solve the problem.

### How do I access pipeline step outputs if I run my pipeline in AzureML?
You can store any pipeline step output in an Azure Blob Storage Account.
To do this, you need to add the following lines to your `catalog.yml`:
```yaml
<your_step_output_name>:
  type: <your_type>
  filepath: abfs://<your_container_name>/<your_path>/<your_file_name>
  credentials: azure_storage
```
Kedro will also need to know your credentials to access the Azure Blob Storage Account.
Therefore, you need to add the following lines to your `credentials.yml`:
```yaml
azure_storage:
  account_name: <YOUR_AZURE_STORAGE_ACCOUNT_NAME>
  account_key: <YOUR_AZURE_STORAGE_ACCOUNT_KEY>
```
