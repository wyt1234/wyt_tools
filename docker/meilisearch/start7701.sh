# 请在192.168.0.3 -> /home/amnier/meilisearch目录下操作

docker stop brain_meilisearch7701
#docker rm brain_meilisearch7701

docker run --name brain_meilisearch7701 -it \
  -d -p 7701:7700 \
  --restart=always \
  -e MEILI_MASTER_KEY='MASTER_KEY' \
  getmeili/meilisearch:v0.28.1 \
  meilisearch --env="production"
