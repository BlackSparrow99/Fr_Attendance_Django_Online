# To run the project you must have install

Python = Latest version (python 3.11 or later version).
Conda = Latest version.
Visual Studio 2022 = Latest version with c++ build tools.
CMake = Latest build.

Ensure all the installation requirements is included in System Environment Variable.

Then run this commands:

conda env create -f environment.yml
conda activate py311_env
pip install -r requirements.txt

The environment.yml and requirements.txt contains all nessaccary packages to run this project

To run the project run this command:
python manage.py runserver
