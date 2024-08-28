from django.apps import AppConfig
from datetime import datetime
import importlib
# from django.contrib.auth.models import Group


class LogsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'
    def ready(self):

        # Erstellung der Rechte Gruppen
        try:
            models = importlib.import_module('django.contrib.auth.models')
            if not models.Group.objects.filter(name='Admin').exists():
                models.Group.objects.create(name='Admin')
            if not models.Group.objects.filter(name='Gruppenleitung').exists():
                models.Group.objects.create(name='Gruppenleitung')
            if not models.Group.objects.filter(name='Raumbetreuer').exists():
                models.Group.objects.create(name='Raumbetreuer')
            if not models.Group.objects.filter(name='Ohne Rolle').exists():
                models.Group.objects.create(name='Ohne Rolle')
        except:
            pass

        # Erstelle verschiedene AGKategorien 
        try:
            models = importlib.import_module('main_app.models')
            if not models.AGKategorie.objects.filter(name='Sport').exists():
                models.AGKategorie.objects.create(name='Sport')
            if not models.AGKategorie.objects.filter(name='Lernen').exists():
                models.AGKategorie.objects.create(name='Lernen')
            if not models.AGKategorie.objects.filter(name='Kreativ').exists():
                models.AGKategorie.objects.create(name='Kreativ')
            if not models.AGKategorie.objects.filter(name='Ernährung').exists():
                models.AGKategorie.objects.create(name='Ernährung')
            if not models.AGKategorie.objects.filter(name='Natur').exists():
                models.AGKategorie.objects.create(name='Natur')
            if not models.AGKategorie.objects.filter(name='Gruppenraum').exists():
                models.AGKategorie.objects.create(name='Gruppenraum')
            if not models.AGKategorie.objects.filter(name='Ruhe').exists():
                models.AGKategorie.objects.create(name='Ruhe')
            if not models.AGKategorie.objects.filter(name='Sonstiges').exists():
                models.AGKategorie.objects.create(name='Sonstiges')
        except:
            pass
        try:
            models = importlib.import_module('main_app.models')
            r_bs = models.Raum_Belegung.objects.all()
            for raum_belegung in r_bs:
                raum = raum_belegung.raum
                if(models.Aufenthalt.objects.filter(raum_id=raum, zeitraum__endzeit=None).exists):
                    aufenthalte = models.Aufenthalt.objects.filter(raum_id=raum, zeitraum__endzeit=None)
                    for aufenthalt in aufenthalte:
                        zeitraum1 = aufenthalt.zeitraum
                        zeitraum1.endzeit = datetime.now().time()
                        zeitraum1.save()
                zeitraum = raum_belegung.zeitraum
                zeitraum.endzeit = datetime.now().time()
                zeitraum.save()
                raum_historie = models.Raum_Historie.objects.create(zeitraum=zeitraum,raum=raum,tag=datetime.now().date(),ag_name=raum_belegung.ag.name,ag_kategorie=raum_belegung.ag.ag_kategorie,leiter=raum_belegung.ag.leiter, max_anzahl=raum_belegung.ag.max_anzahl)
                raum_belegung.delete()
            models.AG.objects.all().delete()
            aufenthalte = models.Aufenthalt.objects.all()
            for aufenthalt in aufenthalte:
                if aufenthalt.zeitraum.endzeit == None:
                    aufenthalt.delete()
            for schueler in models.Schueler.objects.all():
                schueler.angemeldet = False
                schueler.save()
        except:
            pass

        try:
            models = importlib.import_module('django.contrib.auth.models')
            if not models.User.objects.filter(username="root").exists():
                newuser = models.User.objects.create_user(username="root", password="root")
                newuser.is_superuser = True
                newuser.save()
        except:
            pass

        try:
            models = importlib.import_module('main_app.models')
            groups = models.Gruppe.objects.all()
            for group in groups:
                group.vertreter = None
                group.save()
        except:
            pass