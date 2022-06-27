#python -m venv ./venv
#source ./venv/Scripts/activate  # or run venv/Scripts/activate.bat on windows 
#pip install jinja2-cli

jinja2 capabilitiesToPython.j2 capabilities.json --format=json > capabilities.py