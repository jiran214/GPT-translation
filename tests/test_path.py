"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: test_path.py
 @DateTime: 2023/4/14 19:19
 @SoftWare: PyCharm
"""
from utils import get_abspath_pth


def test_get_abspath_pth():
    res = get_abspath_pth(path='./')
    print(res)
    assert res