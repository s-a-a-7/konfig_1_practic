# Makefile для эмулятора

.PHONY: run test help clean

PYTHON ?= python3

help:
	@echo "Доступные цели:"
	@echo "  make run       — запустить эмулятор (интерактивный режим)"
	@echo "  make test      — запустить smoke-тест (требует --vfs и --script)"
	@echo "  make clean     — удалить __pycache__ и *.pyc"

run:
	$(PYTHON) -m src.app

test:
	$(PYTHON) -m src.app --vfs $(VFS) --script $(SCRIPT)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true