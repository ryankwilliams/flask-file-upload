FROM python:2
ADD . /app
WORKDIR /app
RUN pip install -r requirements/app.txt
EXPOSE 5000
CMD python app/app.py