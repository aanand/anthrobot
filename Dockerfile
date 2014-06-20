FROM aanand/numpy:2.7-1.8.1

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD requirements-dev.txt /code/requirements-dev.txt
RUN pip install -r requirements-dev.txt

ADD . /code
