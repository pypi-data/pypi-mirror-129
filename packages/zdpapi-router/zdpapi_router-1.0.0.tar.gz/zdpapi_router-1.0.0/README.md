# zdpapi_router
快速开发后端API的路由组件，支持自动生成CRUD接口

说明：此项目基于zdpapi和zdpapi_mysql构建，如果使用有困难的同学，可以先去看这两个框架
- zdpapi项目地址：https://github.com/zhangdapeng520/zdpapi
- zdpapi_mysql项目地址：https://github.com/zhangdapeng520/zdpapi_mysql

本项目地址：https://github.com/zhangdapeng520/zdpapi_router

功能：
- 自动生成新增单条数据路由
- 自动生成新增多条数据路由
- 自动生成删除单条数据路由
- 自动生成删除多条数据路由
- 自动生成修改单条数据路由
- 自动生成修改多条数据路由
- 自动生成查询单条数据路由
- 自动生成查询多条数据路由
- 自动生成分页查询多条数据路由

## 一、快速入门

### 1.1 安装
```shell
pip install zdpapi_router
```

### 1.2 说明
如果您要直接使用示例代码，一定要确保本地安装了MySQL数据库，且创建了名为test的数据库。同时在test数据库中存在user表，该表有id和name两个字段。

如果您学习过我的另一个项目zdpapi_mysql，则直接运行里面的示例代码即可。

### 1.3 入门案例

将下面的代码复制到main.py中
```python
from zdpapi_router import CRUDRouter
from zdpapi import ZApi
from pydantic import BaseModel

app = ZApi()


class UserSchema(BaseModel):
    id: int  # 必须包含ID，批量更新的时候要用到
    name: str


mysql_config = {
    "host": '127.0.0.1',
    "port": 3306,
    "user": 'root',
    "password": 'root',
    "db": 'test'
}
router = CRUDRouter(mysql_config=mysql_config,
                    table_name="user",
                    columns=["name"],
                    chinese_name="用户",
                    schema=UserSchema)
app = router.register(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True)
```

运行
```shell
python main.py
```

访问：http://127.0.0.1:8000/docs

