from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse

class Lesson(models.Model):# represente une leçon et ses differents attributs dans la base du donnée
    lesson_id = models.AutoField(primary_key=True)
    creer_par = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    position = models.PositiveSmallIntegerField(verbose_name='chapitre no')
    video = models.FileField(upload_to="Video", null=True, blank=True, verbose_name="cours en video")
    fpe = models.FileField(upload_to="FPE", null=True, blank=True, verbose_name="Fichier en presentation")
    pdf = models.FileField(upload_to="PDF", null=True, blank=True, verbose_name="cours en PDF")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("programmes:lessonlist", kwargs={"slug": self.slug})

class Commentaire(models.Model):# represente un commentaire sur un leçon
    nom_lesson = models.ForeignKey(Lesson, null=True, on_delete=models.CASCADE, related_name='comments')
    nom_comm = models.CharField(max_length=100, blank=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    corps = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.nom_comm = slugify("commente par " + str(self.auteur) + " a " + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_comm
    
    class Meta:
        ordering = ['-date_added']

class Reponse(models.Model):
    nom_comm = models.ForeignKey(Commentaire, on_delete=models.CASCADE, related_name='reponses')
    corps = models.TextField(max_length=500)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reponse a " + str(self.nom_comm.nom_comm)
    
class Quiz(models.Model):
    name = models.CharField(max_length=200)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    answer = models.CharField(max_length=200, blank=True, null=True)  # Autoriser les valeurs nulles


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
