FROM python:3

RUN apt-get -o Acquire::Max-FutureTime=86400 update

RUN apt-get install -y ffmpeg
RUN pip install discord.py youtube_dl asyncio PyNaCl ffmpeg ffmpeg-python

WORKDIR /app

ADD src/app.py /app

CMD [ "python", "./app.py" ]