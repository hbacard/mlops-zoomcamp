1. Create a `.env` containing the credentials for AWS (with full S3 access) containing these values
```
AWS_ACCESS_KEY_ID=value
AWS_SECRET_ACCESS_KEY=value
AWS_DEFAULT_REGION=value
BUCKET_NAME=value
```
2. Build the image with `docker build -t taxi-duration .`.
3. Create container by passing the environment variables `docker run --env-file .env taxi-duration`.

Alternatively use docker-compose
