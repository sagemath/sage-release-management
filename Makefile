export REPO_ROOT:=$(shell git rev-parse --show-toplevel)
export TOOL:=$(REPO_ROOT)/tools/bin

.PHONY: all
all: test lint


include Makefile.d/install.mk
include Makefile.d/lint.mk
include Makefile.d/test.mk



.PHONY: shell
shell:
	$(TOOL)/ipython

