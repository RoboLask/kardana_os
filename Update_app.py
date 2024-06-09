import os
import requests
import importlib.util

def download_file(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(response.content)

def import_and_run(filename):
    spec = importlib.util.spec_from_file_location("module.name", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()

# URL файла на GitHub
while True:
    url = ("https://raw.githubusercontent.com/RoboLask/kardana_os/main/kardana_pro_3.py")
    filename = 'kardana_pro_3.py'
    download_file(url, filename)
    print("Success!")
    break