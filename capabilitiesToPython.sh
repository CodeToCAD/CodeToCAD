#python -m venv ./venv
#pip install jinja2-cli
#source ./venv/Scripts/activate  # or run activate.bat on windows 

jinja2 capabilitiesToPython.j2 capabilities.json --format=json > capabilities.py