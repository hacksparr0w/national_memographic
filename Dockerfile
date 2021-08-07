FROM python:3

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry install

CMD poetry run \
  meme bot \
  --api-key $TW_API_KEY \
  --api-secret $TW_API_SECRET \
  --access-token $TW_ACCESS_TOKEN \
  --access-secret $TW_ACCESS_SECRET
