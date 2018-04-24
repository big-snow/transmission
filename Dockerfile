FROM resin/rpi-raspbian

RUN apt-get update && apt-get install -y \
    python \
    python-pip \
    transmission-daemon \
    transmission-cli \

    && pip install --upgrade \ 
    pip \
    google-api-python-client \
    httplib2 \

    && apt-get clean \

    && rm -rf /var/lib/apt/lists/* \

    && ln -s /etc/transmission-daemon/ ./ 

ADD transmission-daemon /transmission-daemon
ADD transmission-with-drive ./transmission-with-drive

VOLUME ./transmission-with-drive/download

CMD /etc/init.d/transmission-daemon start \
    && watch -n 60 python /transmission-with-drive/run.py
