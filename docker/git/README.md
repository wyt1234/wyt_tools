# 部署

- 部署在 192.168.0.1服务器上


## 编辑gitlab.rb 配置

    external_url：GitLab的资源都是基于这个URL，其实就是clone的地址，如果不配置端口81，使用http进行clone时，页面链接会不显示端口，复制出来的链接会无效；
    gitlab_shell_ssh_port：ssh端口，使用ssh进行clone时的端口；
    listen_port：nginx监听的端口；
    redirect_http_to_https_port：使用https时，nginx监听的端口；
    
    #让gitlab的内置nginx监听2001端口
    nginx['listen_port'] = 2001
    
    # 设置gitlab的访问路径（即nginx反向代理后的地址），不加端口号默认为80，git clone 时用到，定死是http，不用https，不然ngixn配置还要改，麻烦
    external_url 'http://www.sci-brain.cn/gitlab'
    
    ###
    注：设置 external_url ，绑定监听的域名或IP或IP+端口。若GitLab需通过公网访问，最好配置域名加HTTPS;
    若是内部网络访问，则可配置IP或IP+端口，也可配置域名，用户通过配置本地hosts解析访问。
    本文为测试，使用IP方式，即 http://192.168.0.1。因构建容器时映射的是80端口。
    ###
    
    # 调整timout时长，从60秒改为90秒
    gitlab_rails['webhook_timeout'] = 90
    gitlab_rails['git_timeout']=90

    # 配置ssh协议所使用的访问地址和端口
    gitlab_rails['gitlab_ssh_host'] = '192.168.0.1'
    gitlab_rails['gitlab_shell_ssh_port'] = 122 # 此端口是run时22端口映射的122端口


### 让配置生效

    #重启容器
    #docker restart gitlab


## 编辑nginx配置文件

vim /etc/nginx/nginx.conf

    sendfile        on;
    keepalive_timeout  30;

    upstream git {
        server  192.168.0.1:2002;
    }

    gzip  on;

     server {
        listen       80;
        server_name  localhost;
        index  index.php index.html index.htm;

        location / {
		    root /usr/share/nginx/html;
		    index index.html;
		    try_files $uri $uri/ /index.html; # react发布的build包
	    }

	    location /sonobreast {
		    alias /usr/share/nginx/deepbc/; # alias后面必须要用“/”结束
		    try_files $uri $uri/ /sonobreast/index.html; # vue发布的build包
	    }

	    location /static {
		    alias /usr/share/nginx/static/; # alias后面必须要用“/”结束
	    }

	    location /gitlab {
            # 设置最大允许上传单个的文件大小
            client_max_body_size 500m;
            proxy_redirect off;
            #以下确保 gitlab中项目的 url 是域名而不是 http://git，不可缺少
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            # 反向代理到 gitlab 内置的 nginx
            proxy_pass http://git/gitlab;
            index index.html index.htm;
        }

        include conf.d/*.conf;
     }