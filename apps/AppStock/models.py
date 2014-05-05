__author__ = 'vitalijlogvinenko'
from django.db import models

#strategy list
class Strategies(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    identifer = models.CharField(max_length=100, unique=True, db_index=True)
    class Meta:
        db_table = "Strategies"

#category list
class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True)
    TableName = models.CharField(max_length=200)
    Strategies = models.ManyToManyField(Strategies)

    class Meta:
        db_table = "Categories"

#name of ticker list
class Ticker(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Categories, db_index=True)
    last_update = models.DateTimeField()

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

#quotes for tickers in category World Index
class Quotes_index(models.Model):
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
        db_table = "Quotes_index"
        unique_together = ("ticker", "per", "date", "time")

#ticker name and id from finam site
class finam_tickers(models.Model):
    ticker = models.ForeignKey(Ticker, null=True, default=None)
    name = models.CharField(max_length=200)
    finam_id = models.IntegerField()

    class Meta:
        db_table = "finam_tickers"

#ticker name and id from mfd site
class mfd_tickers(models.Model):
    ticker = models.ForeignKey(Ticker, null=True, default=None)
    name = models.CharField(max_length=200, unique=True)
    mfd_id = models.IntegerField()

    class Meta:
        db_table = "mfd_tickers"

