from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from conversations.forms import NewConversationForm
from people.models import Person

def _people_conversations_tab_context(context):
    conversation_form = NewConversationForm(account=context["request"].account)
    context.update({"conversation_form":conversation_form,})

    return context

def _render_people_conversations_tab(context):
    return render_to_string("conversations/_people_conversations_tab.html", RequestContext(context["request"],_people_conversations_tab_context(context)))


def _return_fragments_or_redirect(request,context):
    if request.is_ajax():
        return HttpResponse(simplejson.dumps( {"fragments":{"detail_tab":_render_people_conversation_tab(context)}}))
    else:
        return HttpResponseRedirect(reverse("people:person",args=(context["person"].pk,)))    


def save_new_conversation(request, person_id):
    person = get_or_404_by_account(Person, request.account, person_id, using='default')
    obj = person
    if request.method == "POST":
        form = NewConversationForm(request.POST, account=request.account)
        if form.is_valid():
            new_conversation = form.save(commit=False)
            new_conversation.person = person
            new_conversation.save()
        else:
            print form
    return _return_fragments_or_redirect(request,locals())

def delete_conversation_from_people_tab(request, conversation_id):
    c = get_or_404_by_account(Conversation, request.account, conversation_id, using='default')
    person = c.person
    c.delete()
    obj = person

    return _return_fragments_or_redirect(request,locals())
