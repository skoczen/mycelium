$(function(){
// Set up Mycelium object
	if ($.Mycelium === undefined) {
		$.Mycelium = new Object();
	}
	if (typeof(SEARCH_URL) == "undefined") {
	    var SEARCH_URL = ""
	}

// Fragments handler
	var fragments = new Object();
	
	fragments.options = {
	    json_dict_name: "fragments"
	};
	
    // Default fragment actions:
    // replace
    // append
    // clear
    fragments.process_fragments_from_json = function(json) {
        if (json.hasOwnProperty(fragments.options.json_dict_name)) {
            return fragments.process_fragments(json[fragments.options.json_dict_name]);
        } else {
            return fragments.process_fragments(json);
        }
    }
    
	fragments.process_fragments = function(fragment_dict) {
	    $("fragment").each(function(){
	        frag = $(this);
	        if (fragment_dict.hasOwnProperty(frag.attr("name"))) {
	           frag.trigger("fragments."+frag.attr("action"), fragment_dict[frag.attr("name")]);
	        }
	    });
	};
	
	fragments.replace_content = function(e, new_content) {
        $(e.target).html(new_content);
	};
	fragments.append_content = function(e, new_content) {
	    $(e.target).append(new_content);
	};
	fragments.clear_content = function(e, new_content) {
        $(e.target).html("");
	};
	$("fragment").bind("fragments.replace",fragments.replace_content);
	$("fragment").bind("fragments.append",fragments.append_content);
	$("fragment").bind("fragments.clear",fragments.clear_content);

	$.Mycelium.fragments = fragments;


// Search handler
	var sh = new Object();
	
	sh.options = {
	    search_queue_delay_ms: 50, 
	    striped_results: true,
	    highlight_results: true,
	    focus_on_setup: true,
	    search_element: $("input[type=search]"),
	    results_element: $("search_results"),
	    search_url: SEARCH_URL,
	    process_results_as_fragments: true,
	    process_results_as_replace_html: false,
	}
	sh.previous_query = "%*(#:LKCL:DSF@()#SDF)";
    sh.search_timeout = false;

	sh.setUp = function (options) {
		$.extend(true, sh.options, options);
        var t = $(sh.options.search_element);
        t.live("keydown",sh.queue_searching);
        t.live("change",sh.queue_searching);
        t.bind('keyup', 'return', function(){
            t.trigger("mycelium.search.return_pressed");
        });

        if (sh.options.focus_on_setup && !("autofocus" in document.createElement("input"))) {
            t.focus();
        }
	}
	
    sh.queue_searching = function() {
    	clearTimeout(sh.search_timeout);
    	sh.search_timeout = setTimeout(sh.update_search, sh.options.search_queue_delay_ms);
    }

    sh.update_search = function() {
        if (sh.previous_query != $.trim(sh.options.search_element.val())) {
            sh.previous_query = sh.q;
            sh.q = $.trim(sh.options.search_element.val());
            $.ajax({
              url: sh.options.search_url,
              type: "GET",
              dataType: "json",
              data: {'q':sh.q},
              mode: 'abort',
              success: function(json) {
                if (typeof(json) == typeof({})) {
                    if (sh.options.process_results_as_fragments) {
                        $.Mycelium.fragments.process_fragments_from_json(json)
                    }
                    if (sh.options.process_results_as_replace_html) {
                        $(sh.options.results_element).html(json.html);
                    }
                    if (sh.options.highlight_results) {
                        $.Mycelium.highlight_search_terms(sh.q,sh.options.results_element);
                    }
                    if (sh.options.striped_results) {
                        $.Mycelium.update_stripes(sh.options.results_element);
                    }
                }
        	 },
        	});

        }
    }
	$.Mycelium.search = sh;

// Highlights
    $.Mycelium.highlight_search_terms = function(q, context_ele) {
    	var space_queries = q.split(" ");
    	highlight_regexes = [];
    	for (var j in space_queries) {
    		var q = space_queries[j];
    		if (q != "") {
    			highlight_regexes.push(new RegExp(q, "gi"));

    			var dash_queries = q.split("-");
    			if (dash_queries.length > 1) {
    				for (var k in dash_queries) {
    					if (dash_queries[k] != "") {
    						highlight_regexes.push(new RegExp(dash_queries[k], "gi"));
    					}
    				}
    			}
    		}
    	}
    	$(".highlightable", context_ele).each(function(){
    		var text = $(this).text();
    		for (var j in highlight_regexes) {
    			text = text.replace(highlight_regexes[j], '<b>$&</b>')
    		}
    		$(this).html(text);
    	});

    }

// Striping
    $.Mycelium.update_stripes = function(context_ele) {
        $(".striped .striped_row:even",context_ele).addClass("even");
        $(".striped .striped_row:odd",context_ele).addClass("odd");
    }


});
