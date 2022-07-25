docker run -d --name postgres_local --restart always -e POSTGRES_PASSWORD=postgrespw -e ALLOW_IP_RANGE=0.0.0.0/0 -p 5432:5432 postgres:14.2

docker cp postgres_local:/var/lib/postgresql/data/postgresql.conf .
docker cp postgres_local:/var/lib/postgresql/data/pg_hba.conf .
