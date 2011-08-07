$(function(){
// Set up Mycelium object
	if ($.Mycelium === undefined) {
		$.Mycelium = {};
	}
	if (typeof(SEARCH_URL) == "undefined") {
	    var SEARCH_URL = "";
	}

// Fragments handler
	var fragments = new Object();
	
	fragments.options = {
	    json_dict_name: "fragments"
	};
	fragments.get_and_update_fragments = function(url, override_options) {
	    var default_options = {
          url: url,
          type: "POST",
          dataType: "json",
          success: function(json) {
             $.Mycelium.fragments.process_fragments_from_json(json);
          }
        };
        var options =  $.extend(default_options, override_options);
        $.ajax(options);
	};
	
    fragments.process_fragments_from_json = function(json) {
        if (json[fragments.options.json_dict_name] != undefined) {
            return fragments.process_fragments(json[fragments.options.json_dict_name]);
        } else {
            return fragments.process_fragments(json);
        }
    };
    
	fragments.process_fragments = function(fragment_dict) {
	    $("fragment").each(function(){
	        frag = $(this);
            if (fragment_dict[frag.attr("name")] != undefined) {
               frag.trigger("fragments."+frag.attr("action"), {'new_content':fragment_dict[frag.attr("name")], 'target':frag});
	        }
	    });
	    return true;
	};
	
	fragments.replace_content = function(e, d) {
        $(d.target).html(d.new_content);
	};
	fragments.append_content = function(e, new_content, target) {
	    $(target).append(new_content);
	};
	fragments.clear_content = function(e, new_content, target) {
        $(target).html("");
	};
    // Default fragment actions:
    // replace
    // append
    // clear
	$(document).bind("fragments.replace",fragments.replace_content);
	$(document).bind("fragments.append",fragments.append_content);
	$(document).bind("fragments.clear",fragments.clear_content);

	$.Mycelium.fragments = fragments;



// Highlights
    
    $.Mycelium.highlight_search_terms = function(q, context_ele) {
    	var space_queries = q.split(" ");
    	highlight_regexes = [];
        var has_single_b = false;
    	for (var j in space_queries) {
    		var q = space_queries[j];
    		if (q != "") {
                if (q == "<" || q == ">" || q == "/" || q == "b") {
                    if (q == "b") {
                        has_single_b = true;
                    }
                } else {
        			highlight_regexes.push(new RegExp(q, "gi"));
                }

    			var dash_queries = q.split("-");
    			if (dash_queries.length > 1) {
    				for (var k in dash_queries) {
    					if (dash_queries[k] != "") {
                            if (dash_queries[k] == "<" || dash_queries[k] == ">" || dash_queries[k] == "/" || dash_queries[k] == "b") {
                                if (dash_queries[k] == "b") {
                                    has_single_b = true;
                                }
                            } else {
                                highlight_regexes.push(new RegExp(dash_queries[k], "gi"));
                            }
    					}
    				}
    			}
    		}
    	}
    	$(".highlightable", context_ele).each(function(){
    		var text = $(this).text();
            if (has_single_b) {
                text = text.replace(new RegExp('b', "gi"), '<b>$&</b>');
            }
            for (var j in highlight_regexes) {
                text = text.replace(highlight_regexes[j], '<b>$&</b>');
    		}
            $(this).html(text);
    	});

    };

// Striping
    $.Mycelium.update_stripes = function(context_ele) {
        $(".striped .striped_row:even",context_ele).addClass("even");
        $(".striped .striped_row:odd",context_ele).addClass("odd");
    };
    $.Mycelium.update_stripes();

//  Mycelium Elements
    $("tabbed_box.with_button tab_title").live("click",function(){
        var box = $(this).parents("tabbed_box.with_button");
        if (box.hasClass("open")) {
            box.removeClass("open").addClass("closed");
            box.trigger("mycelium.tabbed_box.closed");
        } else {
            box.addClass("open").removeClass("closed");
            box.trigger("mycelium.tabbed_box.opened");
        }
    });


// Auto-disabling input and html
	$(".auto_disable").live("click",function(){
		var btn = $(this);
		if (!btn.hasClass("disabled")) {
			setTimeout(function(){
				btn.addClass("disabled");
				btn.attr("disabled","disabled");

				if (btn.is("a")) {
					btn.attr("old_html", btn.html());
					btn.html(btn.attr("disabled_text"));
				} else {
					btn.attr("old_val", btn.val());
					btn.val(btn.attr("disabled_text"));
				}
			}, 10);
		} else {
			return false;
		}
	});

	$.Mycelium.enable_disabled_btn = function(btn) {
		if (btn.hasClass("disabled")) {
			btn.removeClass("disabled");
			btn.removeAttr("disabled");

			if (btn.is("a")) {
				btn.html(btn.attr("old_html"));
			} else {
				btn.val(btn.attr("old_val"));
			}
		} 		
	};
});


//Support Placeholders
$(document).ready(function() {
	if (!Modernizr.input.placeholder)
	{
		var placeholderText = $('#search').attr('placeholder');

		$('#search').attr('value',placeholderText);
		$('#search').addClass('placeholder');

		$('#search').focus(function() {
			if( ($('#search').val() == placeholderText) )
			{
				$('#search').attr('value','');
				$('#search').removeClass('placeholder');
			}
		});

		$('#search').blur(function() {
			if ( ($('#search').val() == placeholderText) || (($('#search').val() == '')) )
			{
				$('#search').addClass('placeholder');
				$('#search').attr('value',placeholderText);
			}
		});
	}
});