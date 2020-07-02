from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)

    this_passcard_visits = []
    for visit in Visit.objects.filter(passcard=passcard):
        duration = visit.format_duration()
        is_strange = visit.is_visit_long()
        entered_at = localtime(visit.entered_at)

        visit_card = {
            "entered_at" : entered_at,
            "duration" : duration,
            "is_strange" : is_strange 
        }

        this_passcard_visits.append(visit_card)

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits # информация о посещениях
    }
    return render(request, 'passcard_info.html', context)
