import random

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .models import *
import django.db.models
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
import json
from django.core.serializers import deserialize


def home(request):
    context = {"username":get_username(request)}
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')  # Переход на главную страницу или другую
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def test_page(request):
    """
    Страница просмотра тестов для начала прохождения тесты создаются в админке
    """
    tests = Test.objects.filter(is_active=True)
    context = {"tests": tests}
    return render(request, 'test_page.html', context)


@login_required
def do_pass_test(request, id_of_test):
    test = Test.objects.get(pk=id_of_test)
    size_of_questions = test.questions.count if test.questions.count() < test.size_of_pages else test.size_of_pages
    rand_num_of_question = [random.randint(0, size_of_questions-1) for i in range(size_of_questions)]
    print("1 шаг")
    # Сформировал список рандомных запросов
    questions = test.questions.all()
    questions_data = serialize('json',questions)
    print("2 шаг")
    # Получение вариантов ответа с правильными
    answer_options = get_answer_options_for_question(questions)
    answer_options_data = serialize_answer_option(answer_options)
    context = {"test": test, "questions": questions, "size_of_questions": size_of_questions,"username":get_username(request),"is_not_next_question":True}
    request.session['answers'] = []
    request.session['questions'] = [questions_data]
    request.session['answer_options']=answer_options_data
    request.session['test'] =json.loads(serialize('json', [test]))
    request.session['len_of_questions']=test.questions.count()
    request.session['current_question']=0
    request.session['numbers_of_questions']=[i for i in  range(test.questions.count())]
    request.session['answers_of_questions']=[[] for _ in range(test.questions.count())]
    return render(request, 'do_pass_test.html', context)


@login_required
def get_next_question (request, num_of_question):
    # For debug
    if request.session.get("answers") is None:
        print("get_next_qestion answer is None")
    if request.session.get("questions") is None:
        print("get_next_qestion questions is None")
    if request.session.get("test") is None:
        print("get_next_qestion test is None")
    if request.session.get("answer_options") is None:
        print("get_next_qestion answer_options is None")
    selected_indices = request.GET.getlist('answers')
    current_question = request.session.get('current_question')
    numbers_or_questions =request.session['numbers_of_questions']
    answers_of_questions =request.session['answers_of_questions']
    question_data = json.loads(request.session.get("questions")[0])
    dict_string =question_data[num_of_question]
    question =Question.objects.get(pk=dict_string.get("pk"))
    request.session['current_question'] = question
    # Так как десериализация пошла не так как надо решил сделать просто через id
    random_answers = request.session.get("answer_options")[num_of_question][1]
    # random_answers =[json.loads(i) for i in random_answers]
    random_answers = [Answer.objects.get(pk=i.get("pk")) for i in random_answers]
    if num_of_question+1<request.session.get("len_of_questions"):
        next_link = "get_next_question"
        next_question = str(num_of_question+1)
        next_link_name = "Вопрос "+str(num_of_question+1)
        is_not_next_question = True
    else:
        next_link = "end_test"
        next_question = None # Не работает
        next_link_name = "Завершить тест"
        is_not_next_question = False

    request.session['current_question'] = num_of_question
    request.session["answers_of_questions"][current_question] = [int(i) for i in selected_indices]
    context= {"next_link": next_link, "num_of_question": num_of_question, "numbers_of_question": numbers_or_questions,
              "answers_of_questions":answers_of_questions,"is_not_next_question":is_not_next_question ,
              "question": question, "random_answers": random_answers,'next_question':next_question,
              "next_link_name":next_link_name,
              'selected_answers': request.session["answers_of_questions"][num_of_question]}
    return render(request, 'get_next_question.html', context)

@login_required
def end_test(request):
    selected_indices = request.GET.getlist('answers')
    current_question = request.session.get('current_question')
    request.session["answers_of_questions"][current_question] = selected_indices
    answers_of_questions = request.session.get('answers_of_questions')
    answers_of_questions = [[Answer.objects.get(pk = j) for j in i] for i in answers_of_questions]
    answer_options = request.session.get("answer_options")
    answer_options = [[[Answer.objects.get(pk = (k).get('pk'))for k in j] for j in i]for i in answer_options]
    right_answers = []
    incorrect_answers= []
    for i, answer_option in enumerate(answer_options):
        right_ans = answer_option[0]
        res = []
        for r in right_ans:
            if r in answers_of_questions[i]:
                res.append(r)
        right_ans = res
        len_of_answers= len(answer_options[1])
        right_answers.append(len(right_ans))
        incorrect_answers.append(len_of_answers-len(right_ans))
    context={"right_answers":right_answers, "incorrect_answers":incorrect_answers, "username":get_username(request)}
    return render(request, 'end_test', context)




def get_answer_options_for_question(questions):
    """
    Метод возвращает варианты ответов, включающий в себя как минимум 1 правильный ответ
    но не более чем половину вариантов ответа (в случае всего 1 варианта ответа и отсутствия вариантов более,
    либо если размер вариантов ответа равен 1,  возвращает только 1 правильный ответ)
    """
    """
    return answer_options[right_answer, other_answers, random_answers]
    """
    answer_options = []
    for question in questions:
        size_of_right_answers = question.right_answers.count() if  question.right_answers.count() < question.size_of_answers / 2  else question.size_of_answers / 2 if question.answer_options.count() / 2 > 1 else 1
        size_of_other_answers = (
            question.size_of_answers if question.size_of_answers < question.answer_options.count() else question.answer_options.count() - size_of_right_answers)
        # Получаем массив сгенерированных правильных ответов
        right_answer = [question.right_answers.all()[random.randint(0, question.right_answers.count()-1)] for _ in
                        range(size_of_right_answers)]
        # Отсекаем все правильные ответы
        other_answers = question.answer_options.exclude(id__in=[i.id for i in right_answer]).all()
        random_answers = list(right_answer)+list(other_answers)
        random.shuffle(random_answers)
        answer_options.append([right_answer, random_answers])
    return answer_options


def get_username(request):
    if request.user is not None:
        username = request.user.username
    else:
        username = ""
    return username


def serialize_answer_option(answer_options):
    result =[]
    for answer_option in answer_options:
        right_answers=json.loads(serialize('json', answer_option[0]))
        other_answers=json.loads(serialize('json', answer_option[1]))
        result.append([[right_answers],[other_answers]])
    return result