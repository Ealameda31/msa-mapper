#!/bin/sh

# Activating virtual environment
. /opt/venv/bin/activate

# Install testing dependencies
pip install pytest==7.1.2 pytest-dependency==0.5.1

# Running python tests
cd msa_mapper && pytest