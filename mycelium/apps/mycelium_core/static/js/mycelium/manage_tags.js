$(function() {
 //    $("form.category_name").genericFieldForm();
	// $("form.category_name").toggle_edit();

    // bind_tags_events();
    // manageTags.init();

});




var manageTags = {};
manageTags.state = {};
manageTags.objects = {};
manageTags.actions = {};
manageTags.handlers = {};
manageTags.ui = {};

manageTags.init = function() {
	manageTags.ui.init();
	manageTags.handlers.init();
}

manageTags.objects.tagSet = function(name, order ) {
	o = {};
	o.pk = manageTags.state.tag_sets.length;
	o.name = name;
	o.order = order;
	o.is_deleted = false;
	o.tags = [];

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

	return o;
};

manageTags.objects.tag = function(tagset, name, order, num_members ) {
	o = {};
	o.pk = tagset.tags.length;
	o.tagset = tagset;
	o.name = name;
	o.order = order;
	o.num_members = num_members;
	o.is_deleted = false;

	o.ui_element = function() {
		return $("li.tag[pk=" + this.pk + "]", this.ui_container());
	}
	o.ui_container = function() {
		return $("ul.tags", this.tagset.ui_element());
	}
	o.delete = function() {
		this.is_deleted = true;
	}

	return o;
};


// State
manageTags.state.tag_sets = [];
manageTags.state.options = {};
manageTags.state.options.save_timeout_length = 3000; //ms
manageTags.state.get_tagset_from_click = function(target) {
	return manageTags.state.tag_sets[parseInt(target.parents("tagset").attr("pk"),10)];
}
manageTags.state.get_tag_from_click = function(target) {
	var tagset = manageTags.state.get_tagset_from_click(target);
	return tagset.tags[parseInt(target.parents(".tag").attr("pk"),10)];
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
	if (confirm("You sure?\n\nPress OK to delete this tag.\nPress Cancel to leave it in place.")) {
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
	var ts = manageTags.state.get_tagset_from_click($(this));
	manageTags.actions.update_tag_obj(tag);
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
	$( "tagsets" ).sortable({
					update: manageTags.handlers.tagset_order_changed,
				});
	$( "ul.tags" ).sortable({
		connectWith: "ul.tags",
		update: manageTags.handlers.tag_order_changed,
	});
	// .disableSelection();

	$(".add_a_tag_btn").live("click",manageTags.handlers.add_tag_clicked);
	$(".tag input[name$=-name").live("change",manageTags.handlers.tag_name_changed);
	$(".delete_tag_btn").live("click",manageTags.handlers.delete_tag_clicked);

	$(".add_a_category_btn").live("click",manageTags.handlers.add_tagset_clicked);
	$("tagset input[name$=-name").live("change",manageTags.handlers.tagset_name_changed);
	$(".delete_tagset_btn").live("click",manageTags.handlers.delete_tagset_clicked);
}


// Actions
manageTags.actions.add_tag = function(tagset) {
	tagset.tags.push(manageTags.objects.tag(tagset, "Unnamed Tag", 10000, 0));
	manageTags.ui.render_tagset(tagset);
	manageTags.actions.sort_tags_and_tagsets();
	manageTags.actions.queue_save();
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

};
manageTags.actions.update_tagset_obj = function(tagset) {
	tagset.name = $(".detail_header input[name$=-name]",tag.ui_element()).val();
};
manageTags.actions.delete_tagset = function(tagset) {
	tagset.delete();
	manageTags.ui.render_tagset(tagset);
	manageTags.actions.queue_save();
};
manageTags.actions.queue_save = function() {
	clearTimeout(manageTags.state.save_timeout)
	manageTags.state.save_timeout = setTimeout(manageTags.actions.save_state, manageTags.state.options.save_timeout_length);
};
manageTags.actions.save_state = function() {
	console.log("saving");
};
manageTags.actions.sort_tags_and_tagsets = function (){
	var ts_counter = 0;
	$("tagset").each(function(){
		var ts_ele = $(this);
		var tagset = manageTags.state.get_tagset_from_click(ts_ele.children(":first"));
		tagset.order = ts_counter;

		var tag_counter = 0;
		$(".tag", ts_ele).each(function() {
			var tag_ele = $(this);
			var tag = manageTags.state.get_tag_from_click(tag_ele.children(":first"));
			tag.order = tag_counter;
			tag_counter ++;
		})
		ts_counter++;
	});
}

manageTags.ui.init = function() {
	manageTags.ui.render_full_ui();
}
manageTags.ui.render_tag = function(tag) {
	var str = "";
	if (!tag.is_deleted) {
		str += '<div><table class="tag_list striped">';
		str += '	<tr class="striped_row tag_row">';
		str += '		<td class="tag_name"><div class="tag_drag_icon"></div><span class="generic_editable_field"><span class="edit_field"><input type="text" name="TAG-'+tag.pk+'-name" value="'+tag.name+'" maxlength="250" /></span></span></td>';
		str += '		<td class="num_people"><span class="count">'+tag.num_members+'</span> '+ ((tag.num_members==1)?'person':'people') +'</td>';
		str += '		<td class="tag_actions"><a href="#" class="delete_tag_btn mycelium_btn mycelium_delete_btn mycelium_active_grey mycelium_small_btn">Delete Tag</a></td>';
		str += '	</tr>';
		str += '</table></div>';

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


// function bind_tags_events() {
// 	$(".delete_tagset_btn").die("click").live("click",delete_category);
// 	$(".delete_tag_btn").die("click").live("click",delete_tag);
// 	$(".add_a_tag_btn").die("click").live("click",add_a_tag);
// 	$(".add_a_category_btn").die("click").live("click",add_a_category);
// }

// function process_link_via_json(t) {
// 	setTimeout(function(){
// 	if ($("#basic_info_form").hasClass("dirty")) {
// 		$("#basic_info_form").ajaxSubmit({
// 			'async':false
// 		});		
// 	}
// 	$.ajax({
// 		url: $(t).attr("href"),
// 		type: "POST",
// 		dataType: "json",
// 		success: function(json) {
// 			process_fragments_and_rebind_tags_form(json);
// 		}
// 	});
// 	},10);
// }

// function delete_category() {
// 	var ts = $(this).parents("tagset");
// 	var tagset_row = $(".detail_header",ts);
// 	var tag_rows = $(".tag_row",ts);
// 	var ts_add = $(".add_a_tag_btn",ts);
// 	tagset_row.addClass("pre_delete");
// 	tag_rows.addClass("pre_delete");
// 	ts_add.addClass("pre_delete")
// 	if (confirm("Hold on there.\n\nThis will delete the entire tag category, including all tags in it!\n\nThis action can not be undone.\n\nPress OK to delete this tag category.\nPress Cancel to leave it intact.")) {
// 		process_link_via_json($(this));
// 	} else {
// 		tagset_row.removeClass("pre_delete");
// 		tag_rows.removeClass("pre_delete");
// 		ts_add.removeClass("pre_delete");
// 	}
// 	return false;
// }
// function delete_tag() {
// 	var tag_row = $(this).parents(".tag_row");
// 	tag_row.addClass("pre_delete");
// 	if (confirm("You sure?\n\nPress OK to delete this tag.\nPress Cancel to leave it in place.")) {
// 		process_link_via_json($(this));
// 	} else {
// 		tag_row.removeClass("pre_delete");
// 	}
// 	return false;
// }
// function add_a_tag() {
// 	process_link_via_json($(this));
// 	return false;
// }
// function add_a_category() {
// 	process_link_via_json($(this));
// 	return false;
// }

// function process_fragments_and_rebind_tags_form(json) {
//     $.Mycelium.fragments.process_fragments_from_json(json);
//     $.Mycelium.update_stripes();
//     bind_tags_events();
// }
