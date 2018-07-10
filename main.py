# -*- coding: utf-8 -*-
"""
@author : yangyuji
@date : 2018-07-10
@python version:2.7

Noun phrase extraction using Python's regular expression library.
Only for the "SimpleNP" grammar.

"""
from __future__ import print_function
import re,os
import jieba.posseg as pseg
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from pprint import pprint
import uniout

############## SimpleNP
## Uses a five-tag coarse grammar.
## tagset: A D P N O

# Requires conversion from PTB or Petrov/Gimpel tags to our system.
# "Coarse*" indicates petrov/gimpel
# Grammar change from the FST version: can't repeat NUM in both adj and noun.

coarsemap = {
'A': "a ad ag an".split(), #形容词
'D': "r rg rr rz".split(), #限定词
'P': "p".split(), #介词
'N': "n ng nr nrfg nrt ns nt nz".split(), #名词
# all other tags get O
}

## OLDER ATTEMPT: tried to use direct tags as port from foma.
## but this was annoying. have to map back to token positions at the end.
## probably slower too since the python regex compiler is not as smart as foma
# def regex_or(items):
#     return '|'.join(re.escape(x) for x in items)
# Adj = regex_or("JJ JJR JJS CD CoarseADJ CoarseNUM".split())
# Det = regex_or("DT CoarseDET".split())
# Prep= regex_or("IN TO CoarseADP".split())
# Noun= regex_or("NN NNS NNP NNPS FW CD CoarseNOUN CoarseNUM".split())
# ## convention: SPACES separate tags.
# BaseNP = "(({Adj}|{Noun}) )*({Noun} )+".format(**globals())
# PP     = "{Prep} ({Det} )*{BaseNP}".format(**globals())
# NP     = "{BaseNP}({PP} )*".format(**globals())

tag2coarse = {}
for coarsetag,inputtags in coarsemap.items():
    for intag in inputtags:
        assert intag not in tag2coarse
        tag2coarse[intag] = coarsetag

## The grammar!
SimpleNP = "(A|N)*N(PD*(A|N)*N)*"

def coarse_tag_str(pos_seq):
    """Convert POS sequence to our coarse system, formatted as a string."""
    global tag2coarse
    tags = [tag2coarse.get(tag,'O') for tag in pos_seq]
    return ''.join(tags)


def extract_finditer(pos_seq, regex=SimpleNP):
    """The "GreedyFSA" method in Handler et al. 2016.
    Returns token position spans of valid ngrams."""
    ss = coarse_tag_str(pos_seq)
    def gen():
        for m in re.finditer(regex, ss):
            yield (m.start(),m.end())
    return list(gen())

def extract_ngram_filter(pos_seq, regex=SimpleNP, minlen=1, maxlen=8):
    """The "FilterFSA" method in Handler et al. 2016.
    Returns token position spans of valid ngrams."""
    ss = coarse_tag_str(pos_seq)
    def gen():
        for s in xrange(len(ss)):
            for n in xrange(minlen, 1 + min(maxlen, len(ss)-s)):
                e = s+n
                substr = ss[s:e]
                if re.match(regex + "$", substr):
                    yield (s,e)
    return list(gen())


def get_phrases(text=None,grammer='SimpleNP',regex=None,minlen=None, maxlen=None):
    pos_list = []
    words_list = []
    words = pseg.cut(text)
    for w in words:
        pos_list.append(w.flag)
        words_list.append(w.word)
    phrase_tokspans = extract_ngram_filter(pos_list, minlen=minlen, maxlen=maxlen)
    pprint(phrase_tokspans)
    pprint(words_list)

text = "中华人民共和国位于亚洲东部，太平洋西岸，是工人阶级领导的、以工农联盟为基础的人民民主专政的社会主义国家。"
get_phrases(text,grammer='SimpleNP',minlen = 1,maxlen = 4)

