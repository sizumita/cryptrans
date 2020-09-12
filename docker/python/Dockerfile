FROM python:3.8.3
USER root

WORKDIR /bot

ADD requirements.txt /bot

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ADD main.py /bot
ADD bot.py /bot
ADD lib /bot/lib
ADD cogs /bot/cogs

CMD ["python", "main.py"]
