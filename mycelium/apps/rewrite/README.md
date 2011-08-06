django-rewrite is a simple-to-use website and blog application for django.

Overview
========
Rewrite is a user-centric website and blogging application for Django.  It's designed to be simple to use. Its target audience is people and organizations who need a "website", and who aren't particularly likely to know what a "CMS" is.  Editing websites and posting blog entries should be simple.  We built rewrite to make it that way.


Why another CMS/Blog?!?!?!
==========================

Don't get me wrong, there are some great CMS and Blog projects for Django out there, Django-CMS and Mezzanine chief among them.  But they're also industrial-weight solutions, requiring lots of tuning for simple setups.  They're also built around the Django admin site - which is really more of a data-editing scaffold than a true content-administration UI.  

I created django-rewrite to provide a simple website editor and blog that was a joy to use, and where users would always know what their content looked like, and how to change it.

If you have multiple, nested sections of content, please use one of the industrial solutions.  If you *need* tracebacks in your blog, please use one of the heavier blogging apps.  But for the 90% of projects that don't need those advanced features, here's something simpler.



Dependencies
============


Installation
============


Usage
=====


Templates and Styling
=====================

CSS is good. JS is good.  You have full control of both in styling up pages.  By default, the base templates include:

* HTML5 Boilerplate
* jQuery
* jQuery UI
* 1140px templating system.

We've taken the simplest and most flexibile approach to page customization by providing a few flexibile integration points.  The final page is rendered roughly like this:

```
<html>
	<head>
	  <title>{{ page title }}</title>
	  <meta name="description" content="{{ page description }}">
	  <meta name="keywords" content="{{ page keywords }}">

	  {# Core JS #}
	  {{ template.extra_head_html }}
	</head>
	<body>
	  {{ template.page_header_html }}
	  {# main navigation #}
	  {# section navigation #}

	  {{ template.pre_content_html }}
	  {{ page.content }}
	  {{ template.post_content_html }}
	 </body>
</html>
```

This means that you can add side content, headers, footers, and pretty much whatever you'd like in a template.  You can also disable the navigation, either via the interface, or with CSS.

Typically, the use case is that developers build out a first template or two for their clients, using their HTML skills.  There's no pretty UI editing to the template HTML chunks, and that's by design. Knowledge of HTML isn't necessary to use the editor or the blog, but it is for the templates. We want that to be abundantly clear to users.


Advanced Integration
====================

You can also use rewrite as a set of base classes and functionality, and extend to integrate with your particular needs.

- include URLS
- include views
- include models and subclass.