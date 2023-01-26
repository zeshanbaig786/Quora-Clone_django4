from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import Question, Profile, Answer, Vote
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm, QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required

def get_profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
    else:
        profile = None
    return {"profile": profile}

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            p = Profile(user=user)
            p.save()

            messages.success(
                request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'quora/register.html', context)


@login_required
def index(request):
    # list all questions
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("login/")
    profile = get_object_or_404(Profile, user=request.user)
    queryset_list = Question.objects.all().order_by("-timestamp")
    context = {
        "questions": queryset_list,
        "v": Vote.objects.filter(user=request.user.id).count(),
    }
    return render(request, "quora\index.html", context)


@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            profile = get_object_or_404(Profile, user=request.user)
            question = form.save(commit=False)
            question.user = profile
            # Finally write the changes into database
            question.save()
            profile.points = profile.points + 2
            profile.questions = profile.questions + 1
            profile.save()
            messages.success(request, f'Question saved!')
            return redirect('home')
        else:
            print("")
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'quora/create_question.html', context)


@login_required
def question_detail(request, id):
    q = get_object_or_404(Question, id=id)
    profile = get_object_or_404(Profile, user=request.user)
    q.views = q.views + 1
    q.save()
    if request.method == "POST":
        if request.user.is_authenticated:
            answerForm = AnswerForm(request.POST)
            answer = answerForm.save(commit=False)
            answer.question = q
            answer.user = profile
            profile.points = profile.points + 1
            profile.answers = profile.answers + 1
            q.answers = q.answers + 1
            profile.save()
            q.save()
            answer.save()
        else:
            messages.error(request, "Please log in to answer.")
            return HttpResponseRedirect("login")

    answeres = Answer.objects.filter(question=q)
    answerform = AnswerForm()
    context = {
        "question": q,
        "answers": answeres,
        'form': answerform
    }
    return render(request, 'quora/question_detail.html', context)


@login_required
def vote_up(request, id=None):
    answer = get_object_or_404(Answer, id=id)
    if Vote.objects.all().filter(answer=answer, user=request.user).exists():
        vote = get_object_or_404(Vote, answer=answer, user=request.user)
        if vote.vote == -1:
            answer.votes = answer.votes + 2
            answer.save()
            vote.vote = 1
            vote.save()
            answer.user.points = answer.user.points + 10
            answer.user.save()
            return HttpResponseRedirect("/question_detail/" + str(answer.question.id))
        else:
            messages.error(request, "Already voted up")
            return HttpResponseRedirect("/question_detail/" + str(answer.question.id))
    else:
        vote = Vote(answer=answer, user=request.user, vote=1)
        answer.votes = answer.votes + 1
        answer.save()
        vote.save()
        return HttpResponseRedirect("/question_detail/" + str(answer.question.id))


@login_required
def vote_down(request, id=None):
    answer = get_object_or_404(Answer, id=id)
    if Vote.objects.filter(answer=answer, user=request.user).exists():
        vote = get_object_or_404(Vote, answer=answer, user=request.user)
        if vote.vote == 1:
            answer.votes = answer.votes - 2
            answer.save()
            vote.vote = -1
            vote.save()
            answer.user.points = answer.user.points - 10
            answer.user.save()
            return HttpResponseRedirect("/question_detail/" + str(answer.question.id))
        else:
            messages.error(request, "Already voted down")
            return HttpResponseRedirect("/question_detail/" + str(answer.question.id))
    else:
        vote = Vote(answer=answer, user=request.user, vote=-1)
        instance.votes = instance.votes - 1
        instance.save()
        vote.save()
        return HttpResponseRedirect("/question_detail/" + str(answer.question.id))


@login_required
def accept_as_answer(request, id=None):
    answer = get_object_or_404(Answer, id=id)
    if request.user == answer.question.user.user:
        answer.accepted = 1
        answer.user.points = answer.user.points + 10
        answer.user.save()
        answer.save()
        answer.question.answered = 1
        answer.question.save()
        return HttpResponseRedirect("/question_detail/" + str(answer.question.id))
    else:
        messages.error(request, "User unauthorized.")
        return HttpResponseRedirect("/question_detail/" + str(answer.question.id))


@login_required
def unaccept_as_answer(request, id=None):
    answer = get_object_or_404(Answer, id=id)
    if request.user == answer.question.user.user:
        answer.accepted = 0
        answer.user.points = answer.user.points - 10
        answer.user.save()
        answer.save()
        if Answer.objects.filter(question=answer.question, accepted=1).exists():
            answer.question.answered = 1
        else:
            answer.question.answered = 0
        answer.question.save()
        return HttpResponseRedirect("/question_detail/" + str(answer.question.id))
    else:
        messages.error(request, "User unauthorized.")
        return HttpResponseRedirect("/question_detail/" + str(answer.question.id))


@login_required
def view_profile(request, id=None):
    profile = None
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, id=id)
        if profile.points < 100:
            color = "#3498db"
            rank = "Amateur"
        elif profile.points < 1000:
            color = "#1abc9c"
            rank = "Trainee"
        elif profile.points < 2000:
            color = "gold"
            rank = "Professor"
        else:
            color = "red"
            rank = "Legend"
    # else:
    #     profile = get_object_or_404(Profile, id=1)
    #     val = ""
    #     percent = 100
    context = {
        "color": color,
        "rank": rank
    }
    return render(request, "quora/profile.html", context)
