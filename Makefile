.PHONY: all install installmecab installdic installgrongish docker clean zip test

all:

PREFIX:=$(CURDIR)

install: installmecab installgrongish

mecab.tar.gz: 
	curl -fsSL "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE" -o mecab.tar.gz

mecab-0.996: mecab.tar.gz
	tar zxfv mecab.tar.gz

installmecab: mecab-0.996
	cd mecab-0.996 && ./configure --prefix=$(PREFIX) --enable-utf8-only && make && make check && make install

Grongish.tar.gz:
	curl -fsSL "https://github.com/shogo82148/Grongish/releases/download/v0.0.3/Grongish.tar.gz" -o Grongish.tar.gz

installgrongish: Grongish.tar.gz
	tar zxvf Grongish.tar.gz
	rm Grongish.tar.gz
	rm -rf ./togrongishdic
	rm -rf ./fromgrongishdic
	mv Grongish/* .
	rmdir Grongish
	export PATH=$(PREFIX)/bin:$$PATH; pip install -t $(PREFIX) -r requirements.txt

docker:
	mkdir -p grongish-server
	cp Makefile grongish-server/
	cp requirements.txt grongish-server/
	cp lambda_function.py grongish-server/
	docker run -v "$(CURDIR)/grongish-server":/var/task lambci/lambda:build-python3.6 make install

zip: docker
	cd grongish-server && \
	zip -9 -r ../grongish-server.zip . \
	-x mecab-0.996\* -x mecab.tar.gz -x mecab-ipadic-2.7.0-20070801\* \
	-x mecab-ipadic.tar.gz -x Grongish.tar.gz -x bin\* -x libexec\* -x share\* -x include/* \
	-x mecab_python-0.996-py2.7.egg-info/* -x mecab_python3-0.7-py2.7.egg-info/* -x jctconv-0.1.2-py2.7.egg-info/* \
	-x Makefile -x *.pyc

test: docker
	docker run -v "$(PWD)/grongish-server":/var/task lambci/lambda:python3.6 lambda_function.lambda_handler '{"text":"お前のにおいがリントどもを誘ったのだ"}'

clean:
	-rm -rf grongish-server
	-rm grongish-server.zip
