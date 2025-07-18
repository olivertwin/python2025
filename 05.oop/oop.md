# Объектно-ориентированное программирование

- [Объектно-ориентированное программирование](#объектно-ориентированное-программирование)
  - [Обзор](#обзор)
  - [Терминология](#терминология)
  - [Создание класса](#создание-класса)
  - [Создание экземпляра класса](#создание-экземпляра-класса)
  - [Атрибуты](#атрибуты)
  - [Переменная класса](#переменная-класса)
  - [Методы](#методы)
  - [Магические / dunder методы](#магические--dunder-методы)
  - [`__init__`, `__new__`](#__init__-__new__)
  - [Основные концепции ООП](#основные-концепции-ооп)
    - [Наследование](#наследование)
      - [`super`](#super)
      - [Method Resolution Order (MRO)](#method-resolution-order-mro)
    - [Инкапсуляция](#инкапсуляция)
    - [`_` в именах объектов](#_-в-именах-объектов)
    - [Полиморфизм](#полиморфизм)
    - [Абстракция](#абстракция)
    - [Композиция и агрегация](#композиция-и-агрегация)
  - [Изменение поведения атрибутов/методов](#изменение-поведения-атрибутовметодов)
    - [`property`](#property)
    - [`classmethod`](#classmethod)
    - [`staticmethod`](#staticmethod)
  - [dunder методы и атрибуты](#dunder-методы-и-атрибуты)
    - [`__str__`](#__str__)
    - [`__repr__`](#__repr__)
    - [`__dict__`](#__dict__)
    - [`__slots__`](#__slots__)
    - [`__eq__`](#__eq__)
    - [`__hash__`](#__hash__)
    - [`__contains__`](#__contains__)
    - [`__enter__` / `__exit__`](#__enter__--__exit__)
    - [`__call__`](#__call__)

## Обзор

Подходы к написанию программы на Python можно разделить на две категории:

- функциональное программирование: код строится вокруг функций, которые в большей части зависят друг от друга. Если меняем какую-нибудь функцию, то остальной код так же, скорее всего потребует изменений.
- объектно-ориентированное программирование (ООП): программа строится вокруг объектов, внутри которых лежат собственные функции и данные. Так выстраивается иерархическая структура. Объекты независимы друг от друга, и если мы меняем что-то внутри объекта, то это никак не должно отражаться на остальных объектах.

## Терминология

Некоторые термины ООП, которыми будем пользоваться в ближайшее время:

- класс (class): языковая конструкция описывающая какой-либо тип данных. Класс это шаблон для создания объектов.
- экземпляр класса (instance): объект являющийся представителем класса, конкретная реализация.
- метод (method): функция внутри класса, может описывать какие-либо действия.
- атрибут (instance attribute/variable): переменные внутри класса.
- переменная класса (class attribute/variable): переменные класса, общие для всех экземпляров класса

## Создание класса

Классы создаются через ключевое слово `class`, за которым указывается имя класса.

```python
class Device:
    """класс каких-то устройств"""
```

Имена классов в Python принято писать в PascalCase нотации.

> [!NOTE]
>
> - `PascalCase` - слитное написание, каждое слово с большой буквы: NumberOfDevices
> - `camelCase` - слитное написание, каждое следующее слово с большой буквы: numberOfDevices
>
> Акронимы можно оставлять заглавными (pep8): MACAddress <-> MacAddress. VoiceVLAN <-> VoiceVlan

```python
In [2]: Device?
Init signature: Device()
Docstring:      класс каких-то устройств
Type:           type
Subclasses:     
```

из примера выше:

- `Init signature: Device()`: - как выглядит инициализация экземпляра класса. Мы не настраивали конструктор, поэтому создание объекта происходит конструкцией `Device()`, без аргументов.
- `Docstring: класс каких-то устройств`: docstring класса, работает так же, как и у функций
- `Type:           type`: type - тип "обычных" классов, ABCMeta - абстрактных классов

## Создание экземпляра класса

Создание экземпляра класса похоже на вызов функции, поэтому при неудачном выборе названий и не следовании pep8 можно спутать создание экземпляра класса `ClassName()` с вызовом функции `func_name()`.

Общие рекомендации:

- имена функций обычно пишут в snake_case нотации, а имена классов в PascalCase
- имена функций это обычно глагольные конструкции: get_device, parse_result, connect. Имена классов - существительные: Device, ResultParser, DeviceCollector

```python
my_device = Device()

my_device
# >>> <__main__.Device at 0x105487680>

type(my_device)
# >>> __main__.Device

isinstance(my_device, Device)
# >>> True
```

## Атрибуты

Атрибуты это переменные в экземпляре класса. Определение атрибутов является динамическим процессом. Так делать не рекомендуется, но python это позволяет.

```python
class Device:
    pass

device = Device()
device.ip = "192.168.1.1"
device.hostname = "rt1"

print(f"{device.hostname=}: {device.ip=}")
# >>> device.hostname='rt1': device.ip='192.168.1.1'
```

## Переменная класса

Переменная класса это обычная переменная, только объявлена на уровне класса, вне его методов и не привязана к экземпляру класса (т.е. не связана с `self`). Переменные класса доступны как при обращении через сам класс, так и при обращении через экземпляры класса

```python
class Cisco:
    platform = "cisco_iosxe"

Cisco.platform
# >>> 'cisco_iosxe'

device = Cisco()
device.platform
# >>> 'cisco_iosxe'
```

## Методы

Так как метод класса это функция, то и определяется он как функция, только на уровне класса.

```python
class Device:
    def connect(self) -> None:
        print("connecting...")
        print("done")


my_device = Device()

my_device.connect()
# >>> connecting...
# >>> done
```

Важные отличия от обычных функций:

- метод непосредственно связан с объектом класса, поэтому вызывается метод через точечную нотацию. Отдельно/независимо от объекта вызвать метод нельзя.
- в методе есть один обязательные атрибут, всегда идет на первом месте, обычно обозначается как `self` - ссылка на сам объект, через этот `self` внутри функции можно получить доступ к атрибутам объекта или другим методам.

Когда метод вызывается в коде, то на месте `self` ничего не пишется: создается метод `def connect(self) -> None:` - один обязательный позиционный атрибут, но вызывается в коде этот атрибут как `my_device.connect()` - без аргументов.

Внутри методов через ссылку `self` на сам объект можно обращаться к другим атрибутам и методам объекта:

```python
class Device:
    def connect(self) -> None:
        print("connection was established")

    def disconnect(self) -> None:
        print("connection was closed")

    def get_version(self) -> str:
        self.connect()
        version = "v1"
        self.version = version
        self.disconnect()
        return version


device = Device()
version = device.get_version()
print(version)

# >>> connection was established
# >>> connection was closed
# >>> v1
```

> `self` это соглашение, можно использовать любое другое имя (например `this`), но это усложнит чтение кода.

В примере

```python
    def get_version(self) -> str:
        self.connect()
        version = "v1"
        self.version = version
        self.disconnect()
        return version
```

- `version` - переменная в локальное области видимости функции
- `self.version` - переменная в экземпляре класса (атрибут)

Несмотря на два похожих названия это две разные переменные. Одна (version) пропадет после завершения работы метода, вторая (self.version) будет жить пока живет сам экземпляр класса и будет доступна через self.version из других методов.

Как и в случае атрибутов, методы могут быть добавлены динамически (как к самому классу, так и к объекту класса), но это более сложный процесс, и делать так не рекомендуется. Пример добавления метода в объект класса:

```python
import types

class Device:
    pass

device = Device()
device.ip = "192.168.1.1"
device.hostname = "rt1"

def show_info(self) -> None:
    print(f"{self.hostname}: {self.ip}")

device.show_info = types.MethodType(show_info, device)
device.show_info()
# >>> rt1: 192.168.1.1
```

## Магические / dunder методы

У любого класса, даже пустого (как в примере выше) есть специальные служебные методы, которые предоставляют стандартный интерфейс взаимодействия с объектом.

```python
dir(my_device)
 
['__class__',
 '__delattr__',
 '__dict__',
 '__dir__',
 '__doc__',
 '__eq__',
 '__format__',
 '__ge__',
 '__getattribute__',
 '__getstate__',
 '__gt__',
 '__hash__',
 '__init__',
 '__init_subclass__',
 '__le__',
 '__lt__',
 '__module__',
 '__ne__',
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 '__weakref__']
```

Специальные методы начинаются и заканчиваются двойным подчеркиванием `__`, отсюда и название "double underscore", сокращенно: "dunder".

Например, мы можем получить строковое представление экземпляра класса конструкций

```python
str(my_device)
```

Которая, на самом деле, является результатом работы dunder метода `__str__`:

```python
my_device.__str__()
```

Или функция `dir(my_device)` это результат работы `my_device.__dir__()`

## `__init__`, `__new__`

Создании объекта класса происходит в два этапа:

- создание экземпляра класса, реализуется через `__new__`
- инициализация экземпляра класса, реализуется через `__init__`

Т.е. что бы получить экземпляр класса, python сначала создает его (выделение памяти, создание ссылок и пр), и потом настраивает его (задание значений переменных или другие действия).

`__new__` более сложная конструкция, которой можно управлять процессом создания экземпляра класса.

`__init__` часто называют конструктором класса (хотя технически конструктор это `__new__`), и это тот метод, который в основном используется разработчиком для настройки экземпляра класса.

```python
class Device:
    def __init__(self, hostname: str, ip: str) -> None:
        self.hostname = hostname
        self.ip = ip
    
    def show_info(self) -> None:
        print(f"{self.hostname}: {self.ip}")


device = Device("rt1", "192.168.1.1")

print(f"{device.hostname}: {device.ip}")
# >>> rt1: 192.168.1.1
device.show_info()
# >>> rt1: 192.168.1.1
```

Теперь для создания объекта нужно указывать параметры (строка Init signature) hostname и ip:

```python
In [17]: Device?
Init signature: Device(hostname: str, ip: str) -> None
Docstring:      <no docstring>
Type:           type
Subclasses:     
```

Как и другие методы, у `__init__` есть один обязательный аргумент - ссылка на объект класса, `self`. Остальные параметры зависят от конкретного описания и назначения класса, и могут отсутствовать вовсе.

## Основные концепции ООП

### Наследование

Наследование позволяет создавать новый класс на основе существующего. Новый класс (наследник) наследует атрибуты и методы базового класса (родителя), а также может добавлять новые или переопределять существующие.

```python
class Device:
    def __init__(self, hostname: str, ip: str) -> None:
        self.hostname = hostname
        self.ip = ip

    def show_info(self) -> None:
        print(f"{self.hostname=}, {self.ip=}")


class Switch(Device):
    def add_vlan(self, vlan_id: int) -> None:
        print(f"adding vlan {vlan_id}")


class Router(Device):
    def __init__(self, hostname: str, ip: str, platform: str) -> None:
        super().__init__(hostname, ip)
        self.platform = platform

    def show_info(self) -> None:
        print(f"{self.hostname=}, {self.ip=}, {self.platform=}")


sw = Switch("rt1", "192.168.1.1")
rt = Router("rt1", "192.168.1.1", "xe")

sw.show_info()
# >>> self.hostname='rt1', self.ip='192.168.1.1'

rt.show_info()
# >>> self.hostname='rt1', self.ip='192.168.1.1', self.platform='xe'
```

Функция `super()` обеспечивает выполнение указанного метода у родительских классов, таким образом можно дополнить поведение, а не полностью его переписывать.

#### `super`

```python
class Device:
    def __init__(self, hostname: str, ip: str) -> None:
        print("Device init")
        self.hostname = hostname
        self.ip = ip

    def show_info(self) -> None:
        print(f"{self.hostname=}, {self.ip=}")


class Cisco:
    def __init__(self) -> None:
        print("Cisco init")
        self.vendor = "cisco"


class Router(Device, Cisco):
    def __init__(self, hostname: str, ip: str, platform: str) -> None:
        print("Router init")
        super().__init__(hostname, ip)
        self.platform = platform


rt = Router("rt1", "192.168.1.1", "xe")
# >>> Router init
# >>> Device init
```

В примере класс `Router` имеет два родительских класса: `Device` и `Cisco`. При этом в каждом классе есть конструктор `__init__`. Использование функции `super()` позволяет вызвать указанный метод у родителя. Какой именно метод будет вызван (у `Device` или у `Cisco`) определяется алгоритмом
Method Resolution Order (MRO).

#### Method Resolution Order (MRO)

Порядок разрешения методов (но справедлив и для атрибутов) - это порядок просмотра классов-родителей на предмет наличия в них нужного метода (атрибута), как только нужный метод (атрибут) найден, поиск останавливается.

```python
Router.mro()
# >>> [__main__.Router, __main__.Device, __main__.Cisco, object]
```

MRO в комбинации с `super()` позволяет получить доступ к методу у ближайшего в цепочки иерархии родителя.

### Инкапсуляция

Определение инкапсуляции размыто и в разных источниках дается по разному (а где-то и вовсе инкапсуляция не рассматривается как принцип ООП). На инкапсуляцию можно посмотреть с двух сторон:

- механизм сокрытия деталей реализации класса от других объектов, т.е. то, как подробности реализации это дело только класса и внешнему потребителю это знать не нужно.
- механизм для ограничения доступа к структурам класса из вне.

```python
class Device:
    def __init__(self) -> None:
        self._uptime = 0
        self.__hostname = "r1"
    
    def get_hostname(self) -> str:
        return self.__hostname


d = Device()

print(d._uptime)
d._uptime = 1
print(d._uptime)

print(d.get_hostname())
print(d.__hostname)
```

Имена атрибутов/методов с одинарным подчеркиванием `_` в начале являются приватными, но к ним все еще можно получить доступ снаружи для чтения/записи. Это соглашение между разработчиками, что если атрибут/метод называется с `_`, то не стоит его вызывать напрямую, это внутренние данные. Многие линтеры будут ругаться, если приватные атрибуты/методы будут использоваться вне класса.

Имена с двойным подчеркиванием `__` в начале являются приватными и к ним уже нельзя получить доступ снаружи стандартным способом. Но все равно, эти переменные/методы могут быть получены через конструкцию `<экземпляр класса>._<имя класса><имя переменной>`

```python
d._Device__hostname
'r1'
```

Приватные атрибуты/методы могут использоваться когда они являются служебными и не предназначены для внешнего использования (например какие-нибудь счетчики, промежуточные аргументы, служебные методы и прочее), а так же, когда разработчик хочет предоставить отдельный интерфейс для работы с этими атрибутами. Например есть атрибут у класса `ip`, нужно обеспечить его валидацию при установки.

```python
from netaddr import IPAddress


class Device:
    def __init__(self) -> None:
        self._ip = "0.0.0.0"

    def ip(self) -> str:
        return self._ip

    def set_ip(self, ip: str) -> None:
        _ = IPAddress(ip)
        self._ip = ip


d = Device()

print(d.ip())
d.set_ip("192.168.1.1")
print(d.ip())

d.set_ip("wrong string")
```

### `_` в именах объектов

1. имя вида `var`: используется для определения обычных объектов, которые полностью публичны, их можно менять/наследовать. Дочерний класс получает полный доступ и может читать/изменять.

    ```python
    class Parent:
        def __init__(self):
            self.var = 100

    class Child(Parent):
        def __init__(self):
            super().__init__()
            self.var = 200  # тут перепишем значение, установленное в parent 

    c = Child()
    c.var = 300  # а тут доступ извне класса
    ```

2. защищенное (protected) имя `_var`: на уровне соглашения (не интерпретатора) принято, что так именуются внутренние объекты класса (может быть не только аргументом, но и методом) и к ним не стоит обращаться извне класса. Но технически (с т.з. интерпретатора) нет никакой разницы между `var` и `_var` - protected переменные наследуются как есть и без ограничений и их можно (но не стоит) читать/изменять извне класса. Линтеры могут отслеживать такие обращения и выдавать ошибку при их использовании. Например для Ruff это [SLF001](https://docs.astral.sh/ruff/rules/private-member-access/).

    ```python
    class Parent:
        def __init__(self) -> None:
            self._var = 100


    class Child(Parent):
        def __init__(self) -> None:
            self._var = 200
            print(f"до super init: {self._var=}")
            assert self._var == 200
            # __init__ родителя вызывается после инициализации _var в Child
            # поэтому значение переписывается тем, что задается в Parent
            super().__init__()
            print(f"после super init: {self._var=}")
            assert self._var == 100


    if __name__ == "__main__":
        c = Child()
        c._var = 300          # ruff: SLF001 Private member accessed: `_var`
        assert c._var == 300  # ruff: SLF001 Private member accessed: `_var`
    ```

3. приватное имя (private) `__var`: на уровне интерпретатора имя подвергается искажению и к нему добавляется префикс вида `_ИмяРодительскогоКласса`, поэтому напрямую доступа извне класса к переменной уже не будет. Но все еще возможно обратиться через `_ИмяРодительскогоКласса__var` (хотя это и нарушение соглашений)

    ```python
    class Parent:
        def __init__(self) -> None:
            self.__var = 100


    class Child(Parent):
        def __init__(self) -> None:
            super().__init__()
            self.__var = 200
            assert self._Parent__var == 100
            assert self.__var == 200


    if __name__ == "__main__":
        c = Child()

        c._Parent__var = 300
        assert c._Parent__var == 300

        c._Child__var = 400
        assert c._Child__var == 400
    ```

    > если имена объектов (не важно, класса/функции/переменной) начинаются на `_` (т.е. `_VAR`, `__VAR`, `___VAR` и т.д.), то при импорте через звездочку вида `from my_module import *`, они пропускаются (импортированы не будут). При этом сохраняется возможность прямого явного импорта вида `from my_module import _VAR`, либо такие объекты должны быть явно добавлены в `__all__`, который определяет список того, что будет импортировано из модуля при использовании импорта через звездочку:
    >
    > ```python
    > __all__ = (
    >     "PUBLIC_VAR",
    >     "_PROTECTED_VAR",
    >     "__PRIVATE_VAR",
    > )
    > PUBLIC_VAR = 1
    > _PROTECTED_VAR = 2
    > __PRIVATE_VAR = 3
    > ```

4. имя с `_` в конце `var_`: является обычной переменной с теми же правилами, что и просто `var`. Такое именование используется когда нужно избежать конфликта имен с уже существующими объектами, например

    ```python
    def sum_(a, b):
        return a + b

    class MyClass:
        def __init__(self):
            self.list_ = []
    ```

5. магическое имя `__var__`: используется в Python для определения специальных служебных методов/переменных (магические/dunder методы). Не следует создавать собственные имена для таких объектов (если, конечно, не разрабатывается низкоуровневая библиотека):
    - это может привести к конфликту имен в будущем
    - dunder-методы ассоциируются с магией python, поэтому кастомный `__my_custom_method__` может запутать других разработчиков

    ```python
    class MyClass:
        def __init__(self): ...  # переопределяем init - ОК
        def __my_custom_method__(self): ...  # создаем свой dunder-метод - не ОК
    ```

6. мусорная переменная `_`: переменная для игнорирования ненужных значений, например в циклах или при распаковки.

    ```python
    for _ in range(5):
        do_smth()
    ```

7. соглашение для функций перевода `_`: кроме использования в качестве мусорной переменной, `_` так же может использоваться как имя функции для перевода/локализации текста (i18n/l10n), так как это самый короткий алиас, который улучшает читаемость кода. Это соглашение, которое обычно придерживаются при разработки приложений.

    ```python
    from django.http import HttpResponse
    from django.utils.translation import gettext as _

    def my_view(request):
        output = _("Welcome to my site.")
        return HttpResponse(output)
    ```

### Полиморфизм

Полиморфизм - разное поведение одного и того же метода в разных классах. Например

```python
1 + 2 + 3
# >>> 6

"some" + " " + "string"
# >>> 'some string'
```

При работе с числами `+` ведет себя как арифметическое сложение, а при работе со строками - как конкатенатор. Т.е. `+` обладает полиморфизмом в зависимости от того, с какими данными работает.

Или функция `len`: может работать с различными типами данных (строка, список, словарь).

```python
class CiscoNXOS:
    def get_version(self) -> str:
        print("getting version from NX-OS via NETCONF")
        return "1.2.3"

class CiscoIOS:
    def get_version(self) -> str:
        print("getting version from IOS via SSH")
        return "3.2.1"

devices = [
    CiscoNXOS(),
    CiscoIOS(),
]
for device in devices:
    print("-" * 10)
    print(device.get_version())

# >>> ----------
# >>> getting version from NX-OS via NETCONF
# >>> 1.2.3
# >>> ----------
# >>> getting version from IOS via SSH
# >>> 3.2.1
```

Без полиморфизма нужно было бы проверять класс устройства (CiscoNXOS vs CiscoIOS) и в зависимости от этого вызывать получать результат работы метода тем или иным способом.

### Абстракция

Позволяет использовать шаблон-заготовку, в которую выносятся все основные компоненты (атрибуты/методы). На основе этой заготовки в дальнейшем создаются конечные классы с минимальным числом изменений. Например, мы можем сделать абстрактный класс, в котором определим сигнатуры методов для обеспечения полиморфизма, а детали реализации этих методов будут определены в классах-потомках.

### Композиция и агрегация

Два принципа проектирования классов, которые описывают отношения "часть-целое" между объектами. Оба подхода позволяют создавать сложные объекты из более простых, но с разным принципом владения.

Композиция - это сильная форма связи:

- часть не может существовать без целого
- часть создается и уничтожается вместе с целым
- часть принадлежит только одному целому

Агрегация - это слабая форма связи:

- часть может существовать независимо от целого
- часть может принадлежать разным целым в разное время
- часть создается и уничтожается независимо от целого

## Изменение поведения атрибутов/методов

В функциональном программировании существует возможность менять поведение функций с помощью декораторов. Для методов так же возможно применять декораторы такие же, как и для функций, но кроме этого существует ряд декораторов, которые меняют поведение особым образом, который применим только к ООП.

### `property`

Декоратор `@property` позволяет обращаться к методу класса, как к атрибуту (без круглых скобок и без передачи аргументов). Это может быть применено, когда есть необходимость сделать "динамические" атрибуты, например:

```python
from random import randint

class Switch:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    @property
    def free_interface_count(self) -> int:
        # подключаемся к устройству/обращаемся в базе и вычисляем
        # количество свободных портов
        print("...делаем вычисления...")
        return randint(10, 20)


sw = Switch("192.168.1.1", "sw1")

print(sw.free_interface_count)
# >>> ...делаем вычисления...
# >>> 20
```

Так же `@property` может быть использован, когда необходимо делать проверку данных при установки значения в атрибут, или модификацию данных при получении значения. Т.е. для работы с приватными атрибутами (`_<attr-name>`). Выше был похожий пример с валидацией ip, с использованием `@property` эта задача решается более правильно:

```python
from netaddr import IPAddress

class Switch:
    def __init__(self, ip: str) -> None:
        self._ip: str
        self.ip = ip

    @property
    def ip(self) -> str:
        # return self._ip
        return f"device ip address: {self._ip}"

    @ip.setter
    def ip(self, ip: str) -> None:
        _ = IPAddress(ip)
        self._ip = ip

    @ip.getter
    def ip(self) -> str:
        return self._ip

sw = Switch("192.168.1.2")
# >>> device ip address: 192.168.1.2
sw.ip = "500.1.1.1"
# >>> AddrFormatError: failed to detect a valid IP address from '500.1.1.1'
```

### `classmethod`

Декоратор `@classmethod` меняет метод таким образом, что он начинает получать первым аргументом не ссылку на экземпляр класса (`self`), а ссылку на сам класс: `cls` (`cls` это так же соглашение в именовании, как и `self`. И имя может быть любым, но это затруднит понимание кода). Таким образом метод становится независимым от экземпляра класса, но в то же время имеет доступ к переменным класса.

Методы класса доступны как в самом классе, так и в экземпляре класса. Могут применяться когда явно нужно отвязать метод от экземпляра класса, или в классах-помощниках, когда для работы которых не требуется создавать экземпляр класса, но требуется некоторый функционал, который предоставляет класс.

```python
from typing import Iterator


class ConfigParser:
    JUNK_LINES = ["!", "exit-address-family"]

    @classmethod
    def get_config(cls, config: str) -> Iterator[str]:
        for line in config.strip().splitlines():
            if line.strip() in cls.JUNK_LINES:
                continue
            else:
                yield line

    @classmethod
    def get_patch(cls, config: str) -> Iterator[str]:
        last_space = 0
        for line in config.strip().splitlines():
            current_space = len(line) - len(line.lstrip())
            if current_space < last_space:
                last_space = current_space
                yield "exit"
            last_space = current_space
            if line.strip() in cls.JUNK_LINES:
                continue
            else:
                yield line.strip()

config = """
ip forward-protocol nd
no ip http server
!
interface Vlan1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
router bgp 64512
 bgp router-id 192.168.1.1
 bgp log-neighbor-changes
 !
 address-family ipv4
  redistribute connected route-map LAN
 exit-address-family
 !
 address-family vpnv4 unicast
  neighbor 1.2.3.4 activate
 exit-address-family
!
line vty 0 4
 password cisco
!
""".strip()

for line in ConfigParser.get_patch(config):
    print(line)

# >>> ip forward-protocol nd
# >>> no ip http server
# >>> interface Vlan1
# >>> ip address 192.168.1.1 255.255.255.0
# >>> no shutdown
# >>> exit
# >>> router bgp 64512
# >>> bgp router-id 192.168.1.1
# >>> bgp log-neighbor-changes
# >>> address-family ipv4
# >>> redistribute connected route-map LAN
# >>> exit
# >>> address-family vpnv4 unicast
# >>> neighbor 1.2.3.4 activate
# >>> exit
# >>> exit
# >>> line vty 0 4
# >>> password cisco
# >>> exit
```

В примере для работы не требуется создавать экземпляр класса `ConfigParser`, с другой стороны в классе могут существовать классовые переменные (константы, настройки и пр), которые используются в методах, поэтому этим методам нужен доступ к классу, который обеспечивается через `cls`.

### `staticmethod`

Декоратор `@staticmethod` позволяет отвязать метод как от экземпляра класса (`self`), так и от самого класса (`cls`). По сути такой метод становится обычной функцией, которая не имеет доступа ни к `self`, ни к `cls` и может быть вообще записана как отдельная самостоятельная функция. Но иногда удобно сгруппировать такие функции в класс, например что бы не потерять её, или удобстве импорта, или для наследования и пр.

## dunder методы и атрибуты

### `__str__`

Используется для строкового представления экземпляра класса.

```python
class Foo:
    pass

f = Foo()
str(f)
# >>> '<__main__.Foo object at 0x105737710>'


class Foo:
    def __str__(self) -> str:
        return "my object"

f = Foo()

str(f)
# >>> 'my object'
```

### `__repr__`

Используется для формального представления объекта. Формальное представление: отображение в интерпретаторе/дебагере, изначально предполагается, что repr должен возвращать строку, которую можно вставить в интерпретатор и получить тот же объект.

```python
class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.ip}', '{self.hostname}')"

d = Device("192.168.1.1", "rt1")
d
# >>> Device('192.168.1.1', 'rt1')

repr(d)
# >>> "Device('192.168.1.1', 'rt1')"
```

### `__dict__`

`__dict__` атрибут, в котором хранятся все атрибуты класса. `__dict__` существует как для самого класса, так и для экземпляра класса.

```python
class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __str__(self) -> str:
        return f"{self.ip}, {self.hostname}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.ip}', '{self.hostname}')"


print(Device.__dict__)
# >>> {'__module__': '__main__', '__init__': <function Device.__init__ at 0x100c88ea0>, '__str__': <function Device.__str__ at 0x100c88f40>, '__repr__': <function Device.__repr__ at 0x100c88fe0>, '__dict__': <attribute '__dict__' of 'Device' objects>, '__weakref__': <attribute '__weakref__' of 'Device' objects>, '__doc__': None}

d = Device("192.168.1.1", "rt1")
print(d.__dict__)
# >>> {'ip': '192.168.1.1', 'hostname': 'rt1'}
```

Как и любой другой атрибут, определенный на уровне класса (классовая переменная), доступен для всех экземпляров класса. Это значит, что модификация переменной через класс или экземпляр класса, будет отражаться во всех остальных экземплярах:

```python
class DataCenter:
    devices = []


dc1 = DataCenter()
dc2 = DataCenter()

print("before adding")
print(dc1.devices)
print(dc2.devices)

# >>> before adding
# >>> []
# >>> []

dc1.devices.append("r1")
dc1.devices.append("r2")

print("after adding")
print(dc1.devices)
print(dc2.devices)

# >>> after adding
# >>> ['r1', 'r2']
# >>> ['r1', 'r2']
```

список devices из примера определен как классовая переменная и является пустым только когда интерпретатор создает класс. Аналогичное поведение у аргументов функций, где значениями по умолчанию выступают мутабельные данные.

Такое поведение можно использовать когда необходимо, что бы экземпляры класса имели одно общее хранилище (shared space) для обмена информацией между собой или иных целей. Кроме этого есть паттерны проектирования, основанные на таком поведении: Singleton и Borg. Singleton рассматривается позже, а сейчас - Borg, так как он основан на комбинации классовой переменной и атрибута `__dict__`:

```python
class RedisPool:
    _state = {}

    def __init__(self):
        self.__dict__ = self._state
        self._session = None

    def connect(self):
        if self._session is None:
            print("first call, need to create connection...")
            self._session = "some redis session"
        else:
            print("session already exists, no need to connect")

    def disconnect(self):
        self._session = None


r1 = RedisPool()
r2 = RedisPool()

print("before connection")
print(r1._session)
print(r2._session)
# >>> before connection
# >>> None
# >>> None

r1.connect()
# >>> first call, need to create connection...

print("after connection")
print(r1._session)
print(r2._session)
# >>> after connection
# >>> some redis session
# >>> some redis session
```

Таким образом можно реализовывать подключения к внешним ресурсам, например к база данных.

### `__slots__`

атрибут `__slots__` позволяет зафиксировать, какие атрибуты могут быть созданы у класса, т.е. с его помощью можно отключить динамическое создание атрибутов. Это экономит память и ускоряет код, необходимое количество памяти сразу резервируется под экземпляр класса.

```python
class Device:
    __slots__ = ["ip", "hostname"]

    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname


d = Device("192.168.1.1", "rt1")

d.location = "msk"
# >>> AttributeError: 'Device' object has no attribute 'location'
```

При этом хранение атрибутов в словаре `__dict__` уже не нужно, и этот атрибут отсутствует (но список переменных остается в атрибуте `__slots__`)

### `__eq__`

метод определяет поведение при проверки равенства объектов `==`

```python
class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __eq__(self, other: Self) -> bool:
        return self.ip == other.ip


d1 = Device("192.168.1.1", "rt1")
d2 = Device("192.168.1.1", "rt2")

d1 == d2
# >>> True
```

Мы самостоятельно можем определить признаки, на основе которых будем считать объекты равными. Аналогично есть методы `__lt__` сравнение на `<` и `__gt__` - `>`, `__le__` - `<=`, `__ge__` - `>=`, `__ne__` - `!=`.

### `__hash__`

При переопределении метода `__eq__` обычно требуется определять и метод `__hash__`, который с ним связан. Метод `__hash__` необходим для работы функции `hash`, и как следствие, определяет возможность объекта быть ключом в словарях (наиболее частая причина определять `__hash__`)

```python
from typing import Self

class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __eq__(self, other: Self) -> bool:
        return self.ip == other.ip

    def __hash__(self) -> int:
        return hash(self.ip)

d1 = Device("192.168.1.1", "rt1")
d2 = Device("192.168.1.2", "rt2")

configs = {
    d1: "config1",
    d2: "config2",
}
```

### `__contains__`

Метод определяет, как ведет себя экземпляр класса, когда он используется в правой части оператора `in` / `not in`:

```python
from typing import Any, Self


class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __eq__(self, other: Self) -> bool:
        return self.ip == other.ip

    def __hash__(self) -> int:
        return hash(self.ip)

    def __str__(self) -> str:
        return f"{self.ip}, {self.hostname}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.ip}', '{self.hostname}')"

    def __contains__(self, value: Any) -> bool:
        return value == self.ip


device = Device("192.168.1.2", "rt2")


def check_ip(ip: str) -> None:
    # тут работает __contains__
    if ip in device:
        print(f"{ip} belongs to `{device}`")
    else:
        print(f"there is no ip {ip} on `{device}`")


for ip in ["192.168.1.2", "192.168.1.200"]:
    check_ip(ip)

# >>> 192.168.1.2 belongs to `192.168.1.2, rt2`
# >>> there is no ip 192.168.1.200 on `192.168.1.2, rt2`
```

### `__enter__` / `__exit__`

Если необходимо сделать так, что бы с объектом можно было работать через контекстный менеджер `with ... as ...`, тогда у него должны быть определены методы `__enter__` (работает при входе к блок кода) и `__exit__` (работает при выходе из блока кода).

```python
from types import TracebackType
from typing import Literal, Self, Type


class RedisPool:
    def __init__(self) -> None:
        self._session: str | None = None

    def connect(self) -> None:
        if self._session is not None:
            print("сессия уже установлена")
            return
        print("сессия отсутствует, нужно создать")
        self._session = "some redis session"
        raise RuntimeError("ошибка во время открытия сессии")

    def disconnect(self):
        print("закрываем сессию")
        self._session = None

    def get_data(self) -> int:
        if self._session is None:
            raise RuntimeError("нет активной сессии")
        return 42

    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        print(f"{exc_type=}")
        print(f"{exc_val=}")
        print(f"{exc_tb=}")
        self.disconnect()
        return False

print("-" * 10, "test 1")
try:
    with RedisPool() as r:
        data = r.get_data()
except Exception as exc:
    print(f"error here: name: '{exc.__class__.__name__}', text: '{exc}'")
else:
    print("no errors")
    print(f"{data=}")

print("-" * 10, "test 2")
try:
    with RedisPool() as r:
        raise ValueError("test")
except Exception as exc:
    print(f"error here: name: '{exc.__class__.__name__}', text: '{exc}'")
else:
    print("no errors")
```

Если в блоке кода произошло исключение, тогда его параметры (тип, само исключение и traceback) передаются в качестве позиционных аргументов в `__exit__` и у разработчика есть возможность работать с этими исключениями. По умолчанию они будут проброшены наверх по стеку после завершения работы функции `__exit__`. Но если вернуть из функции True, тогда исключение будет заглушено (т.е. не будет проброса наверх).

### `__call__`

Метод `__call__` позволяет экземпляру класса вести себя как функция: объект становится Callable и его можно вызывать используя `()`.

```python
class Multiplier:
    def __init__(self, factor: int) -> None:
        self.factor = factor

    def __call__(self, x: int) -> int:
        return x * self.factor

if __name__ == "__main__":
    funcs: list[Callable[[int], int]] = [
        Multiplier(2),
        Multiplier(3),
        lambda x: x * 4,
    ]
    for func in funcs:
        print(func(10))
```
