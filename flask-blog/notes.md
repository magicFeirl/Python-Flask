## Flask笔记（再）

### `ORM`技术

Object-Relational Mapping，指把关系数据库的表结构映射到对象上。

假设现在有一张表，使用`ORM`我们可以轻松地用Python对象表示：

```mysql
CREATE TABLE user(
	`name` VARCHAR(10) NOT NULL,
    `age` INT NOT NULL, 
    `uid` INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(uid)
);
```

```python
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '' # 设置连接信息

db = SQLALchemy(app) # 示例化db对象


class User():
    __tablename__ = 'user' # 设置表名
    name = db.Column(db.String(10)) # 实例化表格数据
    age = db.Column(db.Integer)
    uid = db.Column(db.Integer, primary_key=True)

    
db.session.add(User(name='U1', age=24))
db.session.commit() # 将更改提交到数据库，在所有数据添加/更改完毕后使用即可
    
```

### 设置`SQLAlchemy`连接信息

 `数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名`

比如想连接到本地的mysql.db `mysql+pymysql://root:123@127.0.0.1/mysql`

### 模板中的代码块

代码块分为两种：变量代码块和语句代码块（个人理解）

其中变量代码块的格式是：`{{ 变量名 }}`

而语句代码块的格式为：`{% for i in li %}`，后面需要对应的end语句，比如for对应的end语句就是

`{% endfor %}`，这点和bash有点相似。

其实用起来和Python中语法感觉没什么差别（理应），主要是要注意区分。

#### 获取对象中的数据

假设现有一个列表`li = [1, 2, 3, 4]`，如何在模板中获取其中的值呢？

和Python中相同，我们可以直接用下标索引列表数据，另外还可以用.来获取，不过个人更习惯前者。

代码

```html
<li>{{ li[0] }}</li> # 通过下标获取
{% for i in li %} # 遍历列表
 <li>{{ i }}</li>
{% endfor %}
```

#### 继承模板

使用继承模板可以简化大量重复的代码，我们可以定义一个`base.html`，里面存放着html的基本代码和网页共有的元素。使用`{% block 块名称 %}`来定义一个块，这个块会被子页面继承，而子页面可以复写其中的内容。

```html
<!-- base.html -->
<html>
    <head>
        
    </head>
    
    <body>
        {% block content%}
        {% endblock %}
    </body>
</html>
```

在子页面使用`{% extends base.html %}`继承模板（需要注意该语句没有对应的end块）。

```html
{% extends base.html %}

<!-- 在此处复写base.html中content块的内容 -->
{% block content %}
 <h2>Hello flask</h2>
{% endblock %}
```

#### 引入模板

举个例子：如果有部分页面需要`navbar`，而有部分不需要，那么就不能简单的将`navbar`定义到`base.html`，可以使用`{% include 'navbar.html' %}`在需要的页面引入`navbar`的内容（该语句也没有end语句块）。

```html
<!-- navbar.html -->

<h2>
    Hello world
</h2>
```

```html
<body>
    {% include 'navbar.html' %}
    <p>
        你好世界
    </p>
</body>
```

### 使用`__init__.py`管理包

初学`flask`有个蛋疼的问题：有多个模块需要`Flask`实例对象，但是如果只是简单的把实例从A导入B，再从B导入A就会发生循环导入的现象，以前我的解决方法是干脆只使用一个`app.py`，里面存放`Flask`实例，然后把`model`什么的都放在里面，共用一个实例对象。但是这样代码量大了之后程序会变得非常难以维护，而且不够模块化，所以为了长远考虑，应该使用包。

#### 模块和包

在当前项目文件夹中新建一个名为`__init__.py`的文件，就定义了一个包，`__init__.py`的内容可以为空。可以在`__init__.py`中存放导入包时的初始化代码，类似构造方法的存在。

**以上代码都是直接打在Markdown里的，不保证没错误**

