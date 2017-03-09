.PHONY: all install installmecab installdic installgrongish docker clean zip test

all:

PREFIX:=$(CURDIR)

install: installmecab installdic installgrongish

mecab.tar.gz: 
	curl -fsSL "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE" -o mecab.tar.gz

mecab-0.996: mecab.tar.gz
	tar zxfv mecab.tar.gz

installmecab: mecab-0.996
	cd mecab-0.996 && ./configure --prefix=$(PREFIX) --enable-utf8-only && make && make check && make install


mecab-ipadic.tar.gz:
	curl -fsSL "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM" -o mecab-ipadic.tar.gz

mecab-ipadic-2.7.0-20070801: mecab-ipadic.tar.gz
	tar zxfv mecab-ipadic.tar.gz

installdic: mecab-ipadic-2.7.0-20070801
	export PATH=$(PREFIX)/bin:$$PATH; cd mecab-ipadic-2.7.0-20070801 && ./configure --prefix=$(PREFIX) --with-charset=utf8 && make && make install


Grongish.tar.gz:
	curl -fsSL "https://github.com/shogo82148/Grongish/releases/download/v0.0.2/Grongish.tar.gz" -o Grongish.tar.gz

installgrongish: Grongish.tar.gz
	tar zxvf Grongish.tar.gz
	mv Grongish/* .
	rmdir Grongish
	export PATH=$(PREFIX)/bin:$$PATH; pip install -t $(PREFIX) -r requirements.txt

docker:
	mkdir -p grongish-server
	cp Makefile grongish-server/
	cp requirements.txt grongish-server/
	cp lambda_function.py grongish-server/
	docker run -v "$(CURDIR)/grongish-server":/var/task lambci/lambda:build-python2.7 make install

zip:
	cd grongish-server && zip -9 -r ../grongish-server.zip . -x mecab-0.996\* -x mecab.tar.gz -x mecab-ipadic-2.7.0-20070801\* -x mecab-ipadic.tar.gz -x Grongish.tar.gz -x bin\* -x libexec\* -x share\*

test:
	docker run -v "$(PWD)/grongish-server":/var/task lambci/lambda:python2.7 lambda_function.lambda_handler '{"text":"お前のにおいがリントどもを誘ったのだ"}'

clean:
	-rm -rf grongish-server
	-rm grongish-server.zip
