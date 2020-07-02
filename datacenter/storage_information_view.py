from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def storage_information_view(request):
    non_closed_visits = []

    for visit in Visit.objects.filter(leaved_at=None):
        who_entered = visit.passcard.owner_name
        entered_at = localtime(visit.entered_at)
        duration = visit.format_duration()

        visit_card = {
            "who_entered" : who_entered,
            "entered_at" : entered_at,
            "duration" : duration
        }

        non_closed_visits.append(visit_card)
    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
