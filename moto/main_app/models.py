from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import pre_delete
from django.dispatch import receiver


# Create your models here.

# Zeitraum enthält zwei Uhrzeiten
class Zeitraum(models.Model):
    startzeit = models.TimeField()
    endzeit = models.TimeField(null=True)
# Datumsraum enhält zwei Tage mit konkreter Uhrzeit
class Datumsraum(models.Model):
    startdatum = models.DateTimeField()
    enddatum = models.DateTimeField()
class Nutzer(models.Model):
    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    tag_id = models.CharField(max_length=100, null=True)          #max_length abhängig von Tags id länge
    # email = models.CharField(max_length=100)
class Personal(models.Model):
    rolle = models.CharField(max_length=40)
    rechte_gruppe = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)       # null=True rausmachen
    nutzer = models.ForeignKey(Nutzer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null= True)    # null=True rausmachen
    is_password_otp = models.BooleanField(default=True)

    class Meta:
        permissions = [("can_import", "Can import excel data")]

class Raum(models.Model):
    raum_nr = models.CharField(max_length=15)
    geschoss = models.CharField(max_length=15)
    kapazitaet = models.SmallIntegerField()
    kategorie = models.CharField(max_length=30, null = True)
    color = models.CharField(max_length=7, default="#FFFFFF", help_text="Hex color code, e.g., #FFFFFF for white")

    def get_schueler_in_raum(self):
        aufenthalte = Aufenthalt.objects.filter(raum_id=self, zeitraum__endzeit__isnull=True)
        return [a.schueler_id for a in aufenthalte]
class Gruppe(models.Model):
    name = models.CharField(max_length=50)
    gruppen_leiter = models.ManyToManyField(Personal)        # ? mehere Gruppenleiter?
    raum = models.ForeignKey(Raum, on_delete=models.SET_NULL, null=True, related_name='leitende_gruppen')
    vertreter = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, related_name='vertretende_gruppen')

class AGZeit(models.Model):
    class WOCHENTAG(models.TextChoices):
        MONTAG = "Montag"
        DIENSTAG = "Dienstag"
        MITTWOCH = "Mittwoch"
        DONNERSTAG = "Donnerstag"
        FREITAG = "Freitag"
    
    wochentag = models.TextField(choices=WOCHENTAG.choices, default=WOCHENTAG.MONTAG, max_length=10)
    zeitraum = models.ForeignKey(Zeitraum, on_delete=models.CASCADE)

class AGKategorie(models.Model):
    name = models.CharField(max_length=100)

class AG(models.Model):
    name = models.CharField(max_length=50)
    max_anzahl = models.SmallIntegerField()
    offene_AG = models.BooleanField() 
    leiter = models.ForeignKey(Personal, on_delete=models.CASCADE, null=True)       # null=True entfernen
    angebots_datum_raum = models.ForeignKey(Datumsraum, on_delete=models.CASCADE, null=True)    # null=True entfernen
    ag_zeit = models.ManyToManyField(AGZeit)
    ag_kategorie = models.ForeignKey(AGKategorie, on_delete=models.CASCADE, null=True)
    zeitraum = models.ForeignKey(Zeitraum, on_delete=models.CASCADE, null = True)

class Schueler(models.Model):
    klasse = models.CharField(max_length=3)             # optional
    bus_kind = models.BooleanField()
    name_eb = models.CharField(max_length=100)
    kontakt_eb = models.CharField(max_length=300)
    angemeldet = models.BooleanField(default=False)      # Ist kind überhaupt an diesem Tag in der OGS
    wc = models.BooleanField(default=False)
    schulhof = models.BooleanField(default=False)
    user_id = models.ForeignKey(Nutzer, on_delete=models.SET_NULL, null=True)
    gruppen_id = models.ForeignKey(Gruppe, on_delete=models.CASCADE)
    ag_buchungen = models.ManyToManyField(AG)
class Feedback(models.Model):
    class Feedbacks(models.TextChoices):
        GOOD = "GOOD", "Good"
        MEDIUM = "MEDIUM", "Medium"
        BAD = "BAD", "Bad"

    feedback_wert = models.CharField(choices=Feedbacks.choices, default=Feedbacks.MEDIUM, max_length=6)
    tag = models.DateField()
    zeit = models.TimeField()
    schueler_id = models.ForeignKey(Schueler, on_delete=models.CASCADE)
    mensa_feedback = models.BooleanField(default=False)
class Raum_Belegung(models.Model):
    tablet_id = models.CharField(max_length=200,null=True)
    raum = models.ForeignKey(Raum, on_delete=models.CASCADE)
    ag = models.ForeignKey(AG, on_delete=models.CASCADE)
    gruppe = models.ForeignKey(Gruppe, on_delete=models.CASCADE, null=True)
    zeitraum = models.ForeignKey(Zeitraum, on_delete=models.CASCADE)
    aufsichtspersonen = models.ManyToManyField(Personal)
class Aufenthalt(models.Model):                # Zuordnung wo sich Kinder befunden haben, wird mit löschen des Zeitraums auch gelöscht
    tag = models.DateField()
    schueler_id = models.ForeignKey(Schueler, on_delete=models.CASCADE)
    raum_id = models.ForeignKey(Raum, on_delete=models.CASCADE)
    zeitraum = models.ForeignKey(Zeitraum, on_delete=models.CASCADE)
class Raum_Historie(models.Model):
    raum = models.ForeignKey(Raum, on_delete=models.CASCADE)
    ag_name = models.CharField(max_length=50, null = True)
    tag = models.DateField()
    zeitraum = models.ForeignKey(Zeitraum, on_delete=models.CASCADE)
    ag_kategorie = models.ForeignKey(AGKategorie, on_delete=models.CASCADE, null = True)
    leiter = models.ForeignKey(Personal, on_delete=models.CASCADE)
    max_anzahl = models.SmallIntegerField()
# class Buchung_AG(models.Model):            # Zuordunung zwischen Schüler und AGS
#     schueler_id = models.ForeignKey(Schueler, on_delete=models.CASCADE)
#     ag_id = models.ForeignKey(AG, on_delete=models.CASCADE)
    
@receiver(pre_delete, sender=Schueler)
def delete_related_user(sender, instance, **kwargs):
    if instance.user_id:
        user = instance.user_id
        instance.user_id = None  # Um eine Endlosschleife zu verhindern, setzen Sie das ForeignKey-Feld auf None
        user.delete()