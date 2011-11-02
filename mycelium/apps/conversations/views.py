from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from django.db import transaction

from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from conversations.models import Conversation
from conversations.forms import NewConversationForm
from people.models import Person
from conversations import CONVERSATION_TYPES, MORE_CONVERSATIONS_SIZE
from activities.tasks import save_action

def _people_conversations_tab_context(context):
    conversation_form = NewConversationForm(account=context["request"].account)
    conversation_form.initial["staff"] = context["request"].useraccount
    new_start_index = 3
    context.update({"conversation_form":conversation_form,'CONVERSATION_TYPES':CONVERSATION_TYPES,'new_start_index':new_start_index})

    return context

def _render_people_conversations_tab(context):
    return render_to_string("conversations/_people_conversations_tab.html", RequestContext(context["request"],_people_conversations_tab_context(context)))


def _return_fragments_or_redirect(request, context):
    if request.is_ajax():
        return HttpResponse(simplejson.dumps( {"fragments":{"detail_tab":_render_people_conversations_tab(context)}}))
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
            try:
                transaction.commit()
            except:
                pass
            save_action.delay(request.account, request.useraccount, "added a conversation", person=person, conversation=new_conversation)
        else:
            print form
    
    return _return_fragments_or_redirect(request,locals())

def delete_conversation_from_people_tab(request, conversation_id):
    c = get_or_404_by_account(Conversation, request.account, conversation_id, using='default')
    person = c.person
    c.delete()
    obj = person

    return _return_fragments_or_redirect(request,locals())


def more_conversations(request, person_id, start_index):
    start_index = int(start_index)
    person = get_or_404_by_account(Person, request.account, person_id, using='default')
    new_start_index = start_index + MORE_CONVERSATIONS_SIZE
    conversations = person.conversations.all()[start_index:new_start_index]
    there_are_more_conversations = person.conversations.all().count() > new_start_index

    if request.is_ajax():
        return HttpResponse(simplejson.dumps( {"fragments":{"more_conversations":render_to_string("conversations/_more_conversations.html", RequestContext(request,locals()))}}))
    else:
        return HttpResponseRedirect(reverse("people:person",args=(person.pk,)))    

    

    
