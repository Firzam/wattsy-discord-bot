FROM python

RUN python -m ensurepip --upgrade

COPY . .

RUN python -m pip install -r requirements.txt

CMD [ "python", "main.py" ]