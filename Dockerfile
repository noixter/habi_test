FROM python:3.10-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app

# Simulate the virtual environment
ENV VIRTUAL_ENV=/usr/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r /app/search_properties/requirements.txt


CMD ["pytest", "--cov=.", "--cov-report", "term-missing", "-s"]
