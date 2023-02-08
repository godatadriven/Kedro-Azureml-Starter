FROM --platform=linux/amd64 python:{{cookiecutter.python_version|string}}-slim

# install project requirements
COPY src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt && rm -f /tmp/requirements.txt