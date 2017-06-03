from django.db import models

# Create your models here.


class Session(models.Model):
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    name = models.TextField()
    slot = models.CharField(max_length=20)
    parallelOrder = models.IntegerField(default=0)
    room = models.ManyToManyField('Room')
    organizer = models.ManyToManyField('Staff',
                                       related_name='sessions')
    moderator = models.ManyToManyField('Staff',
                                       related_name='sessionsm')
    confirmed = models.BooleanField(default=False)
    abstract = models.TextField(default='')
    isotd = models.BooleanField(default=False)


class Speaker(models.Model):
    name = models.TextField()
    introduction = models.TextField()
    sessions = models.ManyToManyField('Session', related_name="Speakers")
    affliation = models.TextField(default='')
    registered = models.BooleanField(default=False)
    contact_staff = models.ForeignKey('Staff', models.SET_NULL,
                                      blank=True,
                                      null=True,)
    contacted = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    tacec_share = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.0)
    otd_share = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.0)


class Staff(models.Model):
    name = models.TextField()
    email = models.TextField()
    cellphone = models.CharField(max_length=15, default='(000)000-0000')
    OTD = 'OTD'
    TAC = 'TACEC'
    ORG = (
        (OTD, 'OTD'),
        (TAC, 'TACEC')
    )
    organization = models.CharField(choices= ORG, default=TAC, max_length = 6)


class Room(models.Model):
    name = models.TextField()
