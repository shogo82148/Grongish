.PHONY: all install installmecab installdic installgrongish docker clean zip test

MECAB_VERSION=0.996.11
RUNTIME_VERSION=3.13
GRONGISH_VERSION=0.0.5

all:

PREFIX:=$(CURDIR)

install: installmecab installgrongish

installmecab:
	curl -o /tmp/mecab.tar.gz -sSL "https://github.com/shogo82148/mecab/releases/download/v$(MECAB_VERSION)/mecab-$(MECAB_VERSION).tar.gz"
	cd /tmp && tar zxfv mecab.tar.gz
	cd "/tmp/mecab-$(MECAB_VERSION)" && ./configure --prefix=$(PREFIX) --enable-utf8-only && make && make install

	curl -o /tmp/mecab-python.tar.gz -sSL "https://github.com/shogo82148/mecab/releases/download/v$(MECAB_VERSION)/mecab-python-$(MECAB_VERSION).tar.gz"
	cd /tmp && tar zxfv mecab-python.tar.gz
	export PATH=$(PREFIX)/bin:$$PATH && export PYTHONPATH=$(PREFIX) && cd "/tmp/mecab-python-$(MECAB_VERSION)" && python -m pip install . --target $(PREFIX)

installgrongish:
	curl -o /tmp/Grongish.tar.gz -fsSL "https://github.com/shogo82148/Grongish/releases/download/v$(GRONGISH_VERSION)/Grongish.tar.gz"
	cd /tmp && tar zxvf Grongish.tar.gz
	cp -r /tmp/Grongish/* .

docker:
	rm -rf grongish-server
	mkdir -p grongish-server
	cp Makefile grongish-server/
	cp lambda_function.py grongish-server/
	docker run -v "$(CURDIR)/grongish-server":/var/task ghcr.io/shogo82148/lambda-python:build-$(RUNTIME_VERSION)-x86_64 make install

zip:
	cd grongish-server && \
	zip -9 -r ../grongish-server.zip . \
	-x Makefile -x *.pyc

test:
	docker run -v "$(PWD)/grongish-server":/var/task ghcr.io/shogo82148/lambda-python:$(RUNTIME_VERSION)-x86_64 lambda_function.lambda_handler '{"text":"お前のにおいがリントどもを誘ったのだ"}'

clean:
	-rm -rf grongish-server
	-rm grongish-server.zip
