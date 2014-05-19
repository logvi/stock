__author__ = 'vitalijlogvinenko'
# coding: utf-8
#Класс для торговых систем

from AppStockLib import *
from apps.AppStock.models import System

class AppStockSystem:
    # Храним идентификаторы всех систем
    def __init__(self):
        self.systems ={
            'diverMACD':{
                'identifer'  : 'diverMACD',
                'name'       : 'Дивергенция MACD',
                'description': 'Дивергенция по MACD(12,26,9)'
            },
            'PriceAtEma':{
                'identifer'  : 'PriceAtEma',
                'name'       : 'Относительно EMA',
                'description': 'Цена относительно EMA(150,200,360)'
            }
        }

    # Функция инициализирует все системы
    def init(self, arNames):
        if(len(arNames)>0):
            for el in arNames:
                print(self.systems[el])
                System.objects.get_or_create(identifer=self.systems[el]['identifer'],
                    defaults = {
                        'name': self.systems[el]['name'],
                        'description': self.systems[el]['description'],
                    }
                )

    # Поиск дивергенции. За расчет берется список цен
    # MACDField - поле в котором хранится значение индикатора MACD
    # На выходе получаем массив вида: [{per:'D'}, type:'UP', signal:True, name:name_strategy, date:'14.05.2014'}]
    def diverSignalAll(self, qs, MACDField):
        systemName = self.systems['diverMACD']['identifer']
        if(qs[0][MACDField] is None):
            print("Нет данных для MACD")
            return False
        else:
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
                            _qs[i][systemName] = True
                            ar_diver.append({'per':_qs[i]['per'],'signal':_qs[i][systemName],'name':systemName, 'type':'up', 'date':_qs[i]['date']})
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

    def test(self, a):
        print('FUCK' + str(a))

