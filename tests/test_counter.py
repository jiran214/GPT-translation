"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: test_counter.py
 @DateTime: 2023/4/13 20:39
 @SoftWare: PyCharm
"""
from prompt import TokenCounter


def test_tk_counter():
    tk_counter = TokenCounter()

    text_list = ['只因你太美！' * 100] * 100

    res = []
    for text in text_list:
        status = tk_counter.add_text(text)
        assert tk_counter._encoder_tk != 0
        if not status:
            res = tk_counter.text_list

    print(len(res))
    assert len(res) not in (0, 1, 100)
