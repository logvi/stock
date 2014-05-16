__author__ = 'vitalijlogvinenko'
from django.db import models

#strategy list
class Strategy(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    identifer = models.CharField(max_length=100, unique=True, db_index=True)
    class Meta:
        db_table = "Strategies"

#system list
class System(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    identifer = models.CharField(max_length=100, unique=True, db_index=True)
    strategy = models.ManyToManyField(Strategy)
    class Meta:
        db_table = "Systems"

#category list
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    TableName = models.CharField(max_length=200)
    Strategy = models.ManyToManyField(Strategy)
    class Meta:
        db_table = "Categories"

#name of ticker list
class Ticker(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, db_index=True)
    last_update = models.DateTimeField(null=True)
    finam_id = models.IntegerField(null=True)
    mfd_id = models.IntegerField(null=True)
    used = models.BooleanField(default=False)

    class Meta:
        db_table = "Tickers"

    #def __unicode__(self):
    #    return self.name

#quotes of tickers
class Quotes(models.Model):
    #category = models.ForeignKey(Categories, db_index=True)
    #ticker = models.CharField(max_length=200, db_index=True)
    ticker = models.ForeignKey(Ticker, db_index=True)
    per = models.CharField(max_length=3, db_index=True)
    date = models.DateField(db_index=True)
    time = models.TimeField(db_index=True)
    open = models.FloatField()
    hight = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    vol = models.BigIntegerField()
    date_create = models.DateTimeField()

    class Meta:
        db_table = "Quotes"
        unique_together = ("ticker", "per", "date", "time")

    # def __unicode__(self):
    #     return self.ticker



