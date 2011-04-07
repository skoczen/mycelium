rules_logic = {
"left_sides": {
{% for l in left_sides %}
	"{{l.pk}}": {
		"display_name":"{{l.display_name}}",
{# 		"operator_partial":"{% for o in l.operators %}{% include "rules/_operators_partial.html" %}{% endfor %}", #}
{# 		"right_side_value_partial":"{% with l.first_right_side_type as rst %}{% include "rules/_right_side_values.html" %}{% endwith %}", #}
		"operator_ids": [{% for o in l.operators %}{{o.pk}}{% if not forloop.last %}, {% endif %}{% endfor %}],
		"right_side_type":"{{l.first_right_side_type.name}}",
		"right_side_type_ids":[{% for rst in l.right_side_types %}{{rst.pk}}{% if not forloop.last %}, {% endif %}{% endfor %}],
		"choices": {% if l.choices %}[{% for c in l.choices %}["{{c|first}}","{{c|last}}"]{% if not forloop.last %}, {% endif %}{% endfor %}]{% else %}null{% endif %},
		"choices_partial": {% if l.choices %}"{% with l.choices as choices %}{% include "rules/_choices.html" %}{% endwith %}"{% else %}null{% endif %}
	}{% if not forloop.last %},{% endif %}
{% endfor %}
},
"operators": {
	{% for o in operators %}
	"{{o.pk}}": {
		"display_name":"{{o.display_name}}",
		"partial":"{% include "rules/_operators_partial.html" %}"
	}{% if not forloop.last %},{% endif %}
	{% endfor %}
},
"right_sides": {
	{% for rst in right_side_types %}
	"{{rst.pk}}": {
		"display_name":"{{rst.name}}",
		"partial":"{% include "rules/_right_side_values.html" %}"
	}{% if not forloop.last %},{% endif %}
	{% endfor %}
}
}