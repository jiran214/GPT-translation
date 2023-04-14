本文主要介绍了pydantic的标准库类型，其支持许多来自Python标准库的常见类型。此外，当没有现有的类型适合您的目的时，您还可以使用自己的Pydantic兼容类型来实现自定义属性和验证。标准库类型包括None、bool、int、float、str、bytes、list、tuple、dict、set、frozenset、deque、datetime.date、datetime.time、datetime.datetime、datetime.timedelta、typing.Any、typing.Annotated、typing.TypeVar、typing.Union、typing.Optional等。此外，如果您有一个生成器，您可以使用`Iterable`定义其类型；如果您有一个不希望被消耗的生成器，例如无限生成器或远程数据加载器，则可以使用`Sequence`表示其类型。对于具有不同类型的模型属性，`Union`类型允许接受不同类型，而`Optional[x]`是`Union[x, None]`的简略写法。当与多个子模型一起使用`Union`时，有时需要检查并验证准确的子模型，并希望强制执行此操作。为解决这个问题，可以在每个子模型中设置相同的字段，并使用歧视性值（即Literal类型），可以更好地实现验证。
使用[注释字段语法](../schema/#typingannotated-fields)可以很方便地将`Union`和`discriminator`信息合并在一起。以下是一个示例！

！！！警告

无法将分类联合体用于仅具有单个变量的情况，例如"`Union[Cat]`"。

Python在解释时将`Union[T]`更改为`T`，因此`pydantic`无法将`Union[T]`的字段与`T`区分开来。

#### 嵌套分类联合体

一个字段只能设置一个判别键，但有时您需要合并多个判别键。在这种情况下，您始终可以使用带有`__root__`的“中间”模型并添加您的判别键。

{!.tmp_examples/types_union_discriminated_nested.md!}

### 枚举和选择

*pydantic*使用Python的标准`enum`类定义选择。

{!.tmp_examples/types_choices.md!}

### 日期时间类型

*Pydantic*支持以下[日期时间](https://docs.python.org/library/datetime.html#available-types)类型：

- `datetime`字段可以是：

  - 存在的`datetime`对象

  - `int`或`float`，假定为Unix时间，即自1970年1月1日以来的秒数（如果`> = -2e10`或`<= 2e10`），或毫秒（如果<`-2e10`或>`2e10`）

  - `str`，格式如下：

    - `YYYY-MM-DD[T]HH:MM[:SS[.ffffff]][Z或[±]HH[:]MM]]]`

    - `int`或`float`作为字符串（假定为Unix时间）

- `date`字段可以是：

  - 存在的`date`对象

  - `int`或`float`，见`datetime`

  - `str`，格式如下：

    - `YYYY-MM-DD`

    - `int`或`float`，见`datetime`

- `time`字段可以是：

  - 存在的`time`对象

  - `str`，格式如下：

    - `HH:MM[:SS[.ffffff]][Z或[±]HH[:]MM]]]`

- `timedelta`字段可以是：

  - 存在的`timedelta`对象

  - `int`或`float`，假定为秒

  - `str`，格式如下：

    - `[-] [DD] [HH：MM] SS [.ffffff]`

    - `[±] P [DD] DT [HH] H [MM] M [SS] S`（用于时间间隔的[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)格式）

{!.tmp_examples/types_dt.md!}

### Booleans

!!! 警告

自版本**v1.0**以来，解析`bool`字段的逻辑已更改。

在**v1.0**之前，`bool`解析从未失败，导致一些意外结果。下面描述了新的逻辑。

如果值不是以下之一，则标准的`bool`字段将引发`ValidationError`：

- 有效的布尔值（即`True`或`False`）

- 整数`0`或`1`

- 当转换为小写字母时为`'0'、'off'、'f'、'false'、'n'、'no'、'1'、'on'、't'、'true'或'y'、'yes'的字符串

- 一个有效的`bytes`（根据上一个规则），当解码为`str`时

!!! 注意

如果您希望使用更严格的布尔逻辑（例如只允许`True`和`False`的字段），可以使用[`StrictBool`](#strict-types)。

以下是演示这些行为的脚本：

{!.tmp_examples/types_boolean.md!}

### Callable

字段也可以是`Callable`类型：

{!.tmp_examples/types_callable.md!}

!!! 警告

Callable字段仅执行一个简单的检查，即参数是否可调用；没有对参数、其类型或返回类型进行验证。

### Type

*pydantic*支持使用`Type[T]`指定字段可能仅接受`T`的子类的类（而不是实例）。

您还可以使用`Type`指定任何类都是允许的。

{!.tmp_examples/types_type.md!}

### TypeVar

无约束支持`TypeVar`，受约束支持或已绑定。

{本文介绍了 *pydantic* 中支持的标准库类型，其中大部分都可以用于数据的字段定义，且可进行严格处理和限制值范围。当然，如果没有现有类型适合你的需求，你也可以实现你自己的 pydantic 兼容类型，这需要自定义属性和验证方式。\


## 标准库类型

*pydantic* 支持许多常见的 Python 标准库类型。如果您需要更严格的处理，请参阅**严格类型**，如果需要限制允许值的范围（例如要求为正整数），请参阅**限制类型**。

下面是 *pydantic* 中支持的一些标准库类型，具体细节可参考下面的链接：

- `None`、`type(None)`或`Literal[None]`
- `bool`
- `int`
- `float`
- `str`
- `bytes`
- `list`
- `tuple`
- `dict`
- `set`
- `frozenset`
- `deque`
- `datetime.date`
- `datetime.time`
- `datetime.datetime`
- `datetime.timedelta`
- `typing.Any`
- `typing.Annotated`
- `typing.TypeVar`
- `typing.Union`
- `typing.Optional`
- `typing.List`
- `typing.Tuple`
- `collections.namedtuple` 子类
- `typing.Dict`
- `typing.TypedDict` 子类
- `typing.Set`
- `typing.FrozenSet`
- `typing.Deque`
- `typing.Sequence`
- `typing.Iterable`
- `typing.Type`
- `typing.Callable`
- `typing.Pattern`
- `ipaddress.IPv4Address`
- `ipaddress.IPv4Interface`
- `ipaddress.IPv4Network`
- `ipaddress.IPv6Address`
- `ipaddress.IPv6Interface`
- `ipaddress.IPv6Network`
- `enum.Enum`
- `enum.IntEnum`
- `decimal.Decimal`
- `pathlib.Path`
- `uuid.UUID`

## Typing Iterables

*pydantic* 为 Python 标准库中 `typing` 类型定义复杂对象。点击[此处]中了解更多关于匹配 `typing.Iterable` 可迭代对象。

## Infinite Generators

如果您有一个生成器可以使用上文提到的的 `Sequence`，在这种情况下，生成器将被消耗并存储在模型上，其值将使用子类型 `Sequence [int]` 进行验证。

但是，如果您有一个不希望被使用的生成器（例如无限生成器或远程数据加载程序），你可以使用 `Iterable` 定义其类型。

警告：`Iterable` 域仅对其参数进行简单检查，即其可迭代且不会被消耗，无法完成对值进行的任何验证。

## Unions

`Union` 类型允许模型属性接受不同的类型。但是根据上面的说明，`Union` 有一些必要注意事项：多个类型定义下，`pydantic` 会尝试“匹配”任何类型，并使用第一个匹配到的值。快速查看当前申明的数据可能会误转换掉数据，因此应该在类型注释中首先声明最具体的类型，避免因识别低级别类型，而造成数据误判。

此外， `Optional[x]` 可以作为 `Union[x, None]` 的简写。这对于指定可以接受 `None` 作为值的必需字段很有用。

针对`Union`的应用，您还可以设置相同的字段的值，即所谓的“带标记的联合”。这样做的好处：
* 验证速度更快，因为只尝试与一个模型进行匹配。
* 失败时仅会报告一个显式错误。
* 生成的 JSON 架构实现了关联的 OpenAPI 规范。

#### 歧义联盟

当使用多个子模型的 `Union` 时，有时您确切地知道需要检查和验证哪个子模型，并希望强制执行此操作。您可以在每个子模型中设置相同的字段（称为 `my_discriminator`），其值是一个区分值。

## Discriminated Unions

当 `Union` 
使用[带注释的字段语法](../schema/#typing-annotated-fields)可以方便地组合`Union`和 `discriminator`信息。下面是一个示例！

！！！ 警告

不能仅使用单个变体（如`Union[Cat]`）使用带鉴别器的联合。

Python在解释时将`Union[T]`更改为`T`，因此`pydantic`无法将`Union [T]`的字段与`T`的字段区分开来。

#### 嵌套鉴别联合

对于字段，只能设置一个鉴别器，但有时您需要组合多个鉴别器。在这种情况下，您可以始终创建“中间”模型并添加您的鉴别器。

{!.tmp_examples/types_union_discriminated_nested.md!}

### 枚举和选择

*pydantic*使用Python的标准`enum`类来定义选择。

{!.tmp_examples/types_choices.md!}


### 日期时间类型

*Pydantic*支持以下[datetime](https://docs.python.org/library/datetime.html#available-types)类型：

* `datetime`字段可以是：

  * `datetime`，现有的`datetime`对象

  * `int`或`float`，假定为Unix时间，即自1970年1月1日以来的秒数（如果> =`-2e10`或<=`2e10`）或毫秒（如果<`-2e10`或> `2e10`）

  * `str`，以下格式有效：

    * `YYYY-MM-DD [T] HH：MM [：SS [. ffffff]] [Z或[±] HH [：] MM]]]`

    * `int`或`float`的字符串（假定为Unix时间）



* `date`字段可以是：

  * `date`, 现有的`date`对象

  * `int`或`float`，同理于`datetime`

  * `str`，以下格式有效：

    * `YYYY-MM-DD`

    * `int`或`float`，同理于`datetime`



* `time`字段可以是：

  * `time`, 现有的`time`对象

  * `str`，以下格式有效：

    * `HH：MM [：SS [. ffffff]] [Z或[±] HH [：] MM]]]`



* `timedelta`字段可以是：

  * `timedelta`, 现有的`timedelta`对象

  * `int`或`float`，假定为秒

  * `str`，以下格式有效：

     *“ [ - ] [DD] [HH：MM] SS [。ffffff]”

     * `[+] P [DD]DT [HH] H [MM]M [SS]S`（`timedelta`的[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)格式）



{!.tmp_examples/types_dt.md!}

### 布尔值

!!! 警告

自**v1.0**版本起，解析`bool`字段的逻辑已更改。

在**v1.0**之前，`bool`解析从不失败，导致一些意外的结果。

下面描述了新逻辑。

如果`bool`的值不是以下之一，则标准`bool`字段将引发`ValidationError`：

* 有效的布尔值（即`True`或`False`）

* 整数`0`或`1`

* 当转换为小写时，符合以下之一的`str`：'0'，'off'，'f'，'false'，'n'，'no'，'1'，'on'，'t'，'true'，'y'，'yes'

* 可通过上述规则解码为`str`的有效`bytes`

!!! 注意

如果您想要更严格的布尔逻辑（例如仅允许`True`和`False`的字段），可以使用[`StrictBool`](#strict-types)。

以下是演示这些行为的脚本：

{!.tmp_examples/types_boolean.md!}


### 可调用

字段也可以是类型`Callable`：

{!.tmp_examples/types_callable.md!}

!!! 警告

仅对可调用字段进行简单检查，以确定参数是否为可调用项。未执行任何参数、类型或返回类型的验证。

### Type

*pydantic*支持使用`Type[T]`指定字段仅接受作为`T`子类的类（而不是实例）。

{!.tmp_examples/types_type.md!}

您还可以使用`Type`本节介绍了一些 Pydantic 支持的自定义类型。

### URL 类型

Pydantic 定义了一些基于 URL 的类型，这些类型可以用于解析 URL，并提供了如下的属性：

- `scheme`：表示 URL 的协议部分。
- `host`：表示 URL 的主机部分。
- `host_type`：表示主机类型，可能是 `domain`、`int_domain`、`ipv4` 或 `ipv6`。
- `user`：表示 URL 的用户名部分。
- `password`：表示 URL 的密码部分。
- `tld`：表示顶级域名部分。
- `port`：表示 URL 的端口号部分。
- `path`：表示 URL 的路径部分。
- `query`：表示 URL 的查询字符串部分。
- `fragment`：表示 URL 的片段部分。

在需要进行 URL 校验时，我们可以利用这些属性进行相关操作。

### Color 类型

`Color` 类型用于存储 CSS3 规范下的颜色值，其可以以名称、16 进制值、RGB/RGBA 元组、RGB/RGBA 字符串、HSL 字符串的形式定义。`Color` 类型有一些方法，比如：

- `original`：返回 `Color` 对象原始的传入值。
- `as_named`：返回对应的颜色名称，如果 alpha 通道已设置或者不存在该颜色则返回 `as_hex`。
- `as_hex`：以 `#fff` 或 `#ffffff` 的格式返回字符串，如果 alpha 通道已设置，则返回 4 或 8 位的十六进制值。
- `as_rgb`：以 `rgb(<red>, <green>, <blue>)` 或 `rgba(<red>, <green>, <blue>, <alpha>)` 的格式返回字符串，如果 alpha 通道已设置，则返回带有 alpha 的字符串。
- `as_rgb_tuple`：以元组的形式返回 RDBA 元组，其中可以设置是否包含 alpha 通道。
- `as_hsl`：以 `hsl(<hue deg>, <saturation %>, <lightness %>)` 或 `hsl(<hue deg>, <saturation %>, <lightness %>, <alpha>)` 的格式返回字符串，如果 alpha 通道已设置，则返回带有 alpha 的字符串。
- `as_hsl_tuple`：以元组的形式返回 HSL 元组，其中可以设置是否包含 alpha 通道。

### Secret 类型

我们可以使用 `SecretStr` 和 `SecretBytes` 来表示敏感信息（如不希望在日志或追踪中显示的信息），这两个类型支持使用 `str` 或 `bytes` 字面量进行初始化，并会以 `'**********'` 或 `''` 的形式进行 JSON 转换。

### Json 类型

`Json` 类型支持从 JSON 字符串中加载 JSON 数据，可以调用 `Json` 类型中的方法进行处理。

### PaymentCardNumber 类型

`PaymentCardNumber` 类型用于验证支付卡，只要满足卡号为纯数字且满足 Luhn 算法验证，就可以通过验证。对于卡类型的分类，Pydantic 定义了类 `PaymentCardBrand`，包括四种可能的类型：`PaymentCardBrand.amex`、`PaymentCardBrand.mastercard`、`PaymentCardBrand.visa` 和 `PaymentCardBrand.other`。

### Constrained 类型

Pydantic 也定义了一些基于原生类型的确定性类型（`con*` 类型函数），可以定义数值、字符串、列表等常用类型的取值范围或长度等等限制。这些类型可以通过 `Field` 函数进一步地进行验证以及定义进一步的元数据信息。
- `min_length: int = None`: 字节数组的最小长度

- `max_length: int = None`: 字节数组的最大长度

- `strict: bool = False`: 控制类型转换



### `condate` 函数的参数

在使用 `condate` 类型函数时，可用以下参数：



- `gt: date = None`：强制日期大于设置的值

- `ge: date = None`：强制日期大于或等于设置的值

- `lt: date = None`：强制日期小于设置的值

- `le: date = None`：强制日期小于或等于设置的值



## 严格类型



您可以使用 `StrictStr`、`StrictBytes`、`StrictInt`、`StrictFloat` 和 `StrictBool` 类型来防止从兼容类型的强制类型转换。

仅当经过验证的值是相应类型或是该类型的子类型时，这些类型才能通过验证。

此行为通过 `ConstrainedStr`、`ConstrainedBytes`、`ConstrainedFloat` 和 `ConstrainedInt` 类的 `strict` 字段公开，并且可以与许多复杂验证规则结合使用。



以下注意事项适用：



- `StrictBytes` 类型（以及 `ConstrainedBytes` 的 `strict` 选项）将接受 `bytes` 和 `bytearray` 类型。

- `StrictInt` 类型（以及 `ConstrainedInt` 的 `strict` 选项）将不接受 `bool` 类型，尽管在 Python 中 `bool` 是 `int` 的子类。其他子类将可以工作。

- `StrictFloat` 类型（以及 `ConstrainedFloat` 的 `strict` 选项）将不接受 `int` 类型。



{!.tmp_examples/types_strict.md!}



## ByteSize



您可以使用 `ByteSize` 数据类型将字节串表示转换为原始字节，并打印可读性更好的字节版本。



!!! info

    注意，`1b` 将被解析为 "1 字节" 而不是 "1 位"。



{!.tmp_examples/types_bytesize.md!}



## 自定义数据类型



您也可以定义自己的数据类型。有几种实现方法。



### 带有 `__get_validators__` 的类



可以使用带有 classmethod `__get_validators__` 的自定义类。调用该类方法将获得一个验证器，用于解析和验证输入数据。



!!! tip

    这些验证器的语义与 [Validators](validators.md) 相同，您可以声明参数 `config`、`field` 等。



{!.tmp_examples/types_custom_type.md!}



可以使用 [`constr(regex=...)`](#constrained-types) 实现类似的验证，除了值不会用空格格式化以外，模式将包括完整的模式，并返回值将是普通字符串。



有关模型架构生成的更多详细信息，请参见 [schema](schema.md)。



### 允许任意类型



您可以使用 [模型配置](model_config.md) 中的 `arbitrary_types_allowed` 配置允许任意类型。



{!.tmp_examples/types_arbitrary_allowed.md!}



### 泛型类作为类型



!!! warning

    这是一项高级技术，在开始时可能不需要。在大多数情况下，您可能只需要标准的 *pydantic* 模型。



您可以使用 [通用类](https://docs.python.org/3/library/typing.html#typing.Generic) 作为字段类型，并根据“类型参数”（或子类型）执行自定义验证，使用 `__get_validators__`。



如果您使用作为子类型的通用类具有 classmethod `__get_validators__`，则不需要使用 `arbitrary_types_allowed` 也可以工作。



因为您可以声明接收当前 `field` 的验证器，所以您可以提取来自通用类类型参数的 `sub_fields`，并对数据进行验证。



{!.tmp_examples/types_generics.md!}