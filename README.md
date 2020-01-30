# flask-wiki
Simple file based wiki for Flask

## developpement

- clone the repo
- pipenv sync
- pipenv run pip install -e .
- cd examples; pipenv run serve
- go to http://localhost:5000/wiki

## tips

- do not forget to add a header with title and tags if you edit your md file by hand

## config

- WIKI_HOME: markdown root file (default: home)
- WIKI_URL_PREFIX: blueprint prefix (default: /demo)
- WIKI_CONTENT_DIR: markdown files location (default: ./data)
- WIKI_UPLOAD_FOLDER: files location such as images, pdf, etc (default: ./data/files)