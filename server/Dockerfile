FROM python:latest

RUN curl -fsSL "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE" -o mecab.tar.gz \
    && tar zxfv mecab.tar.gz \
    && cd mecab-0.996 \
    && ./configure --enable-utf8-only \
    && make && make check && make install && ldconfig \
    && cd .. \
    && rm -rf mecab-0.996 && rm mecab.tar.gz \
    && curl -fsSL "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM" -o mecab-ipadic.tar.gz \
    && tar zxfv mecab-ipadic.tar.gz \
    && cd mecab-ipadic-2.7.0-20070801 \
    && ./configure --with-charset=utf8 \
    && make && make install \
    && cd .. \
    && rm -rf mecab-ipadic-2.7.0-20070801 && rm mecab-ipadic.tar.gz

RUN curl -fsSL "https://github.com/shogo82148/Grongish/releases/download/v0.0.1/Grongish.tar.gz" -o Grongish.tar.gz && tar zxvf Grongish.tar.gz && rm Grongish.tar.gz
WORKDIR /Grongish
COPY gunicorn-server-starter.sh /Grongish/
COPY server.py /Grongish/
RUN pip install jctconv gunicorn mecab-python3 pyramid

CMD ["./gunicorn-server-starter.sh"]