#!/bin/bash
# from https://gist.github.com/dtan4/351d031bec0c3d45cd8f
# see also http://qiita.com/dtan4/items/c6a087666296fbd5fffb

wget -O mecab-0.996.tar.gz 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE'
tar zxfv mecab-0.996.tar.gz
cd mecab-0.996 || exit
./configure --enable-utf8-only
make
make check
sudo make install
sudo ldconfig
