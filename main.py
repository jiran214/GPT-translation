"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: api.py
 @DateTime: 2023/4/13 21:01
 @SoftWare: PyCharm
"""
import asyncio
import os
import pathlib
import time
from pathlib import Path

import fire

from process import Process

ALLOWED_FILE_TYPES = [
    ".txt",
    ".md",
    # ".rtf",
    # ".html",
    # ".pdf",
]

default_path = os.path.join(
    os.path.dirname(__file__),'translated'
)


class Run:
    def __init__(
            self,
            input_path,
            output_dir_path=default_path,
            language=None,
            api_key=None,
            proxy=None,
            concurrent_request=4,

            # 文件爬取时可以设置
            file_extension: str = None,
            concurrent_file=1,
    ):
        # 输入输出配置
        self.input_path = input_path
        # 输出文件夹，首选用户定义的输出位置，后选项目
        self.output_dir_path = output_dir_path
        self.file_extension = file_extension
        self.api_key = api_key
        self.proxy = proxy

        self.task = []
        self.initialize_setting()
        self.initialize_path()
        self.run()

    def initialize_setting(self):
        # 加载settings
        import settings
        if self.api_key:
            settings.proxy = self.proxy
        if self.proxy:
            settings.api_key = self.api_key

        # 验证
        if not hasattr(settings, 'api_key'):
            raise '请输入api_key'

    def initialize_path(self):
        # if not os.path.isabs(self.input_path):
        #     self.input_path = os.path.abspath(self.input_path)
        input_path = Path(self.input_path)

        if input_path.is_dir():
            raise '暂不支持文件夹'
            # 搜索路径下指定文件
            if self.file_extension:
                self.task = list(
                    input_path.rglob(f"*.{self.file_extension}"))
                print(
                    f"允许翻译的扩展：{self.file_extension}"
                )
            else:
                print(
                    f"允许翻译的扩展：{ALLOWED_FILE_TYPES}"
                )
                for extension in ALLOWED_FILE_TYPES:
                    self.task.extend(list(input_path.rglob(f"*.{extension}")))
            print(f"Found {len(self.task)} files to process")

        elif input_path.is_file:
            if input_path.suffix.lower() not in ALLOWED_FILE_TYPES:
                raise TypeError('不支持该类型文件')
            self.task.append(input_path)

    async def _run(self):
        total_files = len(self.task)
        for index, file_path in enumerate(self.task):
            t0 = time.time()
            await Process(path=file_path, output_path_dir=self.output_dir_path).run()
            print(
                f"Process:{file_path.name}完成-耗时{time.time()-t0}"
            )

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run())


if __name__ == '__main__':
    # fire.Fire()
    Run(input_path='./tests/examples/example2.md', output_dir_path='./tests/examples')
