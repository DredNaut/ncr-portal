FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY ncr_portal ./
COPY ncr_portal_client.py ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./ncr_portal" ]
