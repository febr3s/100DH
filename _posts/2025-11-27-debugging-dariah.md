---
title: debugging name processing
tags: MOREL, DARIAH, Jekyll, Zotero
---

# all errors and warnings 

## On image names

Template: Python slugifies "{{}}" as "{{}}", but Jekyll slugifies it as "
	{{}}".

### Problem

Python slugifies "Eine kleine Enzyklopädie der digitalen Langzeitarchivierung" as "eine-kleine-enzyklopa-die-der-2010", but Jekyll slugifies it as "
	/dariah/assets/img/eine-kleine-enzyklopa-die-der--2010".

### Solution

add zotero key instead of author when no author available

### Problem

Python slugifies "Le réseau pensant: pour comprendre la société numérique" as "le-ra-c-seau-pensant-pour-lardellier-2007", but Jekyll slugifies it as "
	le-ra-seau-pensant-pour-lardellier-2007".

Similar for:

big-data-a-revolution-mayer-scha-nberger-2013.jpg and others (titles or authors that have special characters)

### Solution

To be defined, probably something to do with the UTF8 issue

### Problem

Template: Python slugifies "How we think : digital media and contemporary technogenesis" as "how-we-think-hayles-2012", but Jekyll slugifies it as "
	how-we-think-digital-hayles-2012".

## Solution

Something to do with the colon

# On other issues

## Character rendering

"Eine kleine Enzyklopädie der digitalen Langzeitarchivierung" is rendered by Python as "Eine kleine EnzyklopÃ¤die der digitalen Langzeitarchivierung"

"Le rÃ©seau pensant: pour comprendre la sociÃ©tÃ© numÃ©rique"

"Examen des comportements sociaux induits par Internet et l’usage quotidien des autoroutes de l’information. Autour de quatre thÃ¨mes (Ã©pistÃ©mologie, politique, Ã©ducation et culture numÃ©rique), les intervenants enquÃªtent sur ce dispositif sociotechnique qui a bouleversÃ© la sociÃ©tÃ©."

"Viktor Mayer-SchÃ¶nberger"

"L'Ãªtre et l'Ã©cran comment le numÃ©rique change la perception"

## Non permited characters on jekyll build

### titles

- "Digitale Editionsformen. Zum Umgang mit der Ãberlieferung unter den Bedingungen des Medienwandels. Teil 2: Befunde, Theorie und Methodik" (title)
- "SAGW-Bulletin: Dossier "Digital Humanities und Web 2.0"" (title)
- "The Power of Words: Unveiling the Speaker and Writerâs Hidden Craft"

### author

-  DuÅa, Adrian (author)

# Publisher

- Frankfurt am Main: Lang 1995 (sin comillas)
- MÃ¼nchen: Fink 1995 (sin comillas)
- TÃ¼bingen: Gunter Narr 1995