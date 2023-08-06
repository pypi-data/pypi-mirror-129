# pypdm

> mysql/sqlite 的 PDM 生成器

------

## 运行环境

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg) ![](https://img.shields.io/badge/PyCharm-4.0.4%2B-brightgreen.svg)


## 在线安装

`pip install pypdm-db`

## 使用指引

示例代码可参考单元测试：

- sqlite: [test_pypdm_sqlite.py](tests/test_pypdm_sqlite.py)
- mysql: [test_pypdm_mysql.py](tests/test_pypdm_mysql.py)

通过以下函数可生成对应数据库的连接对象：

- `from pypdm.dbc._sqlite import SqliteDBC`
- `from pypdm.dbc._mysql import MysqlDBC`

通过函数 `from pypdm.builder import build` 可生成指定数据表的 PDM 文件。

例如数据库中已有表 [`t_teachers`](tests/db/sqlite/init_db.sql) ，会在指定的 package 目录生成两个代码文件：

- Bean 文件： [*/bean/t_teachers.py](tests/tmp/pdm/sqlite/bean/t_teachers.py)
- DAO 文件：  [*/dao/t_teachers.py](tests/tmp/pdm/sqlite/dao/t_teachers.py)


其中 Bean 文件与表 `t_teachers` 的表结构一一对应， DAO 文件则封装了针对表 `t_teachers` 的增删改查函数。利用这两个文件，就可以方便地对表 `t_teachers` 进行操作。


## 开发者说明

<details>
<summary>展开</summary>
<br/>

### 项目打包

每次修改代码后，记得同步修改 [`setup.py`](setup.py) 下的版本号 `version='x.y.z'`。

```
# 构建用于发布到 PyPI 的压缩包
python setup.py sdist

# 本地安装（测试用）
pip install .\dist\pypdm-db-?.?.?.tar.gz

# 本地卸载
pip uninstall pypdm-db
```

### 项目发布

首先需要在 [PyPI](https://pypi.org/) 上注册一个帐号，并在本地用户根目录下创建文件 `~/.pypirc`（用于发布时验证用户身份），其内容如下：

```
[distutils]
index-servers=pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = <username>
password = <password>
```

其次安装 twine 并上传项目： 

```
# 首次发布需安装
pip install twine

# 发布项目， 若发布成功可在此查看 https://pypi.org/manage/projects/
twine upload dist/*
```

发布到 [PyPI](https://pypi.org/) 的项目名称必须是全局唯一的，即若其他用户已使用该项目名称，则无法发布（报错：`The user 'xxx' isn't allowed to upload to project 'yyy'.`）。此时只能修改 [`setup.py`](setup.py) 下的项目名称 `name`。

> 本项目已集成了 Github Workflows，每次推送更新到 master 即可自动打包


### 关于测试

详见 [单元测试说明](tests)


### 参考资料

- [python package 开发指引](https://packaging.python.org/#python-packaging-user-guide)
- [python package 示例代码](https://github.com/pypa/sampleproject)

</details>


## 赞助途径

| 支付宝 | 微信 |
|:---:|:---:|
| ![](imgs/donate-alipay.png) | ![](imgs/donate-wechat.png) |


## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
