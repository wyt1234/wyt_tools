docker run -d --name brain-postgres --restart always -e POSTGRES_USER='brain' \
  -e POSTGRES_PASSWORD='brain' \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -e ALLOW_IP_RANGE=0.0.0.0/0 \
  -v /home/aminer/postgres/data:/var/lib/postgresql/data \
  -p 5432:5432 postgres:14.2
#docker stop brain-postgres
#cp pg_hba.conf /home/aminer/postgres/data/pgdata/pg_hba.conf
#cp postgresql.conf /home/aminer/postgres/data/pgdata/postgresql.conf
#docker start brain-postgres
