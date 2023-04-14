"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: test_run.py
 @DateTime: 2023/4/14 16:54
 @SoftWare: PyCharm
"""
import os

import pytest

from main import Run


def test_settings():
    with pytest.raises(TypeError):
        Run(input_path='./test_counter.py')

    Run(input_path='./examples/example_pydantic_doc.md', output_dir_path='./examples')