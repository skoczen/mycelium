RULES_LOGIC = {
"left_sides": {
{% for l in left_sides %}
	"{{l.pk}}": {
		"display_name":"{{l.display_name}}",
{# 		"operator_partial":"{% for o in l.operators %}{% include "rules/_operators_partial.html" %}{% endfor %}", #}
{# 		"right_side_value_partial":"{% with l.first_right_side_type as rst %}{% include "rules/_right_side_values.html" %}{% endwith %}", #}
		"operator_ids": [{% for o in l.operators %}{{o.pk}}{% if not forloop.last %}, {% endif %}{% endfor %}],
		"right_side_type":"{{l.first_right_side_type.pk}}",
		"right_side_partial":"{% with l.first_right_side_type as rst %}{% include "rules/_right_side_values.html" %}{% endwith %}",
		"is_date":{% if l.is_date %}true{% else %}false{% endif %}
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
}
}