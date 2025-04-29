# use uv base image
FROM ghcr.io/astral-sh/uv:alpine

ADD app /app/app
ADD .python-version pyproject.toml uv.lock /app

WORKDIR /app

RUN uv sync --locked

CMD ["uv", "run", "uvicorn", "--host", "0.0.0.0", "app.main:app"]
