#!/bin/bash
# from https://gist.github.com/dtan4/351d031bec0c3d45cd8f
# see also http://qiita.com/dtan4/items/c6a087666296fbd5fffb

set -uxe

TMPDIR=$(mktemp -d)
trap 'rm -rfv "$TMPDIR"' EXIT

MECAB_VERSION=0.996.11

# install mecab
cd "$TMPDIR"
curl -o mecab.tar.gz -sSL "https://github.com/shogo82148/mecab/releases/download/v$MECAB_VERSION/mecab-$MECAB_VERSION.tar.gz"
tar zxfv mecab.tar.gz
cd "mecab-$MECAB_VERSION"
./configure --enable-utf8-only
make
make check
sudo make install
sudo ldconfig

# install python binding
cd "$TMPDIR"
curl -o mecab-python.tar.gz -sSL "https://github.com/shogo82148/mecab/releases/download/v$MECAB_VERSION/mecab-python-$MECAB_VERSION.tar.gz"
tar zxfv mecab-python.tar.gz
cd "mecab-python-$MECAB_VERSION"
python -m pip install .
