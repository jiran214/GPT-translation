"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: prompt.py
 @DateTime: 2023/4/13 19:59
 @SoftWare: PyCharm
"""
import tiktoken


class TokenCounter:

    def __init__(self, model='gpt-3.5-turbo', max_tk=4096 - 1024):
        self._encoder = tiktoken.encoding_for_model(model)
        self.max_tk = max_tk
        self._encoder_tk = 0
        self._text_list = []

    def add_text(self, text: str):
        tk = len(self._encoder.encode(text))
        if tk > self.max_tk:
            raise f'暂不支持单行超过 {self.max_tk} token数量'
        self._encoder_tk += tk

        if status := self._encoder_tk < self.max_tk:
            self._text_list.append(text)
        return status

    @property
    def text_list(self):
        return self._text_list

    def clear(self):
        self._encoder_tk = 0
        self._text_list = []
