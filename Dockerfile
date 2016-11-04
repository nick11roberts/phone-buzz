FROM python:3.4
ENV PYTHONUNBUFFERED 1
MAINTAINER Nick Roberts "n3robert@ucsd.edu"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN export export FLASK_APP=routes.py
ENTRYPOINT ["python"]
CMD ["routes.py"]
