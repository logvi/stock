# coding: utf-8
__author__ = 'vitalijlogvinenko'
from AppStockLib import *

class MyStrategy:

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



