# 暂部署在192.168.0.17上
gunicorn -w 3 -b 0.0.0.0:8082 spacy_similarities_app:app -D
ps -ef | grep 0.0.0.0:8082
#kill -9 xxxx
