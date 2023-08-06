# corgy package

Corgy package for elegant command line parsing.


### _class_ corgy.Corgy(\*\*args)
Base class for collections of variables.

**NOTE**: This class is only available on Python 3.9 or higher.

To create a command line interface, subclass `Corgy`, and declare your arguments
using type annotations:

```python
class A(Corgy):
    x: int
    y: float
```

At runtime, class `A` will have `x`, and `y` as properties, so that the class can be
used similar to Python dataclasses:

```python
a = A()
a.x = 1
a.y  # AttributeError (y is not set)
a.y = a.x + 1.1
```

Note that the class’s `__init__` method only accepts keyword arguments, and ignores
arguments without a corresponding attribute. The following are all valid:

```python
A(x=1, y=2.1)
A(x=1, z=3)  # y is not set, and z is ignored
A(**{"x": 1, "y": 2.1, "z": 3})
```

For command line parsing, the `add_args_to_parser` class method can be used to add
arguments to an `ArgumentParser` object. Refer to the method’s documentation for
more details. `A.add_args_to_parser(parser)` is roughly equivalent to:

```python
parser.add_argument("--x", type=int, required=True)
parser.add_argument("--y", type=float, required=True)
```

`Corgy` classes have their `__slots__` attribute set to the annotated arguments.
So, if you want to use additional instance variables not tracked by `Corgy`, define
them (and only them) in the `__slots__` attribute:

```python
class A(Corgy):
    __slots__ = ("x",)
    y: float

a = A()
a.y = 1  # `Corgy` variable
a.x = 2  # custom variable
```

To allow arbitrary instance variables, add `__dict__` to `__slots__`. Names added
through custom `__slots__` are not processed by `Corgy`, and will not be added to
`ArgumentParser` objects by the class methods.

`Corgy` recognizes a number of special annotations, which are used to control how
the argument is parsed.

**Annotated**:
`typing.Annotated` can be used to add a help message:

```python
x: Annotated[int, "help for x"]
```

Annotations can also be used to modify the flags used to parse the argument. By
default, the argument name is used, prefixed with `--`, and `_` replaced by `-`.
This syntax can also be used to create a positional argument, by specifying a flag
without any leading `-`:

```python
x: Annotated[int, "help for x"]  # flag is `--x`
x: Annotated[int, "help for x", ["-x", "--ex"]]  # flags are `-x/--ex`
x: Annotated[int, "help for x", ["x"]]  # positional argument
```

`Annotated` can accept multiple arguments, but only the first three are used by
`Corgy`. The first argument is the type, the second is the help message, and the
third is a list of flags. `Annotated` should always be the outermost annotation;
other special annotations should be part of the type.

**Optional**:
`typing.Optional` can be used to mark an argument as optional:

```python
x: Optional[int]
```

Another way to mark an argument as optional is to provide a default value:

```python
x: int = 0
```

Default values can be used in conjunction with `Optional`:

```python
x: Optional[int] = 0
```

Note that the last two examples are not equivalent, since the type of `x` is
`Optional[int]` in the last example, so it is allowed to be `None`.

When parsing from the command line, arguments which are not marked as optional
(because they are not marked with `Optional`, and don’t have a default value) will
be required.

**NOTE**: Default values are not type checked, and can be arbitrary objects.

**Sequence**
`collections.abc.Sequence` can be used to specify that an argument accepts multiple
space-separated values. `typing.Sequence` can also be used, but is not recommended
as it is deprecated since Python 3.9.

There are a few different ways to use `Sequence`, each resulting in different
conditions for the parser. The simplest case is a plain sequence:

```python
x: Sequence[int]
```

This represents a (possibly empty) sequence, and corresponds to the following call
to `ArgumentParser.add_argument`:

```python
parser.add_argument("--x", type=int, nargs="*", required=True)
```

Note that since the argument is required, parsing an empty list will still require
`--x` in the command line. After parsing, `x` will be a `list`. To denote an
optional sequence, use `Optional[Sequence[...]]`.

To specify that a sequence must be non-empty, use:

```python
x: Sequence[int, ...]
```

This will result in `nargs` being set to `+` in the call to
`ArgumentParser.add_argument`. Using this syntax **requires**
`collections.abc.Sequence`, since `typing.Sequence` does not accept `...` as an
argument.

Finally, you can specify a fixed length sequence:

```python
x: Sequence[int, int, int]
```

This amounts to `nargs=3`. All types in the sequence must be the same. So,
`Sequence[int, str, int]` will result in a `TypeError`.

**Literal**
`typing.Literal` can be used to specify that an argument takes one of a fixed set of
values:

```python
x: Literal[0, 1, 2]
```

The provided values are passed to the `choices` argument of
`ArgumentParser.add_argument`. All values must be of the same type, which will be
inferred from the type of the first value. If the first value has a `__bases__`
attribute, the type will be inferred as the first base type, and all other choices
must be subclasses of that type:

```python
class A: ...
class A1(A): ...
class A2(A): ...

x: Literal[A1, A2]  # inferred type is A
```

`Literal` itself can be used as a type, for instance inside a `Sequence`:

```python
x: Sequence[Literal[0, 1, 2], Literal[0, 1, 2]]
```

This is a sequence of length 2, where each element is either 0, 1, or 2.

Choices can also be specified by adding a `__choices__` attribute to the argument
type, containing a sequence of choices for the type Note that this will not be type
checked:

```python
class A:
    __choices__ = ("a1", "a2")

x: A
```

**Bool**
`bool` types (when not in a sequence) are converted to
`argparse.BooleanOptionalAction`:

```python
class A(Corgy):
    arg: bool

parser = ArgumentParser()
A.add_to_parser(parser)
parser.print_help()
```

Output:

```text
usage: -c [-h] --arg | --no-arg

optional arguments:
-h, --help       show this help message and exit
--arg, --no-arg
```

Finally, `Corgy` classes can themselves be used as a type, to represent a group of
arguments:

```python
class A(Corgy):
    x: int
    y: float

class B(Corgy):
    x: int
    grp: Annotated[A, "a group"]
```

Group arguments are added to the command line parser with the group argument name
prefixed. In the above example, parsing using `B` would result in the arguments
`--x`, `--grp:x`, and `--grp:y`. `grp:x` and `grp:y` will be converted to an
instance of `A`, and set as the `grp` property of `B`. Note that groups will ignore
any custom flags when computing the prefix; elements within the group will use
custom flags, but because they are prefixed with `--`, they will not be positional.

If initializing a `Corgy` class with `__init__`, arguments for groups can be passed
with their names prefixed with the group name and a colon:

```python
class C(Corgy):
    x: int

class D(Corgy):
    x: int
    c: C

d = D(**{"x": 1, "c:x": 2})
d.x  # 1
d.c  # C(x=2)
```


#### _classmethod_ add_args_to_parser(parser: argparse.ArgumentParser, name_prefix: str = '', make_group: bool = False, group_help: Optional[str] = None)
Add arguments for this class to the given parser.


* **Parameters**


    * **parser** – `argparse.ArgumentParser` instance.


    * **name_prefix** – Prefix for argument names (default: empty string). Arguments
    will be named `--<name-prefix>:<var-name>`. If custom flags are present,
    `--<name-prefix>:<flag>` will be used instead (one for each flag).


    * **make_group** – If `True`, the arguments will be added to a group within the
    parser, and `name_prefix` will be used as the group name.


    * **group_help** – Help text for the group. Ignored if `make_group` is `False`.



#### _classmethod_ parse_from_cmdline(parser: Optional[argparse.ArgumentParser] = None, \*\*parser_args)
Parse an object of the class from command line arguments.


* **Parameters**


    * **parser** – An instance of `argparse.ArgumentParser` or `None`. If `None`, a new
    instance is created.


    * **parser_args** – Arguments to be passed to `argparse.ArgumentParser()`. Ignored
    if `parser` is not None.



### corgy.corgyparser(var_name: str)
Decorate a function as a custom parser for a variable.

**NOTE**: This decorator is only available on Python 3.9 or higher.

To use a custom function for parsing an argument with `Corgy`, use this decorator.
Parsing functions must be static, and should only accept a single string argument.
Decorating the function with `@staticmethod` is optional, but prevents type errors.
`@corgyparser` must be the final decorator in the decorator chain.


* **Parameters**

    **var_name** – The argument associated with the decorated parser.


Example:

```python
class A(Corgy):
    time: tuple[int, int, int]
    @corgyparser("time")
    @staticmethod
    def parse_time(s):
        return tuple(map(int, s.split(":")))
```

The `@corgyparser` decorator can be chained to use the same parser for multiple
arguments:

```python
class A(Corgy):
    x: int
    y: int
    @corgyparser("x")
    @corgyparser("y")
    @staticmethod
    def parse_x_y(s):
        return int(s)
```


### _class_ corgy.CorgyHelpFormatter(prog: str)
Formatter class for `argparse` with a cleaner layout, and support for colors.

`Corgy.parse_from_cmdline` uses this formatter by default, unless a different
`formatter_class` argument is provided. `CorgyHelpFormatter` can also be used
independently of `Corgy`. Simply pass it as the `formatter_class` argument to
`argparse.ArgumentParser()`:

```python
from argparse import ArgumentParser
from corgy import CorgyHelpFormatter
parser = ArgumentParser(formatter_class=CorgyHelpFormatter)
```

To configure `CorgyHelpFormatter`, you can set a number of attributes on the class.
Note that you do not need to create an instance of the class; that is done by the
parser itself. The following public attributes are available:


* `enable_colors`: If `None` (the default), colors are enabled if the `crayons`
package is available, and the output is a tty. To explicitly enable or disable
colors, set to `True` or `False`.


* `color_<choices/keywords/metavars/defaults/options>`: These attributes control
the colors used for various parts of the output (see below for reference).
Available colors are `red`, `green`, `yellow`, `blue`, `black`, `magenta`, `cyan`,
and `white`. Specifying the name in all caps will make the color bold. You can
also use the special value `BOLD` to make the output bold without changing the
color. The default value are `blue` for choices, `green` for keywords, `RED` for
metavars, `YELLOW` for defaults, and `BOLD` for options. Format:

```text
    -a/--arg str       help for arg ({'a'/'b'/'c'} default: 'a')
      |      |                          |            |      |
    options  metavars                 choices      keywords defaults
```


* `output_width`: The number of columns used for the output. If `None` (the
default), the current terminal width is used.


* `max_help_position`: How far to the right (from the start), the help string can
start from. If `None`, there is no limit. The default is `40`.


* `marker_extras_<begin/end>`: The strings used to enclose the extra help text
(choices, default values etc.). The defaults are `(` and `)`.


* `marker_choices_<begin/end>`: The strings used to enclose the list of choices for
an argument. The defaults are `{` and `}`.


* `marker_choices_sep`: The string used to separate individual choices in the choice
list. The default is `/`.

Formatting of individual arguments can be customized with magic attributes defined
on the argument type. The following attributes are recognized:


* `__metavar__`: This can be set to a string on the argument type to override the

    default metavar. Usage:

    ```python
    >>> class T:
            __metavar__ = "METAVAR"
    >>> p = ArgumentParser(formatter_class=CorgyHelpFormatter, add_help=False)
    >>> p.add_argument("--arg", type=T)
    >>> p.print_help()
    options:
      --arg METAVAR  (optional)
    ```


* `__corgy_fmt_choice__`: Formatting of argument choices/defaults can be customized

    by defining a function of this name on the argument type. The function should
    take a single argument, the choice, and return a string. Usage:

    ```python
    >>> class T:
        @staticmethod
        def __corgy_fmt_choice__(choice):
            return f"CHOICE-{choice}"
    >>> p = ArgumentParser(formatter_class=CorgyHelpFormatter, add_help=False)
    >>> p.add_argument("--arg", type=T, choices=["a", "b", "c"], default="a")
    >>> p.print_help()
    options:
      --arg T  ({CHOICE-a/CHOICE-b/CHOICE-c} default: CHOICE-a)
    ```


#### _property_ using_colors(_: boo_ )
Whether colors are enabled.

## Submodules

## corgy.types module

Type factories for use with `corgy` (or standalone with `argparse`).


### _class_ corgy.types.OutputFileType(mode: str = 'w', \*\*kwargs)
`argparse.FileType` subclass restricted to write mode.

Non-existing files are created (including parent directories).


* **Parameters**


    * **mode** – any write mode, e.g., `w` (default), `wb`, `a`, `ab`, etc.


    * **\*\*kwargs** – passed to `argparse.FileType`.



### _class_ corgy.types.InputFileType(mode: str = 'r', \*\*kwargs)
`argparse.FileType` subclass restricted to read mode.

This class exists primarily to provide a counterpart to `OutputFileType`.


* **Parameters**


    * **mode** – any read mode, e.g., `r` (default), `rb`, etc.


    * **\*\*kwargs** – passed to `argparse.FileType`.



### _class_ corgy.types.OutputDirectoryType()
Factory for creating a type representing a directory to be written to.

When an instance of this class is called with a string, the string is interpreted as
a path to a directory. If the directory does not exist, it is created. The directory
is also checked for write permissions; a `Path` instance is returned if everything
succeeds, and `argparse.ArgumentTypeError` is raised otherwise.


### _class_ corgy.types.InputDirectoryType()
Factory for creating a type representing a directory to be read from.

When an instance of this class is called with a string, the string is interpreted as
a path to a directory. A check is performed to ensure that the directory exists, and
that it is readable. If everything succeeds, a `Path` instance is returned,
otherwise `argparse.ArgumentTypeError` is raised.


### _class_ corgy.types.SubClassType(cls: Type[corgy.types._T], allow_base: bool = False, use_full_names: bool = False)
Factory for creating a type representing a sub-class of a given class.


* **Parameters**


    * **cls** – The base class for the type. When used as the `type` argument to an
    `argparse.ArgumentParser.add_argument` call, only sub-classes of this class
    are accepted as valid command-line arguments.


    * **allow_base** – Whether the base class itself is allowed as a valid value for this
    type (default: `False`).


    * **use_full_names** – Whether to use the full name of the classes
    (`__module__ + "." + class.__qualname__`) or just `class.__name__`
    (default: `False`). This is useful when the name itself is not enough to
    uniquely identify a sub-class.


Types returned by this class can be used with `corgy`, and will have the
sub-classes added as valid choices.


#### choices()
Return an iterator over valid choices for this type.


### _class_ corgy.types.KeyValueType(\*, separator: str = "'='")

### _class_ corgy.types.KeyValueType(key_type: Callable[[str], corgy.types._KT], val_type: Callable[[str], corgy.types._VT], \*, separator: str = "'='")
Factory for creating a (key, value) pair type.

When an instance of this class is called with a string of the form `key=value`,
the string is split on the first `=` character, and the resulting pair is returned,
after being cast to provided types.


* **Parameters**


    * **key_type** – Callable that convert a string to the key type (default: `str`).


    * **val_type** – Callable that convert a string to the value type (default: `str`)


    * **separator** (*keyword only*) – The separator to use when splitting the input string
    (default: `=`).
