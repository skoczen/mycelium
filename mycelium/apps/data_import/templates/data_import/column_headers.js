{% spaceless %}
COLUMN_HEADERS = {
	"select_options": {
		{% for k,row_type in import_row_types.items %}	
		"{{k}}": 
			[
				{% for k,f in row_type.importable_fields.items %}
				{
					'name':  "{{f.name}}",
					'value': "{{f.field}}"
				}{% if not forloop.last %},{% endif %}
				{% endfor %}
			]{% if not forloop.last %},{% endif %}
		{% endfor %}
	},
	"rendered_select_options": {
		{% for k,row_type in import_row_types.items %}	
		"{{k}}": '<option value="">Choose a field...</option><option value="{{ignore_string}}">Ignore this Column</option>{% for k,f in row_type.importable_fields.items %}<option value="{{f.field}}">{{f.name}}</option></option>{% endfor %}'{% if not forloop.last %},{% endif %}
		{% endfor %}
	},
	"identity_sets": {
		{% for k,row_type in import_row_types.items %}	
		"{{k}}": 
			[
				{% for j,set in row_type.identity_sets.items %}
				{
					'{{j}}': [
								{% for field in set %}
									"{{field.field}}"{% if not forloop.last %},{% endif %}
								{% endfor %}	
							 ]
				}{% if not forloop.last %},{% endif %}
				{% endfor %}
			]{% if not forloop.last %},{% endif %}
		{% endfor %}
		
	}

};
{% endspaceless %}