"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: schema.py
 @DateTime: 2023/4/13 20:09
 @SoftWare: PyCharm
"""
from typing import List, Union, Dict

from pydantic import BaseModel


class GPT35Params(BaseModel):
    model: str = "gpt-3.5-turbo"
    # model: str = Field(..., description="This field is required")  # 模型 ID，只支持 gpt-3.5-turbo 和 gpt-3.5-turbo-0301
    messages: List  # 聊天格式的输入消息列表
    temperature: float = 1.0  # 采样温度，0~2 范围内的浮点数。较大的值会使输出更随机，较小的值会使输出更确定
    top_p: float = 1.0  # 替代采样温度的另一种方式，称为 nucleus 采样，只考虑概率质量排名前 top_p 的 token。范围在 0~1 之间
    n: int = 1  # 每个输入消息要生成的聊天完成选项数量，默认为 1
    stream: bool = False  # 是否启用流式输出
    stop: Union[str, List[str], None] = None  # 最多 4 个序列，当 API 生成的 token 包含任意一个序列时停止生成
    max_tokens: int = None  # 默认inf   # 生成的答案中允许的最大 token 数量，默认为 (4096 - prompt tokens)
    presence_penalty: float = None  # 0.0   # -2.0 到 2.0 之间的数字，用于基于新 token 是否出现在已有文本中惩罚模型。正数值会增加模型谈论新话题的可能性
    frequency_penalty: float = None  # 0.0   # -2.0 到 2.0 之间的数字，用于基于新 token 是否在已有文本中的频率惩罚模型。正数值会降低模型直接重复相同文本的可能性
    logit_bias: Dict[str, float] = None  # 一个将 token ID 映射到关联偏差值（-100 到 100）的 JSON 对象，用于修改指定 token 出现在完成中的可能性
    user: str = None  # 表示最终用户的唯一标识符，可帮助 OpenAI 监视和检测滥用
