FROM python:3.10

WORKDIR /home/app/

COPY ./app ./

RUN set -ex; \
    pip install --no-cache-dir --upgrade pip; \
    pip install --no-cache-dir -r requirements.txt; \
    pip cache purge

EXPOSE 8080

CMD ["python","-u", "app.py"]

