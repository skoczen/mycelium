var manageTags = {};
manageTags.state = {};
manageTags.objects = {};
manageTags.actions = {};
manageTags.handlers = {};
manageTags.encyclopedia = {};
manageTags.ui = {};

manageTags.init = function() {
	manageTags.ui.init();
	manageTags.handlers.init();
}

manageTags.encyclopedia.urls = {};

manageTags.objects.tagSet = function(name, order, db_pk ) {
	o = {};
	o.pk = manageTags.state.tagset_counter;
	manageTags.state.tagset_counter ++;
	o.name = name;
	o.order = order;
	o.is_deleted = false;
	o.tags = [];
	db_pk = (db_pk === undefined) ? false : db_pk;
	o.db_pk = db_pk;


	o.ui_element = function() {
		return $("tagset[pk=" + this.pk + "]");
	}
	o.ui_container = function() {
		return $("tagsets");
	}
	o.delete = function() {
		this.is_deleted = true;
	}
	o.sorted_tags = function() {
		var a = [];
		for (var j in this.tags) {
			a.push(this.tags[j])
		}
		a.sort(manageTags.state.tag_and_tagset_sorter)
		return a
	}
	o.set_order = function(order) {
		this.order = order;
	}
	o.delete_from_page_and_state = function() {
		for (var j in manageTags.state.tag_sets) {
			if (manageTags.state.tag_sets[j].pk == this.pk) {
				this.ui_element().remove();
				manageTags.state.tag_sets.splice(j,1);
			}
		}
	}
	o.remove_tag = function(tag) {
		for (var j in this.tags) {
			if (tag.pk == this.tags[j].pk) {
				this.tags.splice(j,1);
				break;
			}
		}
	}

	return o;
};

manageTags.objects.tag = function(tagset, name, order, num_members, db_pk ) {
	o = {};
	o.pk = manageTags.state.tag_counter;
	manageTags.state.tag_counter ++;
	o.tagset = tagset;
	o.name = name;
	o.order = order;
	o.num_members = num_members;
	o.is_deleted = false;
	db_pk = (db_pk === undefined) ? false : db_pk;
	o.db_pk = db_pk;

	o.ui_element = function() {
		return $("li.tag[pk=" + this.pk + "]", this.ui_container());
	}
	o.ui_container = function() {
		return $("ul.tags", this.tagset.ui_element());
	}
	o.delete = function() {
		this.is_deleted = true;
	}
	o.set_order = function(order) {
		this.order = order;
	}
	o.delete_from_page_and_state = function() {
		for (var j in this.tagset.tags) {
			if (manageTags.state.tag_sets[j].pk == this.pk) {
				this.ui_element().remove();
				this.tagset.tags.splice(j,1);
			}
		}
	}
	o.set_tagset = function(tagset) {
		o.tagset = tagset;
	}

	return o;
};


// State
manageTags.state.tag_sets = [];
manageTags.state.tag_counter = 0;
manageTags.state.tagset_counter = 0;
manageTags.state.options = {};
manageTags.state.options.save_timeout_length = 5000; //ms
manageTags.state.save_in_progress = false;
manageTags.state.save_queued = false;
manageTags.state.get_tagset_from_click = function(target) {
	return manageTags.state.get_tagset_from_page_pk(parseInt(target.parents("tagset").attr("pk"),10));
}
manageTags.state.get_tag_from_click = function(target) {
	var pk = parseInt(target.parents(".tag").attr("pk"),10);
	return manageTags.state.get_tag_from_page_pk(pk);
}

manageTags.state.get_tagset_from_element = function(target){
	return manageTags.state.get_tagset_from_page_pk(parseInt(target.attr("pk"),10));
}
manageTags.state.get_tag_from_element = function(target){
	var pk = parseInt(target.attr("pk"),10);
	return manageTags.state.get_tag_from_page_pk(pk);
}

manageTags.state.get_tagset_from_page_pk = function(pk) {
	for (var j in manageTags.state.tag_sets) {
	var tagset = manageTags.state.tag_sets[j];
		if (tagset.pk == pk) {
			return tagset;
		}
	}
}
manageTags.state.get_tag_from_page_pk = function(pk) {
	for (var j in manageTags.state.tag_sets) {
		var tagset = manageTags.state.tag_sets[j];
		for (var i in tagset.tags) {
			var tag = tagset.tags[i]
			if (tag.pk == pk) {
				return tag;
			}
		}
	}
}

manageTags.state.tag_and_tagset_sorter = function(a, b) {
	return a.order - b.order;
}
manageTags.state.sorted_tagsets = function() {
	var a = [];
	for (var j in manageTags.state.tag_sets) {
		a.push(manageTags.state.tag_sets[j])
	}
	a.sort(manageTags.state.tag_and_tagset_sorter)
	return a
}
manageTags.state.full_data_dump = function() {
	var data = {};
	data.tag_sets = []
	for (var i in manageTags.state.tag_sets) {
		var tagset = manageTags.state.tag_sets[i];
		var ts = {};
		ts.name = tagset.name;
		ts.order = tagset.order;
		ts.is_deleted = tagset.is_deleted;
		ts.tags = [];
		ts.page_pk = tagset.pk;
		ts.db_pk = tagset.db_pk;
		for (var j in tagset.tags) {
			var tag = tagset.tags[j];
			var t = {};
			t.name = tag.name;
			t.order = tag.order;
			t.is_deleted = tag.is_deleted;
			t.db_pk = tag.db_pk;
			t.page_pk = tag.pk;
			ts.tags.push(t);
		}

		data.tag_sets.push(ts);
	}
	return {'data':JSON.stringify(data)}
}


// Handlers
manageTags.handlers.add_tag_clicked = function() {
	var tagset = manageTags.state.get_tagset_from_click($(this));
	manageTags.actions.add_tag(tagset);
	return false;
};
manageTags.handlers.tag_name_changed = function() {
	var tag = manageTags.state.get_tag_from_click($(this));
	manageTags.actions.update_tag_obj(tag);
	manageTags.actions.queue_save();
};
manageTags.handlers.delete_tag_clicked = function() {
	var tag = manageTags.state.get_tag_from_click($(this));
	tag.ui_element().addClass("pre_delete");
	if (confirm("You sure?  \n\nThis will de-tag anyone with this tag, and delete the tag. It can't be undone.\n\nPress OK to delete this tag.\nPress Cancel to leave it in place.")) {
		manageTags.actions.delete_tag(tag);
	}
	tag.ui_element().removeClass("pre_delete");
	return false;
};
manageTags.handlers.tag_order_changed = function() {
	manageTags.actions.sort_tags_and_tagsets();
	manageTags.actions.queue_save();
};

manageTags.handlers.add_tagset_clicked = function() {
	var ts = manageTags.state.get_tagset_from_click($(this));
	manageTags.actions.add_tagset(ts);
	return false;
};
manageTags.handlers.tagset_name_changed = function() {
	var tagset = manageTags.state.get_tagset_from_click($(this));
	manageTags.actions.update_tagset_obj(tagset);
	manageTags.actions.queue_save();

};
manageTags.handlers.delete_tagset_clicked = function() {
	var tagset = manageTags.state.get_tagset_from_click($(this));
	tagset.ui_element().addClass("pre_delete");
	if (confirm("Hold on there.\n\nThis will delete the entire tag category, including all tags in it!\n\nThis action can not be undone.\n\nPress OK to delete this tag category.\nPress Cancel to leave it intact.")) {
		manageTags.actions.delete_tagset(tagset);
	}
	tagset.ui_element().removeClass("pre_delete");
	return false;	
};
manageTags.handlers.tagset_order_changed = function() {
	manageTags.actions.sort_tags_and_tagsets();
	manageTags.actions.queue_save();
};

manageTags.handlers.init = function(){
	manageTags.handlers.setup_sortable_handlers();

	$(".add_a_tag_btn").live("click",manageTags.handlers.add_tag_clicked);
	$(".tag input").live("change",manageTags.handlers.tag_name_changed);
	$(".delete_tag_btn").live("click",manageTags.handlers.delete_tag_clicked);

	$(".add_a_category_btn").live("click",manageTags.handlers.add_tagset_clicked);
	$("tagset .detail_header .generic_editable_field input").live("change",manageTags.handlers.tagset_name_changed);
	$(".delete_tagset_btn").live("click",manageTags.handlers.delete_tagset_clicked);

	$(".save_and_status_btn").live("click", manageTags.actions.queue_save);
}
manageTags.handlers.setup_sortable_handlers = function() {
		$( "tagsets" ).sortable({
					update: manageTags.handlers.tagset_order_changed,
					// handle: '.tagset_drag_icon',
				});
	$( "ul.tags" ).sortable({
		connectWith: "ul.tags",
		update: manageTags.handlers.tag_order_changed,
		// handle: '.tag_drag_icon',
	});
		// .disableSelection();
}

// Actions
manageTags.actions.add_tag = function(tagset) {
	tagset.tags.push(manageTags.objects.tag(tagset, "Unnamed Tag", 10000, 0));
	manageTags.ui.render_tagset(tagset);
	manageTags.actions.sort_tags_and_tagsets();
	manageTags.actions.queue_save();
	manageTags.handlers.setup_sortable_handlers();
};
manageTags.actions.update_tag_obj = function(tag) {
	tag.name = $(".tag_name input[name$=-name]",tag.ui_element()).val();
};
manageTags.actions.delete_tag = function(tag) {
	tag.delete();
	manageTags.ui.render_tag(tag);
	manageTags.actions.queue_save();
};
manageTags.actions.add_tagset = function() {
	var tagset = manageTags.objects.tagSet("Unnamed Category", 10000)
	manageTags.state.tag_sets.push(tagset);
	manageTags.ui.render_tagset(tagset);
	manageTags.actions.sort_tags_and_tagsets();
	manageTags.actions.queue_save();
	manageTags.handlers.setup_sortable_handlers();

};
manageTags.actions.update_tagset_obj = function(tagset) {
	tagset.name = $(".detail_header input[name$=-name]",tagset.ui_element()).val();
};
manageTags.actions.delete_tagset = function(tagset) {
	tagset.delete();
	manageTags.ui.render_tagset(tagset);
	manageTags.actions.queue_save();
};
manageTags.actions.queue_save = function() {
	manageTags.state.save_queued = true;
	if (!manageTags.state.save_in_progress) {
		manageTags.ui.show_saving();
		clearTimeout(manageTags.state.save_timeout)
		manageTags.state.save_timeout = setTimeout(manageTags.actions.save_state, manageTags.state.options.save_timeout_length);
	}
};
manageTags.actions.save_state = function() {
	manageTags.state.save_queued = false;
	manageTags.state.save_in_progress = true;
	
	$.ajax({
		url: manageTags.encyclopedia.urls.save_tags_and_tagsets,
		type: "POST",
		dataType: "json",
		data: manageTags.state.full_data_dump(),
		success: function(json) {
			// delete the things that were deleted.
			for (var j in json.created_tagsets) {
				var ts = json.created_tagsets[j];
				var tagset = manageTags.state.get_tagset_from_page_pk(ts.page_pk)
				tagset.db_pk = ts.db_pk;
			}
    		for (var j in json.created_tags) {
	    		var t = json.created_tags[j];
	    		var tag = manageTags.state.get_tag_from_page_pk(t.page_pk)
	    		tag.db_pk = t.db_pk;
	    	}
    		for (var j in json.deleted_tagsets) {
	    		var ts = json.deleted_tagsets[j];
	    		var tagset = manageTags.state.get_tagset_from_page_pk(ts.page_pk)
	    		// make sure it's still gone
	    		if (tagset.is_deleted) {
	    			tagset.delete_from_page_and_state()	
	    		}
	    	}
    		for (var j in json.deleted_tags) {
	    		var t = json.deleted_tags[j];
	    		var tag = manageTags.state.get_tag_from_page_pk(t.page_pk)
	    		if (tag.is_deleted) {
	    			tag.delete_from_page_and_state()	
	    		}
	    	}

			if (manageTags.state.save_queued) {
				manageTags.actions.save_state();
			} else {
				manageTags.state.save_in_progress = false;
				manageTags.ui.show_saved();
			}
			
		}
	});
};
manageTags.actions.sort_tags_and_tagsets = function (){
	var ts_counter = 0;
	var tag_counter = 0;
	$("tagset").each(function(){
		var ts_ele = $(this);
		manageTags.state.get_tagset_from_element(ts_ele).set_order(ts_counter);
		ts_counter++;
	});
	$("li.tag").each(function() {
		var tag_ele = $(this);
		var tag = manageTags.state.get_tag_from_element(tag_ele);
		var tagset = manageTags.state.get_tagset_from_click(tag_ele);
		tag.set_order(tag_counter);
		if (tag.tagset != tagset) {
			tag.tagset.remove_tag(tag);
			tag.set_tagset(tagset);	
			tagset.tags.push(tag);
		}
		
		tag_counter ++;
	});

	// Update any tagsets.
	for (var j in manageTags.state.tag_sets) {
		var tagset = manageTags.state.tag_sets[j];
		for (var i in tagset.tags) {
			
		}
	}
}


manageTags.ui.init = function() {
	manageTags.ui.render_full_ui();
}
manageTags.ui.render_tag = function(tag) {
	var str = "";
	if (!tag.is_deleted) {
		str += '<table class="tag_list striped">';
		str += '	<tr class="striped_row tag_row">';
		str += '		<td class="tag_name"><div class="tag_drag_icon"></div><span class="generic_editable_field"><span class="edit_field"><input type="text" name="TAG-'+tag.pk+'-name" value="'+tag.name+'" maxlength="250" /></span></span></td>';
		str += '		<td class="num_people"><span class="count">'+tag.num_members+'</span> '+ ((tag.num_members==1)?'person':'people') +'</td>';
		str += '		<td class="tag_actions"><a href="#" class="delete_tag_btn mycelium_btn mycelium_delete_btn mycelium_active_grey mycelium_small_btn">Delete Tag</a></td>';
		str += '	</tr>';
		str += '</table>';

		if (!tag.ui_element().length) {
			tag.ui_container().append('<li class="tag" pk="'+tag.pk+'"></li>')
		}
		tag.ui_element().html(str);
	} else {
		if (tag.ui_element()) {
			tag.ui_element().remove();
		}
	}
	
};
manageTags.ui.render_tagset = function(tagset) {
	if (!tagset.is_deleted) {
		var str = "";
		
		str += '	<div class="detail_header">';
		str += '		<div class="header_actions">';
		str += '			<a href="#" class="delete_tagset_btn mycelium_btn mycelium_delete_btn mycelium_active_grey mycelium_small_btn">Delete Tag Category</a>';
		str += '		</div>';
		str += '		<div class="tagset_drag_icon"></div>';
		str += '		<span class="generic_editable_field"><span class="edit_field"><input type="text" name="TAGSET-'+tagset.pk+'-name" value="'+tagset.name+'" maxlength="250" /></span></span>';
		str += '	</div>';
		str += '	<ul class="tags">';
		str += '	</ul>';
		str += '	<form_actions>';
		str += '	<a href="#" class="mycelium_btn mycelium_small_btn add_a_tag_btn" >Add a Tag</a>';
		str += '	</form_actions>';
		
		if (!tagset.ui_element().length) {
			tagset.ui_container().append('<tagset pk="'+tagset.pk+'"></tagset>');	
		}
		tagset.ui_element().html(str);	
		
		var sorted_tags = tagset.sorted_tags();
		for (var j in sorted_tags) {
			manageTags.ui.render_tag(sorted_tags[j]);
		}		
	} else {
		if (tagset.ui_element()) {
			tagset.ui_element().remove();
		}
	}
};

manageTags.ui.render_full_ui = function() {
	var sorted_tagsets = manageTags.state.sorted_tagsets();

	for (var j in sorted_tagsets) {
		manageTags.ui.render_tagset(sorted_tagsets[j]);
	}
};


manageTags.ui.show_saving = function() {
	$(".save_and_status_btn").html("Saving...");
	$(".last_save_time").html("")
}

manageTags.ui.show_saved = function() {
	$(".save_and_status_btn").html("Saved");
	$(".last_save_time").html("Saved a few seconds ago.")
}
