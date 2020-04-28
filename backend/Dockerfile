FROM python:3.8.2
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir backend
WORKDIR backend
COPY r.txt /backend
RUN pip install -r r.txt
COPY . /backend
WORKDIR backend