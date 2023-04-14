"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: process.py
 @DateTime: 2023/4/14 1:20
 @SoftWare: PyCharm
"""
import asyncio
import os.path
import time
from pathlib import Path

import settings
from openAi import request_openai
from prompt import TokenCounter


class Process:

    def __init__(self, path: Path, output_path_dir):
        print('Process开始运行...')
        self.path = path
        self.output_path_dir = output_path_dir

    def iter_file(self):
        tc = TokenCounter()
        with open(self.path.absolute(), mode="r", encoding='utf-8') as fp:
            tmp_chunk = None
            # lines = fp.readlines()
            while 1:
                if tmp_chunk:
                    chunk = tmp_chunk
                    tmp_chunk = None
                else:
                    chunk = fp.readline()
                    if not chunk:
                        if tc.text_list:
                            yield tc.text_list
                            yield None
                        break

                status = tc.add_text(chunk)
                if not status:
                    tmp_chunk = chunk
                    yield tc.text_list
                    tc.clear()

    def get_new_path(self):
        return os.path.join(self.output_path_dir, f'{self.path.stem}_translated.md')

    async def run(self):

        new_path = self.get_new_path()

        with open(new_path, mode="a", encoding='utf-8') as fp:
            # 获取上次进度
            ...
            # 写入
            tasks = []
            line_num = 0
            for line_list in self.iter_file():
                if line_list is not None:
                    print(f'Process成功获取文本-行数:{len(line_list)}')
                    tasks.append(
                        asyncio.create_task(request_openai(system_content='翻译以下内容，保持原格式', user_content='\n'.join(line_list)))
                    )
                    line_num += len(line_list)

                if len(tasks) == settings.concurrent_request or (line_list is None and tasks):
                    # print(f'Process开始请求openai-发起请求行数:{line_num}')
                    t0 = time.time()
                    res = await asyncio.gather(
                        *tasks
                    )
                    lines = []
                    tks = []
                    for line, tk in res:
                        lines.append(line)
                        tks.append(tk)
                    tasks = []
                    print(f'Process成功请求openai-消耗token:{sum(tks)}-耗时:{time.time()-t0}')
                    time.sleep(0.5)
                    fp.write('\n'.join(lines))
                    print(f'Process成功写入-行数:{line_num}')
                    line_num = 0


class PDFProcess:
    ...
