from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Question, Choice


# Create your views here.


def index(request):
    """displays the latest few questions."""
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {"latest_question_list": latest_question_list}
    # output = " ".join(question.question_text for question in latest_question_list)
    # return HttpResponse(output)

    # Shortcut:
    # https://docs.djangoproject.com/en/3.2/topics/http/shortcuts/#django.shortcuts.render
    # to render: request object, template name, dictionary (optional) etc
    # return render(request, 'polls/index.html', context) ->>>
    return HttpResponse(template.render(context, request))


def polls2(request):
    return render(request, "dj4e.htm")


def owner(request):
    return HttpResponse("Hello, world. 4a7a6fd7 is the polls index.")


def detail(request, question_id):
    """ displays a question text, with no results but with a form to vote."""
    # return HttpResponse("You're looking at question %s." % question_id)

    # try:
    #     question = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, "polls/details.html", {'question': question.question_text})

    # Shortcut:
    # The get_object_or_404() function takes a Django model as its
    # first argument and an arbitrary number of keyword arguments,
    # which it passes to the get() function of the model’s manager.
    # It raises Http404 if the object doesn’t exist
    question = get_object_or_404(Question, id=question_id)
    return render(request, "polls/details.html", {"question": question})


def results(request, question_id):
    """ displays results for a particular question."""
    response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)

    question = get_object_or_404(Question, id=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    """handles voting for a particular choice in a particular question."""
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST.get('choice'))
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question": question, "error_message": "You didn't select choice"})
    else:  # exec if no error
        selected_choice.votes += 1
        selected_choice.save()
        # return HttpResponseRedirect(reverse("polls:results", args=(question.id)))
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # you should always return an HttpResponseRedirect after successfully dealing with POST data.
        # reverse() helps avoid having to hardcode a URL in the view function


class IndexView(ListView):
    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'
    # the automatically generated context variable is question_list, we override this

    def get_queryset(self):
        return Question.objects.order_by('pub_date')[:5]


class DetailsView(DetailView):
    model = Question
    template_name = "polls/details.html"


class ResultsView(DetailView):
    model = Question
    template_name = "polls/results.html"
    context_object_name = 'question'

def hello(request):
    resp = HttpResponse("Hello bitches.")
    resp.set_cookie('dj4e_cookie', '4a7a6fd7', max_age=1000)
    return resp