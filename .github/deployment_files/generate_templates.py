from string import Template

import requests


# Get the latest version from Github
results = requests.get("https://api.github.com/repos/NearBeach/NearBeach/releases?page=1&per_page=1")
results_json = results.json()

# Using the results, find the tag name (aka version)
version = results_json[0]['tag_name']

# Create the __init__.py file
with open('./.github/deployment_files/template__init__.txt', 'r') as input_file:
    src = Template(input_file.read())
    result = src.substitute({'version': version})
    input_file.close()

    with open('./NearBeach/__init__.py', 'w') as output_file:
        output_file.write(result)
        output_file.close()

# Create the pyproject.toml file
with open('./.github/deployment_files/template_pyproject.toml', 'r') as input_file:
    src = Template(input_file.read())
    result = src.substitute({'version': version})
    input_file.close()

    with open('./pyproject.toml', 'w') as output_file:
        output_file.write(result)
        output_file.close()

