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
from plotly.graph_objs import Scatter, Scatterpolar, Layout
from django.core import serializers

# Create your views here.
def playerData(request):
    PitcherList = list(Pitch.objects.values_list('pitcher').distinct())
    PitcherList = [i[0] for i in PitcherList]
    template = loader.get_template('home.html')
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
    df = pd.DataFrame(list(Pitch.objects.filter(pitcher=name).values()))
    plot_div = plot({"data":plotLoc(df), 
        'layout': Layout(title=f"{name}'s Pitch Location Distribution", xaxis=dict(title='Lateral Pitch Location (ft)', range=[-4,4]), yaxis=dict(title='Pitch Height (ft)', range=[-1,6]), legend=dict(title="Pitch Types"))}, 
        output_type='div')
    spin_plot = plot({"data": plotSpin(df), 
        'layout':Layout(title=f"{name}'s Pitch Spin Chart", legend=dict(title="Pitch Types"))}, output_type='div')
    mov_plot = plot({'data': plotMov(df),
        'layout':Layout(title=f"{name}'s Pitch Movement Chart", xaxis=dict(title='Horizontal Pitch Movement (ft)', range=[-30,30]), yaxis=dict(title='Induced Vertical Break (ft)', range=[-30,30]), legend=dict(title="Pitch Types"))}, output_type='div')
    rel_plot = plot({'data': plotRel(df),
        'layout': Layout(title=f"{name}'s Pitch Release Chart", xaxis=dict(title='Horizontal Release (ft)', range=[-4,4]), yaxis=dict(title='Release Height (ft)', range=[0,8]), legend=dict(title="Pitch Types"))}, output_type='div')
    hit_plot = plot({"data": plotHit(df), 
        'layout': Layout(polar=dict(angularaxis=dict(tickmode="array", tickvals=[45,60,75,90,105,120,135], ticktext=['Right Field Foul Line','','','center field','','','Left Field Foul Line']), radialaxis=dict(tickmode="array", tickvals=[0,90,150,300,400,500], range=[0,500], ticktext=['0', '90','150','300','400','500'])), title=f"{name}'s In Play Chart",legend=dict(title="Results"))}, output_type='div')
    infieldHit_plot = plot({"data": plotInfieldHit(df), 
        'layout': Layout(polar=dict(angularaxis=dict(tickmode="array", tickvals=[45,60,75,90,105,120,135], ticktext=['Right Field Foul Line','','','second base','','','Left Field Foul Line']), radialaxis=dict(tickmode="array", tickvals=[0, 60, 90, 120], range=[0,120], ticktext=['0', '60', '90', '120'])), title=f"{name}'s Infield In Play Chart",legend=dict(title="Results"))}, output_type='div')
    return render(request, 'playerDisplay.html', context={'plot_div': plot_div, 'spin_plot': spin_plot, 'mov_plot': mov_plot, 'rel_plot': rel_plot, 'hit_plot': hit_plot, 'infield_hit': infieldHit_plot})

def plotSpin(df):
    df['spinDegree'] = (270 - df['spinDegree'])
    graphList = [Scatterpolar(
        r=df[df['pitchType'] == pitches]['spinRate'], 
        theta=df[df['pitchType'] == pitches]["spinDegree"],
        hovertemplate= [f"Velocity: {df[df['pitchType'] == pitches].iloc[i]['velocity']} <br>Vertical Movement: {df[df['pitchType'] == pitches].iloc[i]['inducedVert']} </br> Horizontal Movement: {df[df['pitchType'] == pitches].iloc[i]['horzBreak']}" for i in range(len(df[df['pitchType'] == pitches]['pitcher']))],
        mode='markers', 
        name=pitches, 
        opacity=0.8,)
        for pitches in df['pitchType'].unique()]
    return graphList

def plotLoc(df):
    graphList = [Scatter(
        x=df[df['pitchType'] == pitches]['plateLocSide'], 
        y=df[df['pitchType'] == pitches]['plateLocHeight'], 
        hovertemplate= [f"Velocity: {df[df['pitchType'] == pitches].iloc[i]['velocity']} <br>Spin: {df[df['pitchType'] == pitches].iloc[i]['spinRate']} </br> Outcome: {df[df['pitchType'] == pitches].iloc[i]['Outcome']}" for i in range(len(df[df['pitchType'] == pitches]['pitcher']))], 
        mode='markers', 
        name=pitches, 
        opacity=0.8,)
        for pitches in df['pitchType'].unique()]
    graphList.insert(0, Scatter(x=[-0.8, 0.8, 0.8, -0.8, -0.8], y=[1.7, 1.7, 3.4, 3.4, 1.7], hoverinfo='skip', name='Strikezone', opacity=0.3))
    return graphList

def plotMov(df):
    graphList = [Scatter(
        x=df[df['pitchType'] == pitches]['horzBreak'], 
        y=df[df['pitchType'] == pitches]['inducedVert'], 
        hovertemplate= [f"Pitch Type: {df[df['pitchType'] == pitches].iloc[i]['pitchType']} <br>Velocity: {df[df['pitchType'] == pitches].iloc[i]['velocity']} </br> Outcome: {df[df['pitchType'] == pitches].iloc[i]['Outcome']}" for i in range(len(df[df['pitchType'] == pitches]['pitcher']))], 
        mode='markers', 
        name=pitches, 
        opacity=0.8,)
        for pitches in df['pitchType'].unique()]
    return graphList

def plotRel(df):
    graphList = [Scatter(
        x=df[df['pitchType'] == pitches]['horzRelease'], 
        y=df[df['pitchType'] == pitches]['vertRelease'], 
        hovertemplate= [f"Pitch Type: {df[df['pitchType'] == pitches].iloc[i]['pitchType']} <br>Velocity: {df[df['pitchType'] == pitches].iloc[i]['velocity']} </br> Outcome: {df[df['pitchType'] == pitches].iloc[i]['Outcome']}" for i in range(len(df[df['pitchType'] == pitches]['pitcher']))], 
        mode='markers', 
        name=pitches, 
        opacity=0.8,)
        for pitches in df['pitchType'].unique()]
    return graphList

def plotHit(df):
    df = df[df['Outcome'] == 'InPlay']
    df['LaunchDirect'] += 90
    graphList = [Scatterpolar(
        r=df[df['inPlayResult'] == result]['LaunchDistance'], 
        theta=df[df['inPlayResult'] == result]["LaunchDirect"],
        hovertemplate= [f"Result: {df[df['inPlayResult'] == result].iloc[i]['inPlayResult']} <br>Batted Ball Type: {df[df['inPlayResult'] == result].iloc[i]['battedBallType']}</br>Exit Velocity: {df[df['inPlayResult'] == result].iloc[i]['ExitVelo']} <br>Distance: {df[df['inPlayResult'] == result].iloc[i]['LaunchDistance']} </br>Pitch Type: {df[df['inPlayResult'] == result].iloc[i]['pitchType']}" for i in range(len(df[df['inPlayResult'] == result]['pitcher']))],
        mode='markers', 
        name=result, 
        opacity=0.8,
        )
        for result in df['inPlayResult'].unique()]
    return graphList

def plotInfieldHit(df):
    df = df[df['Outcome'] == 'InPlay']
    df['LaunchDirect'] += 90
    graphList = [Scatterpolar(
        r=df[df['inPlayResult'] == result]['LaunchDistance'], 
        theta=df[df['inPlayResult'] == result]["LaunchDirect"],
        hovertemplate= [f"Result: {df[df['inPlayResult'] == result].iloc[i]['inPlayResult']} <br>Batted Ball Type: {df[df['inPlayResult'] == result].iloc[i]['battedBallType']}</br>Exit Velocity: {df[df['inPlayResult'] == result].iloc[i]['ExitVelo']} <br>Distance: {df[df['inPlayResult'] == result].iloc[i]['LaunchDistance']} </br>Pitch Type: {df[df['inPlayResult'] == result].iloc[i]['pitchType']}" for i in range(len(df[df['inPlayResult'] == result]['pitcher']))],
        mode='markers', 
        name=result, 
        opacity=0.8,
        )
        for result in df['inPlayResult'].unique()]
    return graphList