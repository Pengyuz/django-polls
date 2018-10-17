from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,JsonResponse,HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.views import generic
import json
from django.urls import reverse
from django.template import loader

from .models import Question,Choice,member

def homepage(request):
    name = request.POST['name']
    no = member.objects.filter(name = name).count()
    flag = 0
    if no == 0:
        user = member(name = name,gender = 1)
        user.save()
    else:
        flag = 1
    return render(request,'polls/homepage.html',{'flag':flag})

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request,'polls/index.html',context)
#
# # Leave the rest of the views (detail, results, vote) unchanged
#
# def detail(request,question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def login(request):
    return render(request,'polls/login.html',{})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@require_http_methods(["GET"])
def show_questions(request):
    response = {}

    questions = Question.objects.filter()
    response['list'] = json.loads(serializers.serialize("json",questions))
    response['msg'] = 'success'
    response['error_num'] = 0

    # except Exception as e:
    #     response['msg'] = e.__str__()
    #     response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def show_choices(request):
    response = {}
    choices = Choice.objects.filter()
    response['list'] = json.loads(serializers.serialize("json",choices))
    response['msg'] = 's'

    return JsonResponse(response)

# @require_http_methods(["GET"])
# def reset_data(request):
#     response = {}
#     q = Question.objects.get(pk=1)
#     c1 = Choice(choice_text = 'fine',votes = 0)
#     c2 = Choice(choice_text='not fine', votes=0)
#     c1.question = q
#     c2.question = q
#     c1.save()
#     c2.save()
#     questions = Question.objects.filter()
#     choices = Choice.objects.filter()
#     response['questions'] = json.loads(serializers.serialize("json",questions))
#     response['Choice'] = json.loads(serializers.serialize('json',choices))
#     response['msg'] = 's'
#     response['error_num'] = 0
#     return JsonResponse(response)
