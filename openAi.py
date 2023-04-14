"""
 @Author: jiran
 @Email: jiran214@qq.com
 @FileName: openAi.py
 @DateTime: 2023/4/13 19:59
 @SoftWare: PyCharm
 封装openai库，关闭ssl实现代理
"""
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

import aiohttp
import openai
import urllib3

import requests
import requests.adapters
from aiohttp import TCPConnector
from openai import api_requestor

import settings
from schema import GPT35Params

proxies = {
    'http': f'http://{settings.proxy}/',
    'https': f'http://{settings.proxy}/'
}

openai.api_key = settings.api_key


def make_session() -> requests.Session:
    s = requests.Session()
    s.verify = False
    s.proxies = proxies
    urllib3.disable_warnings()
    s.trust_env = False
    s.mount(
        "https://",
        requests.adapters.HTTPAdapter(max_retries=2),
    )
    return s


@asynccontextmanager
async def aiohttp_session() -> AsyncIterator[aiohttp.ClientSession]:
    async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
        yield session


# 猴子补丁 关闭ssl验证 添加代理
if settings.proxy:
    # api_requestor._make_session = make_session
    openai.proxy = proxies['http']
    setattr(api_requestor._thread_context, 'session', make_session())
    api_requestor.aiohttp_session = aiohttp_session


async def request_openai(system_content: str, user_content:str, model="gpt-3.5-turbo"):
    try:
        response = await openai.ChatCompletion.acreate(**GPT35Params(
            model=model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            temperature=1,
            # max_tokens
        ).dict(exclude_defaults=False, exclude_none=True))
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        print(f'请求错误{e}')


if __name__ == '__main__':
    # p = request_openai(system_content='翻译以下内容，保持原格式', user_content='\n'.join(['1', '2', '3']))
    p = request_openai(
        system_content='翻译以下内容，保持原格式',
        user_content="""    types (because Python treats these definitions as singletons).
    For example, `Dict[str, Union[int, float]] == Dict[str, Union[float, int]]` with the order based on the first time it was defined.
    Please note that this can also be [affected by third party libraries](https://github.com/pydantic/pydantic/issues/2835)
    and their internal type definitions and the import orders.

As such, it is recommended that, when defining `Union` annotations, the most specific type is included first and
followed by less specific types.

In the above example, the `UUID` class should precede the `int` and `str` classes to preclude the unexpected representation as such:

{!.tmp_examples/types_union_correct.md!}

!!! tip
    The type `Optional[x]` is a shorthand for `Union[x, None]`.

    `Optional[x]` can also be used to specify a required field that can take `None` as a value.
    
    See more details in [Required Fields](models.md#required-fields).

#### Discriminated Unions (a.k.a. Tagged Unions)

When `Union` is used with multiple submodels, you sometimes know exactly which submodel needs to
be checked and validated and want to enforce this.
To do that you can set the same field - let's call it `my_discriminator` - in each of the submodels
with a discriminated value, which is one (or many) `Literal` value(s).
For your `Union`, you can set the discriminator in its value: `Field(discriminator='my_discriminator')`.

Setting a discriminated union has many benefits:

- validation is faster since it is only attempted against one model
- only one explicit error is raised in case of failure
- the generated JSON schema implements the [associated OpenAPI specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#discriminatorObject)

{!.tmp_examples/types_union_discriminated.md!}

!!! note
    Using the [Annotated Fields syntax](../schema/#typingannotated-fields) can be handy to regroup
    the `Union` and `discriminator` information. See below for an example!

!!! warning
    Discriminated unions cannot be used with only a single variant, such as `Union[Cat]`.

    Python changes `Union[T]` into `T` at interpretation time, so it is not possible for `pydantic` to
    distinguish fields of `Union[T]` from `T`.

#### Nested Discriminated Unions"""
    )
    print(asyncio.run(p))