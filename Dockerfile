FROM python:3.10

WORKDIR /smashing-downloader

COPY . .
RUN mkdir "wallpapers"

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["bash"]