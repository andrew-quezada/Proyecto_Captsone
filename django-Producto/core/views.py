from django.shortcuts import render
import plotly.express as px

from core.forms import DateForm
from core.models import Productos


def chart(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    Productos = Productos.objects.all()
    if start:
        Productos = Productos.filter(date__gte=start)
    if end:
        Productos = Productos.filter(date__lte=end)

    fig = px.line(
        x=[c.date for c in Productos],
        y=[c.average for c in Productos],
        title="Productos PPM",
        labels={'x': 'Date', 'y': 'Productos PPM'}
    )

    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })
    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, 'core/chart.html', context)
