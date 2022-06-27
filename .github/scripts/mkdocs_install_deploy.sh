#!/bin/sh

# Activating virtual environment
. /opt/venv/bin/activate

# Install mkdocs dependencies
pip install mkdocs==1.3.0 mkdocs-material==8.3.8 mkdocstrings==0.18.1

# Render website
mkdocs gh-deploy