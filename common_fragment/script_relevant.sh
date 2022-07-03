
# 引入pythonpath，可以在虚拟环境的active里加上
export PYTHONPATH=""
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
export PYTHONPATH="/some/path${PYTHONPATH+":"}${PYTHONPATH-}"