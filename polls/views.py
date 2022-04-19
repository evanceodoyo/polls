from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.db.models import F
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice



# Get and display questions. 
def index(request):
    """Reutrn the last five published questions (not including those set to be published in the future)."""
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    """Display specific questions and their choices."""
    try:
        question = Question.objects.filter(pub_date__lte=timezone.now()).get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    """Get question and display results."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    """Vote/choose a question choice."""
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the voting form
        return render(request, 'polls/detail.html', {'question': question, 'error_message':"You didn't select a choice.", })
    else:
        # Avoiding race condition using Django's F() module.
        #selected_choice.votes = F('votes') + 1

        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



