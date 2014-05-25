# coding: utf-8


__author__ = 'vitalijlogvinenko'
import json
import inspect
from django.core import serializers
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.db.models import Max, Min, get_model
from django.contrib import auth
from django.shortcuts import redirect

from django.shortcuts import render
from .models import Quotes, Category, Strategy, System
import datetime
from AppStockLib import *
from MyStrategy import *
from AppStockSystem import *

def index(request, cat_id, page, template_name='index.html'):
    if(request.user.is_authenticated()):
        #auth.logout(request)
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
    else:
        #return HttpResponse("Нужно авторизоваться")
        return redirect('/login')

def upload(request, cat_id, per, template_name='upload.html'):
    if(request.user.is_authenticated()):
        if(request.META['REQUEST_METHOD']=='POST'):
            per = str(request.POST['per'])
            cat_id = int(request.POST['cat_id'])
            loadFromFinam(Quotes, cat_id, per)
            response_data = {}
            response_data['data'] = "Выгрузка завершена"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            category = Category.objects.all() #список категорий
            #cat_obj = Category.objects.get(id=cat_id)
            #loadFromFinam(Quotes, cat_id, per)
            ctx = {
                'category': category,

            }
            return render(request, template_name, ctx)
        #return HttpResponse("Выгрузка завершена. <br><a href='../'>На главную</a>")
    else:
        return redirect('/login')

def parsing(request):
    if(request.user.is_authenticated()):
        if(request.META['REQUEST_METHOD']=='POST'):
            parsString = request.POST['parsString']
            saveInDB = request.POST['saveInDB']
            catId = request.POST['catId']
            if(saveInDB == '0' or saveInDB == 'false'):
                saveInDB = False
            if(saveInDB == '1' or saveInDB == 'true'):
                saveInDB = True
            response_data = {}
            up = AppStockUpload()
            if(saveInDB):
                a = up.loadTickersFromHTML(parsString, Ticker, catId)
                response_data['data']='Операция завершена'
            else:
                text = up.getTickersFromHTML(parsString,'li a')
                response_data['data'] = text
            return HttpResponse(json.dumps(response_data), content_type="application/json")
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
        #return HttpResponse("Парсировка финама. <br><a href='../'>На главную</a>")
    else:
        return redirect('/login')

#Функция для догрузки данных из финама
def loadFromFinam(obj, category_id, per):
    up = AppStockUpload()
    table_name = obj.__name__
    #Получаем данные по уже выгруженным котировкам
    tickers = obj.objects.raw('''
        WITH tt AS (
            WITH t AS(SELECT ticker_id,max(date) FROM "Quotes" WHERE per='{per}' GROUP BY ticker_id)
                SELECT b.id, a.max, b.name, b.finam_id FROM t a
                INNER JOIN "Tickers" b ON a.ticker_id = b.id AND b.category_id={cat_id} AND b.finam_id IS NOT NULL and used=True
                )
        SELECT a.id, tt.max, a.name, a.finam_id FROM "Tickers" a
        LEFT JOIN tt on tt.id = a.id
        WHERE a.category_id={cat_id} and a.used=True and a.finam_id is not null
    '''.format(table_name=str(table_name),per=str(per),cat_id=category_id))
    tickers = list(tickers)
    #Если данные есть, то делаем догрузку начиная с последней даты котировки
    if(len(tickers)>0):
        for row in tickers:
            a = []
            date_from = row.max
            if(date_from is None):
                date_from = None
            else:
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
def demo(request, cat_id, template_name='demo.html'):
    now = datetime.datetime.now()
    category = Category.objects.all() #список категорий

    #Получаем системы подключенные к стратегии Демо
    demoStrategy = Strategy.objects.filter(identifer='demo')
    demoSystems = demoStrategy[0].system.all()

    ctx = {
        'cat_id' : int(cat_id),
        'now': now,
        'category': category,
        'systems': demoSystems
    }
    return render(request, template_name, ctx)

#Возвращает данные для таблицы
def getTableData(request, cat_id, page, template_name='demo.html'):
    if(request.method == "POST"):
        page = int(request.POST['page'])
        cat_id = int(request.POST['cat_id'])
    page_len = 50 #размер страницы
    page_start = page
    page_end = page_start + page_len
    bPageEnd = False #Последняя страница
    now = datetime.datetime.now()
    category = Category.objects.all() #список категорий
    #Получаем все тикеры в текущей категории
    tickers = Ticker.objects.filter(category_id=cat_id, used=True).order_by('name').values('id','name','last_update')#[page_start:page_end]
    tickers = list(tickers)
    #Получаем количество страниц
    countTickers = len(list(Ticker.objects.filter(category_id=cat_id, used=True).order_by('name').values('id','name','last_update')))
    #Определяем последняя страница или нет
    if (page_end>=countTickers):
        bPageEnd = True
    count_page = countTickers/page_len + 1
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
        calculateSystem(rowTicker, 'D', '2012-01-01', now.date(), demoSystems)
        calculateSystem(rowTicker, 'W', '2004-01-01', now.date(), demoSystems)
        calculateSystem(rowTicker, 'M', '2004-01-01', now.date(), demoSystems)
        #print(rowTicker)
    ctx = {
        'cat_id' : int(cat_id),
        'page' : page,
        'now': now,
        'category': category,
        'tickers': tickers,
        'paginator': paginator,
        'systems' : demoSystems
    }
    print(request.META['REQUEST_METHOD'])
    if(request.META['REQUEST_METHOD']=='POST'):
        response_data = {}
        #Пробую сортировку
        tickers.sort(key=sortBySignalDate, reverse=True)
        tickers = serializeDateInList(tickers)

        demoSystems = list(demoSystems)
        arSystems = []
        for row in demoSystems:
            a = {}
            row = row.__dict__
            print(type(row))
            for key,value in row.items():
                if(key != '_state'):
                    a[key] = value
            arSystems.append(a)
        response_data['systems'] = arSystems
        response_data['pageEnd'] = bPageEnd
        response_data['tickers'] = tickers#[page_start:page_end]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, template_name, ctx)

#Сортирует по дате сигнала
def sortBySignalDate(inputStr):
    #if(inputStr['signals']['diverMACD'][0].has_key('date')):
    if(len(inputStr['signals']['diverMACD'])>0):
        return inputStr['signals']['diverMACD'][0]['date']
    else:
        return datetime.date(2000,2,1)
    #return inputStr['last_update']

#Сериализует объекты даты в списке
def serializeDateInList(list):
    _list = list
    for row in _list:
        serializeDateInDict(row)
    return _list

#Сериализует объекты даты в словаре
def serializeDateInDict(row):
    for key,value in row.items():
        if ( type(value) == datetime.datetime or type(value) == datetime.date ):
            row[key] = str(row[key].strftime('%d.%m.%Y'))
        if( type(value) == dict ):
            serializeDateInDict(row[key])
        if( type(value) == list):
            serializeDateInList(row[key])

#Функция вычисления систем
# Кастыль!!! (В классе AppStockSystem в функции вычисления систем должны приходить параметры в едином виде и браться из базы)
def calculateSystem(ticker, per, dateStart, dateEnd, Systems):
    #Получаем котировки по тикеру
    shSystems = AppStockSystem()
    listQuotes = Quotes.objects.filter(per=per, ticker_id=ticker['id'], date__gte=dateStart, date__lte=dateEnd).order_by('date').values('close','date','low','per','hight')
    if(len(listQuotes)>0):
        #Запускаем расчет по системе
        for rowDemoSystems in Systems:
            ar_per = {}
            startSystem = getattr(shSystems, rowDemoSystems.identifer)
            #Кастыль!!! параметр 'macd' должен браться из хранилища, а не задаваться явно
            systemSignal = startSystem(listQuotes, 'macd')
            if(len(systemSignal)>0):
                lastElemSystemSignal = systemSignal[len(systemSignal)-1]
                if(lastElemSystemSignal['signal']):
                    ar_per = {'per':lastElemSystemSignal['per'],'type':lastElemSystemSignal['type'], 'date':lastElemSystemSignal['date']}
                    signal_name = lastElemSystemSignal['name']
                    ticker['signals'][signal_name].append(ar_per)
    else:
        print(u'Данные по тикеру '+ ticker['name'] +u' за период'+ per +u' не получены')