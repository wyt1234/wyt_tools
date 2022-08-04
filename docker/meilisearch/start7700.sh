# 请在192.168.0.3 -> /home/amnier/meilisearch目录下操作

docker stop brain_meilisearch7700
#docker rm brain_meilisearch7700

# Launch Meilisearch in development mode with a master key
#docker run --name brain_meilisearch -it \
#  -d -p 7700:7700 \
#  --restart=always \
#  -e MEILI_MASTER_KEY='MASTER_KEY' \
#  -v /home/aminer/meilisearch/meili_data:/meili_data \
#  getmeili/meilisearch:v0.27.2 \
#  meilisearch --env="development"

# without volum (faster？) -> NO
#docker run --name brain_meilisearch -it \
#  -d -p 7700:7700 \
#  --restart=always \
#  -e MEILI_MASTER_KEY='MASTER_KEY' \
#  getmeili/meilisearch:v0.27.2 \
#  meilisearch --env="development"

# production mode will faster?
docker run --name brain_meilisearch7700 -it \
  -d -p 7700:7700 \
  --restart=always \
  -e MEILI_MASTER_KEY='MASTER_KEY' \
  getmeili/meilisearch:v0.28.1 \
  meilisearch --env="production"
