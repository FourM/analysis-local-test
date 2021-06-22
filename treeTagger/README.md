# treeTagger

## What is treeTagger
treeTagger is used for morphological analysis of languages such as English

```shell
Japanese sentences -> MeCab
No Japasene sentences -> treeTagger
```

## usage
There is no particular setting for English.

If you want to morphologically analyze the language of another country, 
you need to download the parameter file of that country from the following URL.

[treeTagger](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)

```shell
ex) download Danish parameter file
  cd doc2vec/treeTagger
  curl -O https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/danish.par.gz
  cd ..
  docker-compose down
  docker-compose up -d --build
```

## POS Tag List

```shell
POS Tag|Description|Example
CC|coordinating conjunction|and, but, or, &
CD|cardinal number|1, three
DT|determiner|the
EX|existential there|there is
FW|foreign word|d'œuvre
IN|preposition/subord. conj.|in,of,like,after,whether
IN/that|complementizer|that
JJ|adjective|green
JJR|adjective, comparative|greener
JJS|adjective, superlative|greenest
LS|list marker|(1),
MD|modal|could, will
NN|noun, singular or mass|table
NNS|noun plural|tables
NP|proper noun, singular|John
NPS|proper noun, plural|Vikings
PDT|predeterminer|both the boys
POS|possessive ending|friend's
PP|personal pronoun|I, he, it
PP$|possessive pronoun|my, his
RB|adverb|however, usually, here, not
RBR|adverb, comparative|better
RBS|adverb, superlative|best
RP|particle|give up
SENT|end punctuation|?, !, .
SYM|symbol|@, +, *, ^, |, =
TO|to|to go, to him
UH|interjection|uhhuhhuhh
VB|verb be, base form|be
VBD|verb be, past|was|were
VBG|verb be, gerund/participle|being
VBN|verb be, past participle|been
VBZ|verb be, pres, 3rd p. sing|is
VBP|verb be, pres non-3rd p.|am|are
VD|verb do, base form|do
VDD|verb do, past|did
VDG|verb do gerund/participle|doing
VDN|verb do, past participle|done
VDZ|verb do, pres, 3rd per.sing|does
VDP|verb do, pres, non-3rd per.|do
VH|verb have, base form|have
VHD|verb have, past|had
VHG|verb have, gerund/participle|having
VHN|verb have, past participle|had
VHZ|verb have, pres 3rd per.sing|has
VHP|verb have, pres non-3rd per.|have
VV|verb, base form|take
VVD|verb, past tense|took
VVG|verb, gerund/participle|taking
VVN|verb, past participle|taken
VVP|verb, present, non-3rd p.|take
VVZ|verb, present 3d p. sing.|takes
WDT|wh-determiner|which
WP|wh-pronoun|who, what
WP$|possessive wh-pronoun|whose
WRB|wh-abverb|where, when
:|general joiner|;, -, --
$|currency symbol|$, £
```

## Reference
* [TreeTagger - a part-of-speech tagger for many languages](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)
* [英文の形態素解析ツール「TreeTagger」の品詞コードの，意味・日本語訳の一覧表（完全版）](https://computer-technology.hateblo.jp/entry/20150824/p1)
