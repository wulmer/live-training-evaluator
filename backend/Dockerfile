# use uv base image
FROM ghcr.io/astral-sh/uv:alpine

RUN apk add --no-cache \
  unixodbc-dev \
  g++

RUN \
  apk add --no-cache curl ; \
  curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.6.1-1_amd64.apk ;\
  curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.10.1.1-1_amd64.apk  ;\
  apk add --allow-untrusted msodbcsql17_17.10.6.1-1_amd64.apk ;\
  apk add --allow-untrusted mssql-tools_17.10.1.1-1_amd64.apk ;\
  rm msodbcsql17_17.10.6.1-1_amd64.apk ;\
  rm mssql-tools_17.10.1.1-1_amd64.apk ;\
  apk del curl

ADD .python-version pyproject.toml uv.lock /app

WORKDIR /app

RUN uv sync --locked

ADD app /app/app

CMD ["uv", "run", "uvicorn", "--host", "0.0.0.0", "app.main:app"]
