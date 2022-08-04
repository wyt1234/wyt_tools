# production mode will faster?
docker run --name local_meilisearch -it \
  -d -p 7700:7700 \
  --restart=always \
  -e MEILI_MASTER_KEY='MASTER_KEY' \
  getmeili/meilisearch:v0.28.1 \
  meilisearch --env="production"
