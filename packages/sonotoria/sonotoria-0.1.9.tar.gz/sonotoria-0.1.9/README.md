# Sonotoria

Sonotoria is a library designed to provide features helping with templating and handling yaml files.

# Loading Yaml

Sonotoria lets you load a yaml with variables using jinja2 syntax:

## Examples

### From a file
Given the file:
```yaml
# test.yml
---

param: value
param2: {{ param }}
```

You can load the data:
```py
>>> from sonotoria import yaml
>>> yaml.load('test.yml')
{'param': 'value', 'param2': 'value'}
```

### From a string
You can also load a string directly:
```py
>>> from sonotoria import yaml
>>> yaml.loads('---\nparam: value\nparam2: {{ param }}')
{'param': 'value', 'param2': 'value'}
```

### Using context
Given the file:
```yaml
# test.yml
---

param2: {{ param }}
```

You can load the data:
```py
>>> from sonotoria import yaml
>>> yaml.load('test.yml', context={'param': 12})
{'param2': 12}
```

### Using filters
Given the file:
```yaml
# test.yml
---

param: value
param2: {{ param | doubled }}
```

You can load the data:
```py
>>> from sonotoria import yaml
>>> yaml.load('test.yml', filters={'doubled': lambda s: s*2})
{'param': 'value', 'param2': 'valuevalue'}
```

### Using tests
Given the file:
```yaml
# test.yml
---

param: value
param2: {{ param is number }}
```

You can load the data:
```py
>>> from sonotoria import yaml
>>> yaml.load('test.yml', tests={'number': lambda s: s.isdigit()})
{'param': 'value', 'param2': False}
```

### Using objects
Given the file:
```yaml
# test.yml
--- !stuff

param: value
param2: {{ param }}
```

You can load the data:
```py
>>> from sonotoria import yaml
>>> class Stuff:
....    pass
>>> my_stuff = yaml.load('test.yml', types={'stuff': Stuff})
>>> my_stuff.param
value
>>> my_stuff.param2
value
```
You can add tests, filters and types:


# Extractor

Sonotoria lets you extract data from a file using a jinja2 template.

## Example

Given this input file:
```
That is a description

:param test: Looks like a test variable, huh
:param lol: This might be a fun variable
:param plop: Plop might just be the next best variable name
:return: Pretty much nothing, sadly
```

And this template file:
```
{{ description }}

{% for param, desc in params.items() %}
:param {{ param }}: {{ desc }}
{% endfor %}{% if return_given %}
:return: {{ return }}{% endif %}{% if rtype_given %}
:rtype: {{ rtype }}{% endif %}
```

You can extract data this way:
```py
>>> import sonotoria
>>> sonotoria.extract('template.file', 'input.file')
{
    'description': 'That is a description',
    'params': {
        'test': 'Looks like a test variable, huh',
        'lol': 'This might be a fun variable',
        'plop': 'Plop might just be the next best variable name'
    },
    'return': 'Pretty much nothing, sadly',
    'rtype': None,
    'return_given': True,
    'rtype_given': False
}
```

# Contributors

 * Emmanuel Pluot (aka. Neomyte)
