
.PHONY: test
test: \
    test-unit



.PHONY: test-unit
test-unit:
	$(TOOL)/python -m unittest discover

