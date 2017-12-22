freeze:
	rm requirements.txt
	pip freeze | grep -v "pkg-resources" > requirements.txt
