from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.messages import constants as messages
import logging
from django.urls import reverse
import pandas as pd
from .models import *
import numpy
import os
from plotly.offline import plot
from plotly.graph_objs import Scatter
from django.core import serializers

# Create your views here.
def playerData(request):
    PitcherList = list(Pitch.objects.values_list('pitcher').distinct())
    PitcherList = [i[0] for i in PitcherList]
    print(PitcherList)
    template = loader.get_template('playerData.html')
    context = {
        'PitcherList': PitcherList,
    }
    return HttpResponse(template.render(context, request))

def upload_csv(request):
    data_to_display = None
    if request.method == 'POST':
        file = request.FILES['files']
        obj = File.objects.create(
            file=file
        )
        try:
            file.seek(0)
            path = file.file
            df = pd.read_csv(path)
            df = df.replace(numpy.nan, None)
            data_to_display = 'File Successfully Uploaded'
            for index, row in df.iterrows():
                objs = Pitch(
                    pitchNum = row['PitchNo'],
                    date = row['Date'],
                    pitcher = row['Pitcher'],
                    pitcherID = row['PitcherId'],
                    pitcherHanded = row['PitcherThrows'],
                    batter = row['Batter'],
                    batterID = row['BatterId'],
                    batterHanded = row['BatterSide'],
                    outs = row['Outs'],
                    balls = row['Balls'],
                    strikes = row['Strikes'],
                    pitchType = row['TaggedPitchType'],
                    Outcome = row['PitchCall'],
                    battedBallType = row['TaggedHitType'],
                    inPlayResult = row['PlayResult'],
                    velocity = row['RelSpeed'],
                    vertAngle = row['VertRelAngle'],
                    horzAngle = row['HorzRelAngle'],
                    spinRate = row['SpinRate'],
                    spinDegree = row['SpinAxis'],
                    vertRelease = row['RelHeight'],
                    horzRelease = row['RelSide'],
                    extension = row['Extension'],
                    inducedVert = row['InducedVertBreak'],
                    horzBreak = row['HorzBreak'],
                    plateLocHeight = row['PlateLocHeight'],
                    plateLocSide = row['PlateLocSide'],
                    VertApprAngle = row['VertApprAngle'],
                    HorzApproachAngle = row['HorzApprAngle'],
                    ExitVelo = row['ExitSpeed'],
                    LaunchAngle = row['Angle'],
                    LaunchDirect = row['Direction'],
                    LaunchDistance = row['Distance'],
                    catcher = row['Catcher']
                )

                objs.save()
        except KeyError:
            data_to_display = 'Please enter a .csv file using the Trackman format'
        except TypeError:
            data_to_display = 'Please enter a .csv file using the Trackman format'
        except UnicodeDecodeError:
            data_to_display = 'Please enter a .csv file using the Trackman format'
    return render(request, 'upload_csv.html', {'data_to_display': data_to_display})

def playerDisplay(request, name):
    x_data = list(Pitch.objects.filter(pitcher=name).values_list('velocity'))
    x_data = [i[0] for i in x_data]
    y_data = list(Pitch.objects.filter(pitcher=name).values_list('spinRate'))
    y_data = [i[0] for i in y_data]
    plot_div = plot([Scatter(x=x_data, y=y_data, mode='markers', name='test', opacity=0.8, marker_color='green')], output_type='div')
    return render(request, 'playerDisplay.html', context={'plot_div': plot_div})