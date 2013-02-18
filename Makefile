# languages to generate
LANGUAGES=en de
# languages to include in i19dict.js (no separate loading)
INCLUDE_LANGUAGES=en de
# translation domain
DOMAIN=demo
# locale directory
LOCALES=locale/


POT=locale/$(DOMAIN).pot 
JSON=$(addsuffix .json, $(addprefix $(LOCALES), $(INCLUDE_LANGUAGES)))
PATH:=$(PATH):.

default: combine

extract:
	mkdir -p $(LOCALES)
	i19extract.py *.html > $(POT)

init: extract
	for L in $(LANGUAGES); do \
		pybabel init -D $(DOMAIN) -i $(POT) -d $(LOCALES) -l $$L; done

update: extract
	for L in $(LANGUAGES); do \
		pybabel update -D $(DOMAIN) -i $(POT) -d $(LOCALES) -l $$L; done

compile: update
	for L in $(LANGUAGES); do \
		i19json.py $(LOCALES)$$L/LC_MESSAGES/$(DOMAIN).po $$L $(LOCALES)$$L.json; done

combine: compile
	i19dict.py i19dict.js $(JSON)
