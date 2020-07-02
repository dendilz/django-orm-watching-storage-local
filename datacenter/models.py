from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    def get_duration(self):
        delta = localtime(self.leaved_at) - localtime(self.entered_at)
        return int(delta.total_seconds())

    def is_visit_long(self, minutes=600):
        if self.leaved_at:
            delta = localtime(self.leaved_at) - localtime(self.entered_at)
        else:
            delta = localtime() - localtime(self.entered_at)
        return delta.total_seconds() // 60 > minutes

    def format_duration(self):
        h = (self.get_duration() // 3600) % 24
        m = (self.get_duration() // 60) % 60
        s = self.get_duration() % 60
        return "{:02d}ч.{:02d}м.{:02d}с.".format(h, m, s)
