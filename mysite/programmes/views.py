from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView, ListView
from django.urls import reverse_lazy
from .models import Lesson, Quiz, Question, Option
from .forms import LessonForm, ComForm, RepForm
from django.http import HttpResponseRedirect, FileResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required

class LessonListView(ListView):# vue utilise toutes leçons dans le template (lessonlist.html)
    model = Lesson
    template_name = 'programmes/lessonlist.html'
    context_object_name = 'lessons'
    def get_queryset(self):
        return Lesson.objects.all()

class LessonListViewDetail(DetailView, FormView):#affiche les details d une leçon dans template (lessonlistdetail.htm)
    context_object_name = 'lesson'
    model = Lesson
    template_name = 'programmes/lessonlistdetail.html'
    form_class = ComForm
    second_form_class = RepForm

    def get_context_data(self, **kwargs):
        context = super(LessonListViewDetail, self).get_context_data(**kwargs)

        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()

        context['quizzes'] = Quiz.objects.filter(lesson=self.object)

        return context

    def form_valid(self, form):
        self.object = self.get_object()
        fd = form.save(commit=False)
        fd.auteur = self.request.user
        fd.nom_lesson_id = self.object.pk
        fd.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_valid2(self, form):
        self.object = self.get_object()
        fd = form.save(commit=False)
        fd.auteur = self.request.user
        fd.nom_comm_id = self.request.POST.get('comment_id')
        fd.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('programmes:lessonlistdetail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form2' in request.POST:
            form_class = self.second_form_class
            form_name = 'form2'
        else:
            form_class = self.form_class
            form_name = 'form'
        
        form = form_class(request.POST)

        if form_name == 'form' and form.is_valid():
            return self.form_valid(form)

        if form_name == 'form2' and form.is_valid():
            return self.form_valid2(form)
        
        return self.render_to_response(self.get_context_data(form=form))

class LessonCreateView(UserPassesTestMixin, CreateView):
    form_class = LessonForm
    model = Lesson
    template_name = 'programmes/lessoncreate.html'

    def get_success_url(self):
        return reverse_lazy('programmes:lessonlistslug', kwargs={'slug': self.object.slug})

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.creer_par = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='ENSEIGNANT').exists()


    

class LessonUpdateView(UpdateView):
    fields = ('nom', 'position', 'pdf', 'fpe')
    context_object_name = 'lesson'
    model = Lesson
    template_name = 'programmes/lessonupdate.html'

    def get_success_url(self):
        return reverse_lazy("programmes:lessonlist")

class LessonDeleteView(DeleteView):
    model = Lesson
    context_object_name = "lesson"
    template_name = 'programmes/lessondelete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.session['slug'] = self.object.slug
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("programmes:lessonlist")
    
class QuizView(DetailView):
    model = Quiz
    template_name = 'programmes/quiz.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(quiz=self.object).prefetch_related('option_set')
        return context
    
    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        questions = quiz.question_set.all()
        score = 0
        
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = get_object_or_404(Option, id=selected_option_id)
                if selected_option.is_correct:
                    score += 1

        # Store the score in the session
        request.session['score'] = request.session.get('score', 0) + score
        
        # Get the next quiz in the same lesson
        next_quiz = Quiz.objects.filter(lesson=quiz.lesson, id__gt=quiz.id).first()
        
        if next_quiz:
            return redirect('programmes:quiz_view', pk=next_quiz.id)
        else:
            return redirect('programmes:quiz_result')



class QuizResultView(DetailView):
    template_name = 'programmes/quiz_result.html'
    
    def get(self, request, *args, **kwargs):
        score = request.session.get('score', 0)
        del request.session['score']
        return render(request, self.template_name, {'score': score})
    
    

def quiz_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.question_set.all()
    return render(request, 'quiz.html', {'quiz': quiz, 'questions': questions})

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'programmes/quiz_detail.html'
    context_object_name = 'quiz'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.question_set.all()
        return context
    
    def get_queryset(self):
        return Quiz.objects.filter(lesson__slug=self.kwargs['slug'])
    
class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz_list.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        # Récupérer la leçon associée à l'URL
        lesson_slug = self.kwargs['slug']
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        
        # Filtrer les quiz associés à la leçon
        return Quiz.objects.filter(lesson=lesson)
    
    
def lesson_detail(request, lesson_id):
    # Récupérer la leçon actuelle
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    # Filtrer les quiz associés à la leçon actuelle
    quizzes = Quiz.objects.filter(lesson=lesson)

    context = {
        'lesson': lesson,
        'quizzes': quizzes,
    }

    return render(request, 'lesson_detail.html', context)

def download_lesson_pdf(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    return FileResponse(open(lesson.pdf.path, 'rb'), content_type='application/pdf')
