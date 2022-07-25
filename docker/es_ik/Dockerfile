FROM elasticsearch:7.3.2

COPY readonlyrest.yml /usr/share/elasticsearch/config/readonlyrest.yml

COPY readonlyrest-1.20.0_es7.3.2.zip /download-folder/readonlyrest-1.20.0_es7.3.2.zip

COPY elasticsearch-analysis-ik-7.3.2.zip /download-folder/elasticsearch-analysis-ik-7.3.2.zip

RUN sh -c 'echo -e "y" | /usr/share/elasticsearch/bin/elasticsearch-plugin install file:///download-folder/readonlyrest-1.20.0_es7.3.2.zip'

RUN sh -c 'echo -e "y" | /usr/share/elasticsearch/bin/elasticsearch-plugin install file:///download-folder/elasticsearch-analysis-ik-7.3.2.zip'
