# Template tag
from datetime import date, timedelta

from django import template
#from myapp.models import Event # You need to change this if you like to add your own events to the calendar

register = template.Library()

def get_last_day_of_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)


def month_cal(year=date.today().year, month=date.today().month):
#    event_list = Event.objects.filter(start_date__year=year, start_date__month=month)

    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    month_cal = []
    week = []
    week_headers = []
    now = date.today()

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = False
        cal_day['count'] = 0
        cal_day['now'] = False
        if Deposito.objects.filter(jatuh_tempo=day).count() > 0:
            total_deposito = total_cutoff = 0
            for d in Deposito.objects.filter(jatuh_tempo=day):
                total_deposito += d.nilai
                total_cutoff += d.cutoff()
            cal_day['event'] = True
            cal_day['count'] = Deposito.objects.filter(jatuh_tempo=day).count()
            cal_day['cutoff'] = total_cutoff
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False
        if day == now:
            cal_day['now'] = True
        week.append(cal_day)
        if day.weekday() == 6:
            month_cal.append(week)
            week = []
        i += 1
        day += timedelta(1)

    return {'calendar': month_cal, 'headers': week_headers}

register.inclusion_tag('elements/month_cal.html')(month_cal)

"""
Put this in your template (in my case agenda/month_cal.html):

<table class="cal_month_calendar">
<tr>
{% for day in headers %}
<th>{{ day|date:"D"|slice:":2" }}</hd>
{% endfor %}
</tr>
{% for week in calendar %}
<tr>
{% for day in week %}
<td{% if not day.in_month %} class="cal_not_in_month"{% endif %}>{% if day.event %}<a href="/calendar/{{ day.day|date:"Y/m" }}/">{{ day.day|date:"j" }}</a>{% else %}{{ day.day|date:"j" }}{% endif %}</td>
{% endfor %}
</tr>
{% endfor %}
</table>

"""
