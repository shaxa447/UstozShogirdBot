
init:
	pybabel init -i locales/messages.pot -d locales -D messages -l uz
	pybabel init -i locales/messages.pot -d locales -D messages -l en


extract:
	pybabel extract --input-dirs=. -o locales/messages.pot

update:
	pybabel update -d locales -D messages -i locales/messages.pot

compile_language:
	pybabel compile -d locales -D messages