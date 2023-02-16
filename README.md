# Kedro Azureml Starter
This repo is a starter template for a Kedro project that can run its pipelines both locally and on AzureML.
To run on AzureML pipelines, we use the [kedro-azureml](https://kedro-azureml.readthedocs.io/) plugin.
This plugin automatically translates your Kedro pipeline into an AzureML pipeline:

Kedro pipeline             |  AzureML Pipeline
:-------------------------:|:-------------------------:
<img src="images/kedro_viz.jpg" width="450">  | <img src="images/azureml_viz.jpg"  width="450">

Quickly want to try this out? This starter can automatically generate the above pipeline for you. Just follow the instructions below. 

## Requirements for this starter
- Python 3.8+
- A terminal with the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) installed. 
- kedro >= 0.18.4. You can install kedro using [pipx](https://github.com/pypa/pipx), pip or conda:
```bash
pipx install kedro
```
or
```bash
python -m venv .venv
source .venv/bin/activate
pip install kedro
```
or
```bash
conda create -n kedro python=3.10
conda activate kedro
pip install kedro
```

## Starting a new kedro project
Before starting a new kedro project, make sure you have a Azure Machine Learning Workspace with a compute cluster.
The starter will ask you like:
- Your AzureML Workspace name.
- Your AzureML Workspace resource group.
- Your blob storage account name and container name. Here we will store the temporary files for the pipeline.
- Your AzureML compute cluster name. This will be the default compute cluster for your pipeline steps.
- Your Container Registry name.

When it has all the information, you can create the project with the following command:

```bash
kedro new \
  --starter=https://github.com/godatadriven/kedro-azureml-starter \
  --checkout main
```
All the remaining instructions will be in the generated README.md file.

## Using the starter
A nice feature of this template is that your pipelines run both locally and on AzureML.

### Running locally
Running locally works exactly the same as in a normal Kedro project:
```bash
kedro run
```
### Running on AzureML
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

You can do all these steps with the following command:
```bash
# Login to your Azure account
az login
# Login to your Container Registry
az acr login --name <your-container-registry-name>
# Build the docker image
docker build -t <your-container-registry-name>.azurecr.io/<your-image-name>:<your-image-tag> .
# Push the docker image to your Container Registry
docker push <your-container-registry-name>.azurecr.io/<your-image-name>:<your-image-tag>
# Register you docker images as an AzureML environment.
az ml environment create \
    --name <your-environment-name> \
    --image <your-container-registry-name>.azurecr.io/<your-image-name>:<your-image-tag>
    --workspace-name <your-azureml-workspace-name> \
    --resource-group <your-azureml-workspace-resource-group>
    ```
```

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

### Where can I find the names for all the resources?
You can find the names of all the resources in the [Azure Portal](https://portal.azure.com/).
Then, find your AzureML Workspace.
Here there should be an area called essentials.
This should contain all the needed information.

![AzureML Workspace](images/ml-workspace-resources.jpg)

### I have a ML Workspace, but I don't have a compute cluster. How can I create one?
Go to your [ML Workspace](https://ml.azure.com/).
When you are in your workspace, click on the compute tab in the left menu.
Then click on the button **compute cluster** tab (**not** the compute instance tab).
Click on the **+ New** button and follow the instructions.
