# coding: utf-8
__author__ = 'vitalijlogvinenko'
from AppStockLib import *

class MyStrategy:

    def __init__(self):
        self.diverMACD = 'diverMACD'
        self.PriceAtEma = 'PriceAtEma'

    #Добавляем описание стратегий в модель где хранятся системы
    def init(self, objModel):
        objModel.objects.get_or_create(name="Дивергенция MACD", identifer=self.diverMACD, description="Дивергенция по MACD(12,26,9)")
        objModel.objects.get_or_create(name="Относительно EMA", identifer=self.PriceAtEma, description="Цена относительно EMA(150,200,360)")

    #Функция накладывает необходимые индикаторы на чистый график
    def includeIndicators(self, queryset):
        indicators = AppStockIndicators()
        res = indicators.EMA(queryset, 150, rounded=False, field='close', output='ema150')
        res = indicators.EMA(res, 200, rounded=False, field='close', output='ema200')
        res = indicators.EMA(res, 360, rounded=False, field='close', output='ema360')
        res = indicators.MACD(res, 12 , 26 , 9 , output='macd')
        return res
    #Конец includeIndicators
    #**

    #Функция для вычисления следующего значения индикаторов
    def includeIndicatorsNext(self, row, qs):
        qs = list(qs)
        indicators = AppStockIndicators()
        res = indicators.nextMACD(row[0], qs[len(qs)-1], 'close', 'macd')
        res = indicators.nextEMA(res, qs[len(qs)-1], 'close', 'ema150')
        res = indicators.nextEMA(res, qs[len(qs)-1], 'close', 'ema200')
        res = indicators.nextEMA(res, qs[len(qs)-1], 'close', 'ema360')
        row[0] = res
        res = qs + row
        return res
    #Конец includeIndicatorsNext
    #**


    #Поиск дивергенции. За расчет берется список цен
    #На выходе получаем массив вида: [{per:'D'}, type:'UP', signal:True, name:name_strategy}]
    def diverSignalAll(self, qs):
        i = 0
        min_low = qs[i]['low']
        x_macd = None #Значение macd
        x_price = None #значение цены
        ar_macd = []
        ar_diver = []
        is_diver = False
        while i<len(qs):
            #print(str(qs[i]['date']) + " = " + str(qs[i]['low']))
            if(qs[i]['low']<min_low):
                min_low = qs[i]['low']
            if(len(qs[i-3:i])!=0):
                x1 = qs[i]['macd']['signal']['ema']
                x = qs[i-1]['macd']['signal']['ema']
                x3 = qs[i-2]['macd']['signal']['ema']
                x4 = qs[i-3]['macd']['signal']['ema']
                #print(res[i]['macd']['signal']['ema'])
                if (x1>x and x<x3<x4):
                    if((x_price is not None and x_macd is not None) and ((x_price>min_low and x_macd<x) or ((len(ar_macd)>=3 and (min_low<ar_macd[len(ar_macd)-2]['low'] and min_low<x_price) and x>ar_macd[len(ar_macd)-2]['macd'])))):
                        #print("min_low = "+str(min_low)+" x_prixe = " + str(x_price)+" ar_macd[len(ar_macd)-2]['low'] = "+str(ar_macd[len(ar_macd)-2]['low']))
                        #print(" x = "+str(x)+" x_macd = "+str(x_macd)+" ar_macd[len(ar_macd)-2]['macd'] = " + str(ar_macd[len(ar_macd)-2]['macd']))
                        _qs = qs
                        _qs[i][self.diverMACD] = True
                        ar_diver.append({'per':_qs[i]['per'],'signal':_qs[i][self.diverMACD],'name':self.diverMACD, 'type':'up', 'date':_qs[i]['date']})
                    else:
                        if(len(ar_diver)>0):
                            ar_diver[len(ar_diver)-1]['signal'] = False
                    x_macd = qs[i-1]['macd']['signal']['ema']
                    x_price = min_low
                    ar_macd.append({'low':x_price,'macd':x_macd})
                    #print("Date = " + str(qs[i-1]['date']) + "; LOW = " + str(min_low) + "; MACD = " + str(x_macd))
                    min_low = qs[i]['low']
            i += 1
        return ar_diver
    #Конец функции diverSignalAll
    #**

    def PriceAtEmaSignal(self, qs):
        i = 0
        ar_signal = []
        while i<len(qs):
            ema150 = qs[i]['ema150']['ema']
            ema200 = qs[i]['ema200']['ema']
            ema360 = qs[i]['ema360']['ema']
            price_low = qs[i]['low']
            price_hight = qs[i]['hight']
            #print("date = "+ str(qs[i]['date']) + "low = "+str(price_low)+" hight = "+str(price_hight))
            emamax = max(ema150,ema200,ema360)
            emamin = min(ema150,ema200,ema360)
            #print("min = " + str(emamin) + " max = " + str(emamax))
            if(price_low > emamax):
                _qs = qs
                _qs[i][self.PriceAtEma] = True
                ar_signal.append({'per':_qs[i]['per'],'signal':_qs[i][self.PriceAtEma],'name':self.PriceAtEma, 'type':'up', 'date':_qs[i]['date']})
            elif (price_hight < emamin):
                _qs = qs
                _qs[i][self.PriceAtEma] = True
                ar_signal.append({'per':_qs[i]['per'],'signal':_qs[i][self.PriceAtEma],'name':self.PriceAtEma, 'type':'down', 'date':_qs[i]['date']})
            else:
                _qs = qs
                _qs[i][self.PriceAtEma] = True
                ar_signal.append({'per':_qs[i]['per'],'signal':_qs[i][self.PriceAtEma],'name':self.PriceAtEma, 'type':'in', 'date':_qs[i]['date']})
            i += 1

        return ar_signal



