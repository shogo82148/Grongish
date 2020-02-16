.PHONY: all install installmecab installdic installgrongish docker clean zip test

MECAB_VERSION=0.996.2
RUNTIME_VERSION=python3.8
GRONGISH_VERSION=0.0.3

all:

PREFIX:=$(CURDIR)

install: installmecab installgrongish

installmecab:
	curl -o /tmp/mecab.tar.gz -sSL "https://github.com/shogo82148/mecab/releases/download/v$(MECAB_VERSION)/mecab-$(MECAB_VERSION).tar.gz"
	cd /tmp && tar zxfv mecab.tar.gz
	cd "/tmp/mecab-$(MECAB_VERSION)" && ./configure --prefix=$(CURDIR) --enable-utf8-only && make && make install

installgrongish:
	curl -o /tmp/Grongish.tar.gz -fsSL "https://github.com/shogo82148/Grongish/releases/download/v$(GRONGISH_VERSION)/Grongish.tar.gz"
	cd /tmp && tar zxvf Grongish.tar.gz
	cp -r /tmp/Grongish/* .
	export PATH=$(PREFIX)/bin:$$PATH; pip install -t $(PREFIX) -r requirements.txt

docker:
	mkdir -p grongish-server
	cp Makefile grongish-server/
	cp requirements.txt grongish-server/
	cp lambda_function.py grongish-server/
	docker run -v "$(CURDIR)/grongish-server":/var/task lambci/lambda:build-$(RUNTIME_VERSION) make install

zip: docker
	cd grongish-server && \
	zip -9 -r ../grongish-server.zip . \
	-x Makefile -x *.pyc

test: docker
	docker run -v "$(PWD)/grongish-server":/var/task lambci/lambda:$(RUNTIME_VERSION) lambda_function.lambda_handler '{"text":"お前のにおいがリントどもを誘ったのだ"}'

clean:
	-rm -rf grongish-server
	-rm grongish-server.zip
