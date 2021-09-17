FROM python:3.8

ARG VERSION 

LABEL org.text-classification=$VERSION

COPY webapp/* /webapp/

RUN cd /webapp && unzip *.zip && rm *.zip

WORKDIR /webapp



RUN pip --default-timeout=1000 install -r requirements.txt 

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]