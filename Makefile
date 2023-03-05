.PHONY: test run

test:
	pytest

run:
	cargo watch -q -c -w src/ -x run
