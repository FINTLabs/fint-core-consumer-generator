# fint-core-consumer-generator
This project generates a Core 2 consumer based on the user's input of domain and package. It accomplishes this by scraping the information model website for the specified version, ensuring that all information is up-to-date.

## How to generate a consumer
- Install Python 3 on your machine if you haven't already.
- Open a terminal or command prompt and navigate to the root directory of the fint-core-consumer-generator project
- Run the main.py script with Python 3 by typing `python3 main.py` into your terminal or command prompt.
- Follow the prompts to provide the necessary information such as domain, package, and version number.
- Once the script has completed, the generated consumer will be available in the output folder of the project.

## Input folders
If the user wishes to customize some of the generated files, they can navigate to the input folder and make changes as necessary. This folder is organized into different sub-folders with specific purposes:

- `static:` Contains static elements that are not generated but are common across all consumers, such as workflow files or a .gitignore file.
- `base:` Contains files that are generated in the root of the project.
- `config:` Contains files that are generated in the config folder.
- `model:` Contains files that are generated for each unique model scraped from the information model website.
- `kustomize:` Contains files for kustomization.

By modifying these files, users can tailor the generated consumer to their specific needs.

## Beware
The generated code may not be consistent across all resources, as not all methods are identical. Therefore, we recommend building the consumer locally and making any necessary changes before publishing.
