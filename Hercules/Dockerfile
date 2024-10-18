FROM python:3.12-alpine

WORKDIR /app

COPY CustomModules ./CustomModules
COPY *.py .
COPY requirements.txt .
COPY watermark.lua .

ENV TERM=xterm
ENV PYTHONUNBUFFERED=1

ARG TARGETPLATFORM
ARG BUILD_DATE
ARG COMMIT

RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libc-dev linux-headers rust cargo g++ && \
    apk add git lua5.4-dev luarocks5.4 && \
    ln -s /usr/bin/luarocks-5.4 /usr/bin/luarocks && \
    luarocks install luacheck && \
    git clone "https://github.com/zeusssz/hercules-obfuscator.git" Obfuscator && \
    mv watermark.lua Obfuscator/src/modules && \
    python -m pip install --upgrade pip && \
    pip install --upgrade setuptools wheel && \
    pip install -r requirements.txt && \
    apk del .build-deps && \
    find /usr/local \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' + && \
    rm -rf /root/.cache/pip

LABEL maintainer="Discord: piko.piko.no.mi (970119359840284743)" \
      commit=$COMMIT \
      description="Hercules Bot for obfuscating lua files." \
      release=$BUILD_DATE \
      VERSION="1.2.2" \
      url="https://gitlab.bloodygang.com/Serpensin/Hercules"

CMD ["python3", "main.py"]
