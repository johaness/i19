# Makefile include

POT=$(LOCALES)$(DOMAIN).pot
LANGUAGES=$(LANGUAGES_INCLUDE) $(LANGUAGES_OTHER)
JSON_INCLUDE=$(addsuffix .json, $(addprefix $(LOCALES), $(LANGUAGES_INCLUDE)))
JSON_OTHER=$(addsuffix .jsonpath, $(addprefix $(LOCALES), $(LANGUAGES_OTHER)))


default: combine

extract:
	mkdir -p $(LOCALES)
	i19extract $(POT) $(POT).i19n $(HTML)

init: extract
	for L in $(LANGUAGES); do \
		pybabel init -D $(DOMAIN) -i $(POT) -d $(LOCALES) -l $$L; done

update: extract
	for L in $(LANGUAGES); do \
		pybabel update -D $(DOMAIN) -i $(POT) -d $(LOCALES) -l $$L; done

compile: update
	for L in $(LANGUAGES); do \
		i19json $(LOCALES)$$L/LC_MESSAGES/$(DOMAIN).po $$L $(POT).i19n $(LOCALES)$$L.json; \
		echo "{\"$$L\": \"$(BASEURL)$(LOCALES)$$L.json\"}" > $(LOCALES)$$L.jsonpath; \
    done

combine: compile
	i19dict $(I19JS) $(JSON_OTHER) $(JSON_INCLUDE) 
