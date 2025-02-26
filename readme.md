# Greek Macronizer

Refer mainly to:
http://macronizer.gr/

## Dependencies 

    Python:

        pip3 install requests
        pip3 install tqdm
        pip3 install bs4
        pip3 install greek_accentuation
        pip3 install numpy
        pip3 install scipy
        pip3 install pyuca
        pip3 install beautifulsoup

    Ruby:
        gem install parallel
        tinycus and genos need to be cloned from Bitbucket into the ifthimos folder


To understand the way in which the tokens have been extracted and the artifacts created thereby is crucial.
Take as an exampe Soph. Ajax 699f, Νύσια Κνώσι᾽ ὀρχήματ᾽ αὐτοδαῆ ξυνὼν ἰάψῃς:

Νύσια	a-p---na-	Νύσιος
Κνώσι	n-p---na-	Κνώσι
’	n-p---na-	’
ὀρ	n-p---na-	ὀρ
-	u--------	-
χήματ	n-p---na-	χήματ
’	n-p---na-	’
αὐτοδαῆ	a-p---na-	αὐτοδαής
ξυνὼν	v-sppamn-	ξυνὼν
ἰάψῃς	v2sasa---	ἰάπτω

Obviously, words followed by a line with an elision mark, need to be reunited with this mark (Κνώσι, χήματ + ’),
and words encircling a line-break mark need to be joined together (ὀρ + χήματ).

Now, the use of dashes for ellipses could have created confusion, as e.g. Eur. IT 1, 23, "τίκτει — τὸ καλλιστεῖον εἰς ἔμ᾽ ἀναφέρων —"

—	u--------	—
τὸ	l-s---na-	ὁ
καλλιστεῖον	n-s---na-	καλλιστεῖον
εἰς	r--------	εἰς
ἔμ	p-s---ma-	ἔμ
’	p-s---ma-	’
ἀναφέρων	v-sppamn-	ἀναφέρω
—	u--------	—

Luckily, the two usages have (hopefully consistently!) separate unicodes: the line-break is a short en dash, same as in the tag,
while the ellipsis is surrounded by two em dashes. 

## FLÖDESSCHEMA

### FÖRBEREDA TOKENS.TSV (Detta kan göras igen om det släpps bättre POS-analys) 
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
    ii. CGCG 1.72: Ord kan bara sluta på vokaler och ν, ρ, σ, ξ, ψ (förutom ἐκ, οὐκ, οὐχ, vilka ej är relevanta)
8. Rensa bort tokens med extra akut på ultiman pga enclitica
9. Rensa bort eliderade ord OM det finns oeliderade motsvarigheter. Annars inkludera.


Skulle behövas en second-opinion för lemmatisering och POS-analys. Morpheus? ChatGPT?

### BYGGA MACRONS.TSV

Nu byggs en fjärde kolumn, MACRON, utöver de första tre från tokens.txt

0. Tokens med enbart "gratis" macrons togs bort i steg 6. Dessa kan lätt makroniseras algoritmiskt och behöver ej finnas i macrons.tsv.
Vissa tokens har tog både obestämbara och "gratis", och då bör de som är gratis makroniseras i filen, då målet är att alla dichrona i filen ska vara indikerade
- Om ett ord har cirkumflex eller iota subscriptum/adscriptum på ett α, ι, υ, så makronisera detta tecken direkt
- Om ett properispomenon eller proparoxtiton har ett α, ι, υ på ultiman, så "breve-isera" ultiman direkt

Följande typer av tokens mappas också mot sina normala motsvarigheter och inkluderas ej i vår dictionary:
- tokens på grav
- eliderade tokens (sex teoretiska alternativ: om det mot all förmodan finns flera möjliga oeliderade motsvarigheter i dictionary, så kolla ordklass och/eller morfologi för att disambiguera)
- eliderade tokens som aspirerats av följande ord, e.g. τ > θ, κ > χ, π > φ

- tokens med extra akut på ultiman pga enclitica 

1. Algoritmiskt lägga in de långa som finns i regelbundna deklinationer/konjugationer; kanske använda ifthimos
2. Lägga in scrapeade former från LSJ.gr och Wiktionary etc. Inkl. POS-info? 
3. Sök på tokens med dichrona i öppna stavelser i HYPOTACTICs metrik-corpus
4. Gissa slutvokal på eliderade former och skicka till oeliderade motsvarigheter
4. Manuellt kolla resterande rötter



NB:
Några få ord i TLG-corpuset är i ALL-CAPS och kommer nog bara från titel och talare:

<l n="t"><label type="head">ΑΛΚΗΣΤΙΣ</label> </l>
<l n="1"><label type="speaker">ΑΠΟΛΛΩΝ</label> 

Dessa ord kan sorteras bort, då de ändå inte är relevanta för metern.

## Explanation of tags

Taggen i raden
    `VERB	λάβηι	v3sasa---	λάβηι`
läses som 
    v = VERB
    3 = tredje person
    s = singular
    a = aorist
    s = subjunktiv
    a = aktivum

### POS tags (source: https://github.com/cltk/greek_treebank_perseus)

        1: 	part of speech
        
            n	noun
            v	verb
            t	participle
            a	adjective
            d	adverb
            l	article
            g	particle
            c	conjunction
            r	preposition
            p	pronoun
            m	numeral
            i	interjection
            e	exclamation
            u	punctuation
        
        2: 	person
        
            1	first person
            2	second person
            3	third person
        
        3: 	number
        
            s	singular
            p	plural
            d	dual
        
        4: 	tense
        
            p	present
            i	imperfect
            r	perfect
            l	pluperfect
            t	future perfect
            f	future
            a	aorist
        
        5: 	mood
        
            i	indicative
            s	subjunctive
            o	optative
            n	infinitive
            m	imperative
            p	participle
        
        6: 	voice
        
            a	active
            p	passive
            m	middle
            e	medio-passive
        
        7:	gender
        
            m	masculine
            f	feminine
            n	neuter
        
        8: 	case
        
            n	nominative
            g	genitive
            d	dative
            a	accusative
            v	vocative
            l	locative
        
        9: 	degree
        
            c	comparative
            s	superlative
