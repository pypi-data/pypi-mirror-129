# zapi_mysql
基于异步的快速操作MySQL的组件

使用pip安装
```shell
pip install zapi_mysql
```

## 一、增删改数据

### 1.1 创建表
```python
import asyncio
from zapi_mysql import Mysql
db = Mysql(host='127.0.0.1',
           port=3306,
           user='root',
           password='root',
           db='test')


async def test_example_execute(loop):
    # 删除表
    await db.connect()
    sql = "DROP TABLE IF EXISTS user;"
    
    # 创建表
    await db.execute(sql)
    sql = """CREATE TABLE user
                                  (id INT,
                                  name VARCHAR(255),
                                  PRIMARY KEY (id));"""
    await db.execute(sql)
    
    # 插入SQL语句
    sql = "INSERT INTO user VALUES(1,'张三')"
    await db.execute(sql)


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example_execute(loop))
```

### 1.2 插入数据
```python
import asyncio
from zapi_mysql import Mysql
db = Mysql(host='127.0.0.1',
           port=3306,
           user='root',
           password='root',
           db='test')


async def test_example_execute(loop):
    # 插入SQL语句
    sql = "INSERT INTO user VALUES(2,'李四')"
    await db.execute(sql)


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example_execute(loop))
```

### 1.3 批量插入数据
```python
import asyncio
from zapi_mysql import Mysql
db = Mysql(host='127.0.0.1',
           port=3306,
           user='root',
           password='root',
           db='test')


async def test_example_execute(loop):
    # 插入SQL语句
    data = [(4, 'gothic metal'), (5, 'doom metal'), (6, 'post metal')]
    sql = "INSERT INTO user VALUES(%s,%s)"
    await db.execute(sql, data=data)


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example_execute(loop))
```

## 二、查询数据

### 2.1 查询所有数据
```python
import asyncio
from zapi_mysql import Mysql
db = Mysql(host='127.0.0.1',
           port=3306,
           user='root',
           password='root',
           db='test')


async def test_example_execute(loop):
    # 插入SQL语句
    sql = "SELECT id, name FROM user ORDER BY id"
    result = await db.execute(sql)
    print("查询结果：\n", result)


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example_execute(loop))
```

### 2.2 查询单条数据
```python
import asyncio
from zapi_mysql import Mysql
db = Mysql(host='127.0.0.1',
           port=3306,
           user='root',
           password='root',
           db='test')


async def test_example_execute(loop):
    # 查询单条数据
    sql = "SELECT id, name FROM user ORDER BY id"
    result = await db.execute(sql, return_all=False)
    print("查询结果：\n", result)


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example_execute(loop))
```

