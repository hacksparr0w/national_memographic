FROM python:3

RUN pip install national_memographic

CMD meme bot \
  --api-key $TW_API_KEY \
  --api-secret $TW_API_SECRET \
  --access-token $TW_ACCESS_TOKEN \
  --access-secret $TW_ACCESS_SECRET
