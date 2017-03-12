MECAB_DICT_INDEX=$(shell mecab-config --libexecdir)/mecab-dict-index
PYTHON=python

.PHONY: all test
all: Grongish.tar.gz

fromgrongishdic/sys.dic: fromgrongishdic/word.csv fromgrongishdic/char.def fromgrongishdic/unk.def fromgrongishdic/dic.csv
	cd fromgrongishdic && $(MECAB_DICT_INDEX)

fromgrongishdic/dic.csv: mkdic_from_grongish.py togrongishdic/sys.dic
	$(PYTHON) mkdic_from_grongish.py

togrongishdic/sys.dic: mkdic_to_grongish.py togrongishdic/Noun.number.csv
	$(PYTHON) mkdic_to_grongish.py
	cd togrongishdic && $(MECAB_DICT_INDEX)

Grongish.tar.gz: fromgrongishdic/sys.dic togrongishdic/sys.dic GrongishTranslator.py
	rm -rf Gronfish
	mkdir -p Grongish/fromgrongishdic
	cp GrongishTranslator.py README.md Grongish/
	cp fromgrongishdic/dicrc fromgrongishdic/char.bin fromgrongishdic/char.bin fromgrongishdic/matrix.bin fromgrongishdic/sys.dic fromgrongishdic/unk.dic Grongish/fromgrongishdic/
	mkdir -p Grongish/togrongishdic
	cp togrongishdic/dicrc togrongishdic/char.bin togrongishdic/char.bin togrongishdic/matrix.bin togrongishdic/sys.dic togrongishdic/unk.dic Grongish/togrongishdic/
	tar zcvf Grongish.tar.gz Grongish

test: togrongishdic/sys.dic
	python3 -m unittest tests.test_all
