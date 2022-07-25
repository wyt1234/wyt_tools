- --auth：需要密码才能访问容器服务。

## 用以下命令添加用户和设置密码，并且尝试连接

- 创建管理员账号 和 指定db 的账号

```shell
# 进入容器
$ docker exec -it name bash
# 进入mongo shell
$ mongo admin
# 创建一个名为 admin，密码为 aminer@sz2022 的用户。
>  db.createUser({ user:'admin', pwd:'aminer@sz2022',roles:[ { role:'userAdminAnyDatabase', db: 'admin'}, "readWriteAnyDatabase"]});
# 尝试使用上面创建的用户信息进行连接。
> db.auth('admin', 'aminer@sz2022')

# 创建其它db
> use diagnose
# 给该db创建用户
> db.createUser({ user:'diagnose', pwd:'diagnose@2022',roles:[ { role:'readWrite', db: 'diagnose'}]})
# 验证在该db下创建的用户是否成功
> db.auth('diagnose', 'diagnose@2022')
> exit
```

```shell
# 创建其它db
> use scibrain
# 给该db创建用户
> db.createUser({ user:'scibrain', pwd:'scibrain@2022',roles:[ { role:'readWrite', db: 'scibrain'}]})
# 验证在该db下创建的用户是否成功
> db.auth('scibrain', 'scibrain@2022')
> exit
```

