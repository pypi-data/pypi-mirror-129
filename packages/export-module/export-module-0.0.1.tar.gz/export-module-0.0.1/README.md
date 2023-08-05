# export-module

> 让Python支持import/export功能

### 安装 Installation

pip：

```bash
pip install export-module
```

### 用法 Usage

#### Import

```python
from export-module import *
Import("module name")
Import("object name").From("module name")
Import("object name").As("variable name") #Temporarily unavailable
```

#### Export

```python
from export-module import *
Export(object)
Export(name=object,)
```

### 示例 Examples

##### file1.py

```python
from export-module import *
def test(name):
    print(name)
class a(object):
    def __init__(self):
        pass
Export(test,obj=a)
```

##### file2.py

```python
from export-module import *
t2 = Import('test').From("file1")
a = Import('obj').From("file1")
```

