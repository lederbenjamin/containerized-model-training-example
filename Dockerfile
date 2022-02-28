FROM python:3.6-stretch

RUN apt-get update -y && apt-get install -y  \
    gnupg2  \
    libgpgme-dev  \
    swig

COPY pyproject.toml poetry.lock is_ready.sh train.py text_classifier.py /
COPY gnupg /gnupg/

RUN pip install --upgrade pip \
  && pip install poetry  \
  && poetry config virtualenvs.create false  \
  && poetry install --no-root --no-dev

CMD [ "python", "./train.py" ]