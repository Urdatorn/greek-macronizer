import spacy

nlp = spacy.load("grc_odycy_joint_trf")

doc = nlp("ὦ παῖ, τέλος μὲν Ζεὺς ἔχει βαρύκτυπος πάντων ὅσ᾽ ἔστι, καὶ τίθησ᾽ ὅκῃ θέλει")

#for token in doc:
#   print(token.orth_, token.lemma_,token.is_stop, token.pos_, token.morph, token.dep_, token.head)

from spacy import displacy
displacy.serve(doc, port=5001)
