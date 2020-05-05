compile:
	python3 compile.py

black:
	black compile.py

serve: compile
	cd compiled && mkdocs serve -s
