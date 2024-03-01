macrons.txt har ungefär 37-38 tusen unika lemmata.
LSJ har runt 116 502 lemmata. 

Taggen i raden
    VERB	λάβηι	v3sasa---	λάβηι
läses som 
    v = VERB
    3 = tredje person
    s = singular
    a = aorist
    s = subjunktiv
    a = aktivum


FLÖDESSCHEMA

FÖRBEREDA TOKENS.TXT (Detta kan göras igen om det släpps bättre POS-analys) 
Detta delflöde är klart i en första version. Se prepare_tokens/main_tokens.py för vilka script det rör sig om.

1. Ta bort all punktuation, ev. förutom ' för elision (remove_punctuation.py) (möjligtvis skapas nya dubletter)
2. Ta bort dubletter
3. Ta bort konstiga rader bortom all räddning
4. Normalisering
5. Sortera alfabetiskt med pyuca
6. Ta bort alla rader vars TOKEN
    - ej innehåller α, ι, υ
    - har cirkumflex eller iota subscriptum/adscriptum på sin enda α, ι, υ (behövs ej dictionary), eller denna ingår i en diftong
    - är properispomenon och inte har α, ι, υ på en tidigare stavelse än penultiman (behövs ej dictionary)
    - är proparoxiton och -"-
7. Felaktig POS-analys som behöver köras om i OdyCy och/eller annan analysator:
    i. Om en TAG innehåller 'x' eller är kortare än nio tecken, flytta raden till lines_x.txt
    ii. Om ett LEMMA ej innehåller vokaler, flytta raden till lines_x.txt

Kör sen OdyCy och/eller annan POS-analys igen på alla TOKENs i lines_x.txt, 
och låt resultatet genomgå allt ovan. Om ngt är kvar, så lägg till i tokens.txt

Skulle behövas en second-opinion för lemmatisering och POS-analys. Morpheus? ChatGPT?

BYGGA MACRONS.TXT (Detta är en skiss; arbetet har knappt påbörjats i skrivande stund 1 mars)

Nu byggs en fjärde kolumn, MACRON, utöver de första tre från tokens.txt

0. Tokens med enbart "gratis" macrons togs bort i steg 6. Dessa kan lätt makroniseras algoritmiskt och behöver ej finnas i macrons.txt.
Vissa tokens har tog både obestämbara och "gratis", och då bör de som är gratis makroniseras i filen, då målet är att alla dichrona i filen ska vara indikerade
- Om ett ord har cirkumflex eller iota subscriptum/adscriptum på ett α, ι, υ, så makronisera detta tecken direkt
- Om ett properispomenon eller proparoxtiton har ett α, ι, υ på ultiman, så "breve-isera" ultiman direkt

1. Algoritmiskt lägga in de långa som finns i regelbundna deklinationer/konjugationer; kanske använda ifthimos
2. Lägga in scrapeade former från LSJ.gr och Wiktionary etc. Inkl. POS-info? 
3. Sök på tokens med dichrona i öppna stavelser i HYPOTACTICs metrik-corpus
4. Gissa slutvokal på eliderade former och skicka till oeliderade motsvarigheter
4. Manuellt kolla resterande rötter


    ADJ: adjective
    ADP: adposition
    ADV: adverb
    AUX: auxiliary
    CCONJ: coordinating conjunction
    DET: determiner
    INTJ: interjection
    NOUN: noun
    NUM: numeral
    PART: particle
    PRON: pronoun
    PROPN: proper noun
    PUNCT: punctuation
    SCONJ: subordinating conjunction
    SYM: symbol
    VERB: verb
    X: other

