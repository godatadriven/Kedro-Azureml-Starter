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

{% if cookiecutter.include_iris_example == "True" +%}

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

### Run locally
A nice feature of this template is that your pipelines run both locally and on AzureML. 
However, if some of your steps store data in Azure Blob Storage, ensure you have to ensure that you set up the correct credentials (see the  Reading and writing intermediate data to Azure Blob Storage section). 
To run your pipeline locally, use the command:

```bash
kedro run
```

### Run on AzureML
In this project, we use the [kedro-azureml](https://kedro-azureml.readthedocs.io/) plugin to automatically translate our kedro pipelines to AzureML pipelines.
Therefor, we don't need to write any AzureML specific code.
We only need to run `kedro azureml run`.
However, before we can do this, we first need to create a docker based environment for AzureML. 


#### Environment preparation
AzureML runs our code inside a Docker container. 
This container must contain our Python version and all the dependencies needed to run our code. 
This container does not need to contain our code because AzureML will copy and upload all our code every time we submit a job, and this ensures that we are always running the latest version of our code.

Before creating our environment, you need to log in to Azure, and the Azure Container Registry (ACR) connected to your AzureML workspace.
You can do this using the following commands:

```bash
az login
az acr login --name {{cookiecutter.azureml_container_registry_name}}
```

Now, we can create our environment.
Creating an environment is a three-step process:
1. Build the Docker image: The `Dockefile` in this project contains all the necessary steps.
2. Push the Docker image to the ACR: This is done using the `docker push` command.
3. Create the AzureML environment: This is done using the `az ml environment create` command.

You do this using the following command:

```bash
docker build -t {{cookiecutter.azureml_container_registry_name}}.azurecr.io/kedro-base-image/{{cookiecutter.azureml_environment_name}}:latest . \
docker push {{cookiecutter.azureml_container_registry_name}}.azurecr.io/kedro-base-image/{{cookiecutter.azureml_environment_name}}:latest && \
az ml environment create \
  --name {{cookiecutter.azureml_environment_name}} \
  --image {{cookiecutter.azureml_container_registry_name}}.azurecr.io/kedro-base-image/{{cookiecutter.azureml_environment_name}}:latest \
  --workspace-name {{ cookiecutter.azureml_workspace_name }} \
  --resource-group {{ cookiecutter.azureml_resource_group }}
```
Note: AzureML expects `linux/amd64` based images. That is why we added `--platform linux/amd64` docker file.
As a result, building the image might take a while if you use a M1 Mac.

#### Submitting 
When you have created your environment, you can submit your pipeline to AzureML.
All you need to do is run the command below and the [kedro-azureml](https://kedro-azureml.readthedocs.io/) plugin will take care of the rest.
The plugin 

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

### Optional: Reading and writing intermediate data to Azure Blob Storage

Kedro projects typically store their (intermediate) results using the data [engineering convention](https://kedro.readthedocs.io/en/stable/faq/faq.html#what-is-data-engineering-convention).
The big advantage of this convention is that you easily reuse these (intermediate) results in other pipeline steps.
In Kedro, this is typically done by using the `catalog.yml` file.
For example, if a pipeline produces a pickled model, you can store that in `data/06_models/model.pkl` by adding the following line to your `catalog.yml` file:

```yaml
model:
  type: pickle.PickleDataSet # This tells kedro to store the data as a pickle file
  filepath: kedro/06_models/model.pickle" # This tells kedro where to store the data on the local file system
  backend: pickle # alternative: joblib
```

This will store the model on the local file system.
Of course, saving files to the local file system is not very useful when running in the cloud.
Luckily, kedro allows you to store these intermediate results in other places, like Azure Blob Storage.
Before we can do this, we need to set up the credentials for Azure Blob Storage.
This can be done by adding the following lines to your `conf/local/credentials.yml` file:

```yaml
azure_storage:
  account_name: <YOUR_AZURE_STORAGE_ACCOUNT_NAME>
  account_key: <YOUR_AZURE_STORAGE_ACCOUNT_KEY>
```

Now, all you need to do is change your `catalog.yml` to the following, and it will store the data in your Azure Blob Storage instead of the local file system:

```yaml
model:
  type: pickle.PickleDataSet
  filepath: abfs://<CONTAINER_NAME>/06_models/model.pickle" # This tells kedro where to store the data on your Azure Blob Storage
  backend: pickle
  credentials: azure_storage # This tells kedro to use the `azure_storage` from the `credentials.yml` file
```

The big advantage of this is that you can now cache and reuse your intermediate results both locally and in the cloud.
For example, if all your data is stored in Azure Blob Storage, you run a part of your pipeline locally using the following:
```bash
kedro run --from-nodes=<YOUR_STARTING_NODE>
```

In AzureML, you do the something but only at pipeline level instead of node level:

```bash
kedro azureml run --pipeline "YOUR_PIPELINE_NAME"
```

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