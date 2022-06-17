FROM python:3.10.0a7-slim-buster

COPY . /

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org" && \
    pip install setuptools==58.1.0 wheel==0.37.1

RUN python setup.py bdist_wheel

RUN pip install dist/*