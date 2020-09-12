FROM python:3.8.3
USER root

WORKDIR /bot

ADD main.py /bot
ADD bot.py /bot
ADD lib /bot/lib
ADD cogs /bot/cogs

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "main.py"]
