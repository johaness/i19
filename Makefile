# languages to include in i19dict.js (no separate loading)
LANGUAGES_INCLUDE=en
# other languages to generate
LANGUAGES_OTHER=de
# translation domain
DOMAIN=demo
# locale directory
LOCALES=locale/


POT=$(LOCALES)$(DOMAIN).pot 
LANGUAGES=$(LANGUAGES_INCLUDE) $(LANGUAGES_OTHER)
JSON_INCLUDE=$(addsuffix .json, $(addprefix $(LOCALES), $(LANGUAGES_INCLUDE)))
JSON_OTHER=$(addsuffix .jsonpath, $(addprefix $(LOCALES), $(LANGUAGES_OTHER)))
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
		i19json.py $(LOCALES)$$L/LC_MESSAGES/$(DOMAIN).po $$L $(LOCALES)$$L.json; \
		echo "{\"$$L\": \"$(LOCALES)$$L.json\"}" > $(LOCALES)$$L.jsonpath; \
    done

combine: compile
	i19dict.py i19dict.js $(JSON_INCLUDE) $(JSON_OTHER)
