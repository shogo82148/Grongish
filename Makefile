MECAB_DICT_INDEX=$(shell mecab-config --libexecdir)/mecab-dict-index
PYTHON=python

.PHONY: all
all: grongishdic/sys.dic

grongishdic/sys.dic: grongishdic/word.csv grongishdic/char.def grongishdic/unk.def grongishdic/dic.csv
	cd grongishdic && $(MECAB_DICT_INDEX)

grongishdic/dic.csv:
	$(PYTHON) mkdic.py

Grongish.tar: grongishdic/sys.dic
	rm -rf Gronfish
	mkdir -p Grongish/grongishdic
	cp GrongishTranslator.py README.md Grongish/
	cp grongishdic/dicrc grongishdic/char.bin grongishdic/char.bin grongishdic/matrix.bin grongishdic/sys.dic grongishdic/unk.dic Grongish/grongishdic/
	tar zcvf Grongish.tar Grongish
