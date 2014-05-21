# coding: utf-8


__author__ = 'vitalijlogvinenko'
import json
from django.core import serializers
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.db.models import Max, Min, get_model

from django.shortcuts import render
from .models import Quotes, Category, Strategy, System
import datetime
from AppStockLib import *
from MyStrategy import *
from AppStockSystem import *

def index(request, cat_id, page, template_name='index.html'):
    page_num = page
    cat_id = cat_id
    page_len = 50
    page_start = (int(page_num) - 1)*page_len
    page_end = page_start + page_len
    now = datetime.datetime.now()
    #Получаем объект связанный с текущей категорией
    #cat_obj = Category.objects.get(id=cat_id)
    #quotes_obj = get_model("AppStock", cat_obj.TableName)
    category = Category.objects.all()
    strategies = Strategy.objects.all()
    tickers = list(Ticker.objects.filter(category_id=cat_id, used=True).order_by('name').values('id','name','last_update')[page_start:page_end])
    count_page = len(list(Ticker.objects.filter(category_id=cat_id, used=True).order_by('name').values('id','name','last_update')))/page_len + 1
    print(count_page)
    paginator = []
    i = 1
    while i<=count_page:
        paginator.append(i)
        i += 1

    ms = MyStrategy()
    ms.init(System)
    systems = System.objects.all()
    signals = None
    counter = page_start + 1
    for row_ticker in tickers:
        #print(row_ticker['name'])
        row_ticker['signals'] = {}
        row_ticker['counter'] = counter
        counter += 1
        for row_strat in systems:
            row_ticker['signals'][str(row_strat.identifer)]=[]

        #ticker_id = Ticker.objects.get(name=row_ticker['name'])
        list_ = Quotes.objects.filter(per='D',ticker_id=row_ticker['id'],date__gte='2012-01-01',date__lte=now.date()).order_by('date').values('close','date','low','per','hight')
        if(len(list_)>0):
            qs = ms.includeIndicators(list_)
            ar_per = []
            signals = ms.diverSignalAll(list(qs))
            if(len(signals)>0):
                if(signals[len(signals)-1]['signal']):
                    ar_per.append({'per':signals[len(signals)-1]['per'],'type':signals[len(signals)-1]['type'], 'date':signals[len(signals)-1]['date']})
                    signal_name = signals[len(signals)-1]['name']
                    row_ticker['signals'][signal_name] = ar_per
            ar_per2 = []
            signals = ms.PriceAtEmaSignal(list(qs))
            if(len(signals)>0):
                if(signals[len(signals)-1]['signal']):
                    ar_per2.append({'per':signals[len(signals)-1]['per'],'type':signals[len(signals)-1]['type'], 'date':signals[len(signals)-1]['date']})
                    signal_name = signals[len(signals)-1]['name']
                    row_ticker['signals'][signal_name] = ar_per2

        list_ = Quotes.objects.filter(per='W',ticker_id=row_ticker['id'],date__gte='2004-01-01',date__lte=now.date()).order_by('date').values('close','date','low','per','hight')
        if(len(list_)>0):
            qs = ms.includeIndicators(list_)
            signals = ms.diverSignalAll(list(qs))
            if(len(signals)>0):
                if(signals[len(signals)-1]['signal']):
                    ar_per.append({'per':signals[len(signals)-1]['per'],'type':signals[len(signals)-1]['type'], 'date':signals[len(signals)-1]['date']})
                    signal_name = signals[len(signals)-1]['name']
                    row_ticker['signals'][signal_name] = ar_per
            #ar_per = []
            signals = ms.PriceAtEmaSignal(list(qs))
            if(len(signals)>0):
                if(signals[len(signals)-1]['signal']):
                    ar_per2.append({'per':signals[len(signals)-1]['per'],'type':signals[len(signals)-1]['type'], 'date':signals[len(signals)-1]['date']})
                    signal_name = signals[len(signals)-1]['name']
                    row_ticker['signals'][signal_name] = ar_per2

        list_ = Quotes.objects.filter(per='M',ticker_id=row_ticker['id'],date__gte='2004-01-01',date__lte=now.date()).order_by('date').values('close','date','low','per','hight')
        if(len(list_)>0):
            qs = ms.includeIndicators(list_)
            signals = ms.diverSignalAll(list(qs))
            if(len(signals)>0):
                if(signals[len(signals)-1]['signal']):
                    ar_per.append({'per':signals[len(signals)-1]['per'],'type':signals[len(signals)-1]['type'], 'date':signals[len(signals)-1]['date']})
                    signal_name = signals[len(signals)-1]['name']
                    row_ticker['signals'][signal_name] = ar_per
            #ar_per = []
            signals = ms.PriceAtEmaSignal(list(qs))
            if(len(signals)>0):
                if(signals[len(signals)-1]['signal']):
                    ar_per2.append({'per':signals[len(signals)-1]['per'],'type':signals[len(signals)-1]['type'], 'date':signals[len(signals)-1]['date']})
                    signal_name = signals[len(signals)-1]['name']
                    row_ticker['signals'][signal_name] = ar_per2

            #Выделяем строку при соблюдении правила
            signal_ema = row_ticker['signals']['PriceAtEma']
            if(signal_ema[2]['type'] != signal_ema[1]['type'] or signal_ema[1]['type']!=signal_ema[0]['type']):
                row_ticker['signals']['select_row'] = True
            else:
                row_ticker['signals']['select_row'] = False
            #print(row_ticker['signals'])
        #for a in signals:
        #    print(a)
    print(tickers)
    ctx = {
        'cat_id' : int(cat_id),
        'page' : page_num,
        'now': now,
        'category': category,
        'tickers': tickers,
        'paginator': paginator,
        'strategies': strategies,
        'systems' : systems
    }
    return render(request, template_name, ctx)

def upload(request, cat_id, per):
    #Получаем объект связанный с текущей категорией
    cat_obj = Category.objects.get(id=cat_id)
    #quotes_obj = get_model("AppStock", cat_obj.TableName)
    loadFromFinam(Quotes, cat_id, per)

    # Tickers = list(mfd_tickers.objects.exclude(ticker_id__isnull=True).values('mfd_id'))
    # #Tickers = [63, 59994, 62792, 59998, 59817, 59992, 54116, 61157, 59993, 59995, 51987, 61775, 59186, 69, 60508, 46778, 33231, 56693, 29363, 17125, 49748, 51821, 50793, 9834, 39233, 50794, 50994, 32144, 37399, 56252, 44598, 17799, 73, 74, 144, 41369, 157, 168, 183, 204, 28600, 28601, 41228, 41229, 232, 190, 41807, 246, 273, 287, 288, 316, 317, 258, 264, 269, 270, 42053, 42605, 346, 330, 38822, 51850, 336, 342, 396, 383, 44517, 415, 416, 394, 41824, 443, 445, 50968, 53333, 65447, 17107, 460, 506, 64989, 555, 511, 29055, 29058, 571, 49900, 589, 602, 598, 599, 607, 608, 542, 612, 614, 615, 28676, 41967, 14995, 647, 64410, 650, 648, 629, 632, 666, 832, 672, 49747, 855, 856, 61457, 9060, 35831, 716, 880, 51353, 46788, 27847, 891, 9441, 726, 730, 742, 747, 778, 777, 779, 787, 815, 826, 39588, 944, 945, 909, 910, 913, 915, 948, 35798, 967, 975, 54550, 993, 41402, 1273, 1272, 1019, 37247, 36267, 48769, 49749, 60067, 1122, 35928, 28926, 60491, 46012, 53461, 36848, 36847, 1240, 1281, 17327, 58189, 28606, 1353, 1359, 35301, 58324, 58325, 33481, 1372, 1334, 1373, 54102, 54103, 1383, 1384, 1385, 1386, 33198, 63600, 1389, 30298, 57601, 1402, 28561, 41494, 41339, 41340, 1463, 1464, 1466, 1476, 39756, 1418, 1498, 1503, 1506, 30018, 1437, 1529, 1542, 1543, 41820, 1613, 1614, 1615, 1549, 1566, 1567, 1568, 1576, 1579, 1587, 1626, 40778, 32421, 1593, 1639, 35278, 31759, 1658, 1665, 1683, 41980, 1706, 1718, 37859, 1712, 1738, 1764, 1750, 1754, 37883, 1786, 1805, 1798, 44777, 1820, 1826, 1827, 41823]
    # #Tickers = [{'mfd_id':21018}]
    # newTickers = {}
    # i = 0
    # arLength = len(Tickers)/30
    # ost = len(Tickers) - arLength*30
    # if(ost>0):
    #     arLength += 1
    # while i<arLength:
    #     newTickers[i] = list(item['mfd_id'] for item in Tickers[i*30:i*30+30])
    #     i += 1
    # i = 0
    # now = datetime.datetime.today()
    # week = now - datetime.timedelta(weeks=1)
    # now = datetime.datetime.strftime(now, '%d.%m.%Y')
    # week = datetime.datetime.strftime(week,'%d.%m.%Y')
    # print(now + " ; " + week)
    # while i<=len(newTickers)-1:
    #     print(newTickers[i])
    #     #res = up.uploadFromFinam(Quotes, 1, newTickers[i], '01.01.2014',None,"D")
    #     #res = up.uploadFromMFD(Quotes, 1, newTickers[i], None, None, "D")
    #     #res = up.uploadFromMFD(Quotes, 1, newTickers[i], None, None, "W")
    #     #res = up.uploadFromMFD(Quotes, 1, newTickers[i], None, None, "M")
    #     #res = up.uploadFromMFD(Quotes, 1, newTickers[i], None, None, "H1")
    #     print("GOOD"+str(i))
    #     i += 1

    ctx = {
        'test': 'uppload',
    }
    #return render(request, template_name, ctx)
    return HttpResponse("Выгрузка завершена. <br><a href='../'>На главную</a>")

def parsing(request):
    up = AppStockUpload()
    #a = up.loadTickersFromHTML("../pars/pars.txt",finam_tickers)
    #Связываем id Tickers с id finam_tickers
    # t = Ticker.objects.filter(category=2)
    # for row in t:
    #     print(row.name)
    #     try:
    #         g = finam_tickers.objects.get(name=row.name)
    #         f = finam_tickers.objects.filter(name=row.name).update(id=g.id, ticker=row.id)
    #     except finam_tickers.DoesNotExist:
    #         f = None
    return HttpResponse("Парсировка финама. <br><a href='../'>На главную</a>")

#Функция для догрузки данных из финама
def loadFromFinam(obj, category_id, per):
    up = AppStockUpload()
    table_name = obj.__name__
    #Получаем данные по уже выгруженным котировкам
    tickers = obj.objects.raw('''
        WITH t AS(SELECT ticker_id,max(date) FROM "{table_name}" WHERE per='{per}' GROUP BY ticker_id)
        SELECT b.id, a.max, b.name, b.finam_id FROM t a
        INNER JOIN "Tickers" b ON a.ticker_id = b.id AND b.category_id={cat_id} AND b.finam_id IS NOT NULL
    '''.format(table_name=str(table_name),per=str(per),cat_id=category_id))
    tickers = list(tickers)
    #Если данные есть, то делаем догрузку начиная с последней даты котировки
    if(len(tickers)>0):
        for row in tickers:
            a = []
            date_from = row.max
            date_from = datetime.datetime.strftime(date_from, "%d.%m.%Y")
            print(date_from)
            a.append(row.finam_id)
            res = up.uploadFromFinam(obj, category_id, a, date_from, None, per)
    #иначе делаем полную выгрузку
    else:
        tickers = Ticker.objects.raw('''
          select a.* from "Tickers" a
          where category_id={cat_id}
        '''.format(cat_id=category_id))
        for row in tickers:
            a = []
            a.append(row.finam_id)
            print(row.finam_id)
            res = up.uploadFromFinam(obj, category_id, a, None, None, per)
    #Конец loadFromFinam

#Вьюха для демо режима
def demo(request, cat_id, page, template_name='demo.html'):
    page_num = page #номер страницы
    page_len = 50 #размер страницы
    page_start = (int(page_num) - 1)*page_len
    page_end = page_start + page_len
    now = datetime.datetime.now()
    category = Category.objects.all() #список категорий
    #Получаем все тикеры в текущей категории
    tickers = Ticker.objects.filter(category_id=cat_id, used=True).order_by('name').values('id','name','last_update')[page_start:page_end]
    tickers = list(tickers)
    #Получаем количество страниц
    count_page = len(list(Ticker.objects.filter(category_id=cat_id, used=True).order_by('name').values('id','name','last_update')))/page_len + 1
    #создаём пагинатор
    paginator = []
    i = 1
    while i<=count_page:
        paginator.append(i)
        i += 1

    #Получаем системы подключенные к стратегии Демо
    demoStrategy = Strategy.objects.filter(identifer='demo')
    demoSystems = demoStrategy[0].system.all()
    shSystems = AppStockSystem()

    counter = page_start + 1
    for rowTicker in tickers:
        rowTicker['signals'] = {}
        rowTicker['counter'] = counter
        counter += 1
        for rowDemoSystems in demoSystems:
            rowTicker['signals'][rowDemoSystems.identifer] = []
        #Получаем котировки по тикеру
        listQuotes = Quotes.objects.filter(per='D',ticker_id=rowTicker['id'],date__gte='2012-01-01',date__lte=now.date()).order_by('date').values('close','date','low','per','hight')
        if(len(listQuotes)>0):
            #Запускаем расчет по системе
            for rowDemoSystems in demoSystems:
                ar_per = []
                startSystem = getattr(shSystems, rowDemoSystems.identifer)
                systemSignal = startSystem(listQuotes, 'macd')
                if(len(systemSignal)>0):
                    lastElemSystemSignal = systemSignal[len(systemSignal)-1]
                    if(lastElemSystemSignal['signal']):
                        ar_per.append({'per':lastElemSystemSignal['per'],'type':lastElemSystemSignal['type'], 'date':lastElemSystemSignal['date']})
                        signal_name = lastElemSystemSignal['name']
                        rowTicker['signals'][signal_name] = ar_per
        else:
            print(u'Данные по тикеру '+rowTicker['name']+u' не получены')
        #print(rowTicker)
    ctx = {
        'cat_id' : int(cat_id),
        'page' : page_num,
        'now': now,
        'category': category,
        'tickers': tickers,
        'paginator': paginator,
        'systems' : demoSystems
    }
    print(request.META['REQUEST_METHOD'])
    if(request.META['REQUEST_METHOD']=='POST'):
        response_data = {}
        #     row_ticker['last_update'] = str(row_ticker['last_update'].strftime('%d.%m.%Y'))
        #     if(row_ticker[])
        tickers = serializeDateForList(tickers)
        print(tickers)
        response_data['tickers'] = tickers
        return HttpResponse(json.dumps(tickers), content_type="application/json")
    else:
        return render(request, template_name, ctx)

def serializeDateForList(list):
    _list = list
    for row in _list:
        serializeDateForDict(row)
    return _list

def serializeDateForDict(row):
    for key,value in row.items():
        print(row)
        if ( type(value) == datetime.datetime or type(value) == datetime.date ):
            row[key] = str(row[key].strftime('%d.%m.%Y'))
        if( type(value) == dict ):
            serializeDateForDict(row[key])
        if( type(value) == list):
            serializeDateForList(row[key])