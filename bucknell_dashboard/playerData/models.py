from django.db import models

# Create your models here.
class Pitch(models.Model):
    pitchNum = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    pitcher = models.CharField(max_length=50, blank=True, null=True)
    pitcherID = models.IntegerField(blank=True, null=True)
    pitcherHanded = models.CharField(max_length=50, blank=True, null=True)
    batter = models.CharField(max_length=50, blank=True, null=True)
    batterID = models.IntegerField(blank=True, null=True)
    batterHanded = models.CharField(max_length=50, blank=True, null=True)
    outs = models.IntegerField(blank=True, null=True)
    balls = models.IntegerField(blank=True, null=True)
    strikes = models.IntegerField(blank=True, null=True)
    pitchType = models.CharField(max_length=50, blank=True, null=True)
    Outcome = models.CharField(max_length=50, blank=True, null=True)
    battedBallType = models.CharField(max_length=50, blank=True, null=True)
    inPlayResult = models.CharField(max_length=50, blank=True, null=True)
    velocity = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    vertAngle = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    horzAngle = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    spinRate = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    spinDegree = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    vertRelease = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    horzRelease = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    extension = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    inducedVert = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    horzBreak = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    plateLocHeight = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    plateLocSide = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    VertApprAngle = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    HorzApproachAngle = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    ExitVelo = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    LaunchAngle = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    LaunchDirect = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    LaunchDistance = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    catcher = models.CharField(max_length=50, blank=True, null=True)
    
class File(models.Model):
    file = models.FileField(upload_to="playerData/excel")
    
    