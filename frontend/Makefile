SHELL=bash

help:
	@echo "Makefile for managing the frontend application"
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  help            Show this help message"
	@echo "  dev             Run the application in development mode"

dev:
	@if [ -f "../backend/.deployed-hostname.txt" ]; then \
		echo "Backend is deployed under http://$$(<../backend/.deployed-hostname.txt):8000"; \
	fi
	@npm install
	@BACKEND=$$(<../backend/.deployed-hostname.txt) npm run dev -- --open

