SHELL=bash

dev:
	@if [ -f "../backend/.deployed-hostname.txt" ]; then \
		echo "Backend is deployed under http://$$(<../backend/.deployed-hostname.txt):8000"; \
	fi
	npm run dev -- --open

