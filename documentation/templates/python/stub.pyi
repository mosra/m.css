{% set pj = joiner('\n\n') %}
{% if STUB_HEADER %}{{ pj() }}{{ STUB_HEADER|trim }}{% endif %}
{% if page.dependencies %}{{ pj() }}{% for prefix, module in page.dependencies %}
{% if not loop.first %}

{% endif %}
{% if prefix %}from {{ prefix }} import {{ module or '*' }}{% else %}import {{ module }}{% endif %}
{% endfor %}{% endif %}
{% macro render_enums(enums) %}
{% for enum in enums %}
{% if not loop.first %}


{% endif %}
class {{ enum.name }}({% if enum.base_relative %}{{ enum.base_relative }}{% else %}enum.Enum{% endif %}):
{% if not enum.values %}
    ...
{%- else %}
    {% for value in enum.values %}
    {% if not loop.first %}

    {% endif %}
    {{ value.name }} = {{ value.value }}{% endfor %}
{% endif %}
{% endfor %}{% endmacro %}
{% macro render_functions(functions) %}
{% for function in functions %}
{% if not loop.first %}


{% endif %}
{% if function.is_classmethod %}
@classmethod
{% elif function.is_staticmethod %}
@staticmethod
{% endif %}
{% if function.is_overloaded %}
@typing.overload
{% endif %}
{% if function.params|length == 1 and not function.params[0].name %}
def {{ function.name }}({% if function.is_classmethod %}cls, {% elif function.is_method and not function.is_staticmethod %}self, {% endif %}*args):
{% else %}
def {{ function.name }}({% for param in function.params %}{% if loop.index0 and function.params[loop.index0 - 1].kind == 'POSITIONAL_OR_KEYWORD' and param.kind == 'KEYWORD_ONLY' %}, *{% endif %}{% if not loop.first %}, {% endif %}{% if param.kind == 'VAR_POSITIONAL' %}*{% elif param.kind == 'VAR_KEYWORD' %}**{% endif %}{{ param.name }}{% if param.type_quoted %}: {{ param.type_quoted }}{% endif %}{% if param.default_relative %} = {{ param.default_relative }}{% endif %}{% if param.kind == 'POSITIONAL_ONLY' and (loop.last or function.params[loop.index0 + 1].kind != 'POSITIONAL_ONLY') %}, /{% endif %}{% endfor %}){% if function.type_quoted %} -> {{ function.type_quoted }}{% endif %}:
{% endif %}
    ...
{%- endfor %}{% endmacro %}
{% macro render_properties(properties) %}
{% for property in properties %}
{% if not loop.first %}


{% endif %}
@property
def {{ property.name }}(self){% if property.type_quoted %} -> {{ property.type_quoted }}{% endif %}:
    ...
{%- if property.is_settable +%}
@{{ property.name }}.setter
def {{ property.name }}(self, value{% if property.type_quoted %}: {{ property.type_quoted }}{% endif %}):
    ...
{%- endif %}
{%- if property.is_deletable +%}
@{{ property.name }}.deleter
def {{ property.name }}(self):
    ...
{%- endif %}
{%- endfor %}{% endmacro %}
{% macro render_data(data_) %}
{% for data in data_ %}
{% if not loop.first %}


{% endif %}
{{ data.name }}{% if data.type_quoted or data.value_relative %}{% if data.type_quoted %}: {{ data.type_quoted }}{% endif %}{% if data.value_relative %} = {{ data.value_relative }}{% endif %}{% else %}: ...{% endif %}
{% endfor %}{% endmacro %}
{% if page.enums %}{{ pj() }}{{ render_enums(page.enums) }}{% endif %}
{% if page.classes %}{{ pj() -}}
{% for class in page.classes recursive %}
{% if not loop.first %}


{% endif %}
class {{ class.name }}:
{% if not class.has_members %}
    ...
{%- endif %}
{% set mj = joiner('\n\n') %}
{% if class.enums %}{{ mj() }}{{ render_enums(class.enums)|indent(4, first=True) }}{% endif %}
{% if class.classes %}{{ mj() }}{{ loop(class.classes)|indent(4, first=True) }}{% endif %}
{% if class.data %}{{ mj() }}{{ render_data(class.data)|indent(4, first=True) }}{% endif %}
{% if class.staticmethods %}{{ mj() }}{{ render_functions(class.staticmethods)|indent(4, first=True) -}}{% endif %}
{% if class.classmethods %}{{ mj() }}{{ render_functions(class.classmethods)|indent(4, first=True) }}{% endif %}
{% if class.methods %}{{ mj() }}{{ render_functions(class.methods)|indent(4, first=True) }}{% endif %}
{% if class.dunder_methods %}{{ mj() }}{{ render_functions(class.dunder_methods)|indent(4, first=True) }}{% endif %}
{% if class.properties %}{{ mj() }}{{ render_properties(class.properties)|indent(4, first=True) }}{% endif %}
{%- endfor %}{% endif %}
{% if page.data %}{{ pj() }}{{ render_data(page.data) }}{% endif %}
{% if page.functions %}{{ pj() }}{{ render_functions(page.functions) }}{% endif %}
