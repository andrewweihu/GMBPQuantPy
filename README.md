# GMBPQuantPy

GMBP Python Quant Repository

## Directory Structure

<pre>

/gmbp_quant       <= top level for module import, e.g. import gmbp_quant.**.**
|
|--/apps          <= top level job & app entry points go here
|--/dal           <= data access layer functionalities for internal data access like DB
|--/dpl           <= data pipeline functionalities for external data access like APIs
|--/epa           <=
|--/factor        <=
|--/mdpalgo       <=
|--/research      <= research functionalities go here
|--/signal        <=
/notebook         <= research or presentation notebooks go here
/runtime_env/env  <= scripts and Python runtime environment yml files(with versioning) go here
|
|--/linux         <= Linux Python runtime environment yml files
|--/windows       <= Windows Python runtime environment yml files
|--/macOS         <= macOS Python runtime environment yml files
/test             <= all test cases where pytest can collect go here, similar folder structure as in "gmbp_quant"
pip.conf          <= configuration of our own pypi server that hosts our own Python packages, such as "gmbp-common"
                     pip will go to pypi.org to find packages first. If pip couldn't find a package from pypi.org, then
                     it will go to our own server to download that package.
requirements.txt  <= shows requirement for packages for our Python environment. pip will install missing packages for
                     you. Please add the package into this file if your code requires a new package.

</pre>

## Set up PYTHONPATH (for Linus/MacOS)
1. add the following command to the file ~/.bash_profile, so that your system can recognize Python paths
   (you can also replace ${pwd} with ${YOUR_GMBPQuantPy_DIR} explicitly if you like.):
```export PYTHONPATH="${PYTHONPATH}:${pwd}"```
2. run ```source ~/.bash_profile``` to activate it.

## Python Runtime Environment Management

### conda Installation and Setup

1. Please install the latest version of Miniconda or Anaconda from Anaconda official website.
   Make sure Python version >= 3.8.
2. Make sure conda's bin folder added into your PATH environment variables. 

### Setup "gmbp_quant" Python Runtime Environment

* Steps to set up a Python virtual environments (Linux/macOS):
````console
1. python -m venv ~/.envs/gmbp-quant
2. cd ~/.envs/gmbp-quant/
3. conda deactivate
4. source bin/activate
5. cd ${YOUR_GMBPQuantPy_DIR}
6. export PIP_CONFIG_FILE=pip.conf     
7. pip install -r requirements.txt 
````
Repeat step 2-7 again after requirements.txt is updated.

## Run All Tests From Command Line
````console
cd ${YOUR_GMBPQuantPy_DIR}
pytest test
````

