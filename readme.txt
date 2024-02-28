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

    1. Ta bort all punktuation, ev. förutom ' för elision (remove_punctuation.py) (möjligtvis skapas nya dubletter)
    3. Ta bort dubletter
    4. Ordna alfabetiskt
    5. Omvandla till BETA CODE (beta_code.py)
    2. Gör allt till gemener, i.e. ta bort alla '*' (möjligtvis skapas nya dubletter, så kolla dubletter igen)
    6. Ta bort alla rader vars TOKEN
        - ej innehåller α, ι, υ
        - har cirkumflex på sin enda α, ι, υ (behövs ej dictionary)
        - är properispomenon och inte har α, ι, υ på en tidigare stavelse än penultiman (behövs ej dictionary)
    7. Felaktig POS-analys:
        i. Om en TAG innehåller 'x' eller är kortare än nio tecken, flytta raden till lines_x.txt
        ii. Om ett LEMMA ej innehåller vokaler, flytta raden till lines_x.txt

    Kör sen OdyCy och/eller annan POS-analys igen på alla TOKENs i lines_x.txt, 
    och låta resultatet genomgå allt ovan. Om ngt är kvar, så lägg till i tokens.txt
    
    BYGGA MACRONS.TXT

    Nu byggs en fjärde kolumn, MACRON, med de första tre från tokens.txt
    "GRATIS" MACRONS
    OBS: 
    - Om ett ord har cirkumflex på en α, ι, υ, så makronisera direkt
    - Om ett properispomenon har en α, ι, υ på ultiman, så "breve-isera" ultiman direkt

    1. Algoritmiskt lägga in de långa {A, I, U} som finns i regelbundna deklinationer/konjugationer
    2. Lägga in scrapeade former från LSJ.gr och Wiktionary etc.
    3. Sök på tokens med kvarvarande {A, I, U} i HYPOTACTICs metrik-corpus, om dess {A, I, U} är i öppen stavelse
    4. Manuellt kolla resten (beroende på om det är hanterbart)
