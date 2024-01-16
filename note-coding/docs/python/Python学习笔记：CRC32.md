# Python学习笔记：CRC32

## 基本概念

CRC全称：循环冗余校验（Cyclic Redundancy Check）。

CRC是一种用于校验通信链路上数字传输准确性的计算方法（通过某种数学运算来建立数据位和校验位的约定关系），这种方法尽量提高接受方收到数据的正确率。

值得注意，CRC只是一种数据错误检查技术，是一种常用的检错码，但并不能用于自动纠错。

```python
from zlib import crc32

def is_id_in_test_set(identifier, test_ratio):
    return crc32(np.int64(identifier)) < test_ratio * 2**32
```

