from django.db import models
from django.contrib.auth.models import User
import os

def renomer_image(instance, filename):#definir chemin ou l image du profil sera téléchargé
    upload_to = 'image/'
    ext = filename.split('.')[-1]
    if instance.user.username:
        filename = "photo_profile/{}.{}".format(instance.user.username, ext)
    return os.path.join(upload_to, filename)

class Profile(models.Model):#chaque utilisateur a un sul profil,et haque profil est lié à un seul utilisateur
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    photo_profile = models.ImageField(upload_to=renomer_image, blank=True)
    is_approved = models.BooleanField(default=False)  #indique si le profil approuvé ou non par l'administrateur

    ETUDIANT = 'etudiant'
    ENSEIGNANT = 'enseignant'
    PARENT = 'parent'

    TYPE_USER_CHOICES = [
        (ETUDIANT, 'Étudiant'),
        (ENSEIGNANT, 'Enseignant'),
        (PARENT, 'Parent'),
    ]

    type_profil = models.CharField(max_length=100, choices=TYPE_USER_CHOICES, default=ETUDIANT)
    # stocke le type de profil d utilisatur 
    # le mot de passe est passé est stockée dans le champ
    def __str__(self):
        return self.user.username
