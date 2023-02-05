.PHONY: install-tools


install-tools: tools/bin/activate


tools/bin/activate:
	python -m venv tools
	./tools/bin/pip install -r requirements.txt

