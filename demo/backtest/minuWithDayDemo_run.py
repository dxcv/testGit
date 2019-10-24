# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 16:54:50 2016
日线和分钟线混合回测的例子，即本来使用5分钟线进行测试，但是中间还应用日线的各种指标，比如突破NN 日均线等
@author: msi
"""

import sys

sys.path.append("..")

from datetime import datetime, timedelta

from pyalgotrade import strategy, bar
from pyalgotrade.technical import ma


class ENE_backtest(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        # 自定义日线级别dataseries
        self.__instrument = instrument
        self.__feed = feed
        self.setUseAdjustedValues(False)
        self.__position = None
        self.__ENE = None

        self.__feed_day = self.resampleBarFeed(frequency=bar.Frequency.DAY, callback=self.resample_callback)

        self.__MA3 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 3, 5)
        self.__MA5 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 5, 5)
        self.__MA8 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 8, 5)
        self.__MA10 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 10, 5)
        self.__MA12 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 12, 5)
        self.__MA15 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 15, 5)

        self.__MA30 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 30, 5)
        self.__MA35 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 35, 5)
        self.__MA40 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 40, 5)
        self.__MA45 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 45, 5)
        self.__MA50 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 50, 5)
        self.__MA60 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 60, 5)

        self.__EMA12 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 12, 5)
        self.__EMA50 = ma.EMA(self.__feed_day[instrument].getCloseDataSeries(), 50, 5)

        ##############各种信号量########
        self.initState = False  # 开头的几个过滤掉
        self.eneUpMode = False  # ENE 日线向下
        self.buyType = None  # 买入的类型，“UP”是上升趋势中轨买入，‘DOWN’是下降趋势下轨买入
        self.buyWaitSignal = False  # 买入等待信号
        self.sellWaitSignal = False  # 卖出等待信号
        self.holdDay = datetime.min  # 持有的日期

        self.sellinfo = ''
        self.buyPrice = 0.0

        self.min_ma5 = ma.SMA(self.__feed[instrument].getCloseDataSeries(), 5)  # 5分线5均
        self.min_ma10 = ma.SMA(self.__feed[instrument].getCloseDataSeries(), 10)  # 5分线5均
        self.min_ma20 = ma.SMA(self.__feed[instrument].getCloseDataSeries(), 20)  # 5分线5均
        self.min_ma30 = ma.SMA(self.__feed[instrument].getCloseDataSeries(), 30)  # 5分线5均
        self.min_ma60 = ma.SMA(self.__feed[instrument].getCloseDataSeries(), 60)  # 5分线5均
        self.min_ma120 = ma.SMA(self.__feed[instrument].getCloseDataSeries(), 120)  # 5分线5均


    def resample_callback(self, bars):

        #####################bars为pyalgotrade.bar.Bars，self.getFeed()[self.__instrument]为 <class 'pyalgotrade.dataseries.bards.BarDataSeries'>################
        #####bars = self.getFeed()[self.__instrument]   #若使用这个的话调用的是分钟线，或者需要重写一个Dataserie   
        #####closeSeries = bars.getCloseDataSeries()    
        # print "Resampled", bars.getDateTime(), bars[self.__instrument].getClose()  #另一套可用

        # print "日線",bars.getDateTime(),self.__MA10[-1],self.__MA11[-1]     #当分钟线走到 16号的时候，其ma10[-1]是15号的，也就是日线仍走到15号，但其15号的数据日线收盘价等数据全都有
        # self.eneLastData =
        if 1 > 2:
            print(type(bars), type(self.getFeed()[self.__instrument]))

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.buyPrice = execInfo.getPrice()
        self.info("BUY at ￥%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        sellPrice = execInfo.getPrice()
        self.info(
            "SELL at ￥%.2f%s 收益%.2f" % (execInfo.getPrice(), self.sellinfo, (sellPrice / self.buyPrice - 1) * 100))
        self.buyPrice = 0.0
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

        ##检查分钟均线状况

    def checkMinCondition(self):
        if self.min_ma5[-1] > self.min_ma10[-1] > self.min_ma20[-1] > self.min_ma30[-1] > self.min_ma60[-1]:  # 多头排列
            return 'UP'
        if self.min_ma5[-1] < self.min_ma10[-1] < self.min_ma20[-1] < self.min_ma30[-1] < self.min_ma60[-1]:  # 空头排列
            return 'DOWN'

        return 'UN_FLUNE'  # 多空不明

    ##检查ENE轨道状况   
    def checkENECondition(self):
        minShort = min(self.__MA3[-1], self.__MA5[-1], self.__MA8[-1], self.__MA10[-1], self.__MA12[-1],
                       self.__MA15[-1])
        maxLong = max(self.__MA30[-1], self.__MA35[-1], self.__MA40[-1], self.__MA45[-1], self.__MA50[-1],
                      self.__MA60[-1])

        if minShort > maxLong and all([self.__EMA12[x] > self.__EMA50[x] for x in range(-1,-6,-1)]):
            # for i in range(5):
            #     print(self.__EMA12[i],self.__EMA50[i])
            eneSignal = 'UP'
        else:
            eneSignal = 'DOWN'
        return eneSignal

    def onBars(self, bars):

        if self.initState is False:  # 如果MA均线有数值了才开始计算
            if self.__MA60.__len__() < 1:
                return
            else:
                if self.__MA60[-1] is None:
                    return
                else:
                    self.initState = True

        if (bars.getDateTime() - self.holdDay) < timedelta(days=1):  # 持有期大于一天
            return

        ma = (self.__MA10[-1] * 10.0 + bars[self.__instrument].getOpen()) / 11.0
        self.__UPPER = float(
            1 + 10.0 / 100) * ma  ##############当分钟线走到第二天的时候，日线仍走到前一天self.__feed_day[self.__instrument].getCloseDataSeries()[-1]仍为前一天的
        self.__LOWER = float(1 - 9.0 / 100) * ma
        self.__ENE = (self.__UPPER + self.__LOWER) / 2

        price = bars[self.__instrument].getOpen()
        # print "分鐘線",bars.getDateTime()
        buySignal = False
        sellSignal = False

        if self.__position is None or not self.__position.isOpen() and self.buyWaitSignal is False:  # 未持有,未下穿过
            if self.checkENECondition() == 'UP':  # 上升通道
                if price > self.__EMA50[-1]:
                    return
                else:  # 当前价格在中轨之下，可以尝试买入
                    self.buyWaitSignal = True
                    self.buyType = 'UP'
            else:  # 下降通道
                return

        if self.buyWaitSignal is True:  # 出现一次下穿情况，直接等待均线排列好买入
            # if self.checkMinCondition() is not 'UP':  # 添加日线死叉条件不买入
            #     return
            # else:
                buySignal = True

        if buySignal is True and self.__position == None:  # 买入操作
            shares = 100 * (int(self.getBroker().getCash() * 0.7 / bars[self.__instrument].getPrice()) / 100)
            self.__position = self.enterLong(self.__instrument, shares, True)
            self.buyWaitSignal = False
            self.holdDay = bars.getDateTime()
            return

        if not self.__position.exitActive() and self.sellWaitSignal is False:
            if self.buyType == 'UP':  # 上升趋势买入的
                # if price < self.__LOWER:  # 下穿下轨（大跌趋势）
                #     self.sellWaitSignal = True
                #     self.sellinfo = "上升趋势买入,跌至下轨"
                # elif price >= self.__UPPER:  # 上穿上轨准备卖出
                #     self.sellWaitSignal = True
                #     self.sellinfo = "上升趋势买入,上穿上轨"
                # el
                if price >= self.buyPrice * 1.15:
                    self.sellWaitSignal = True
                    self.sellinfo = "上升趋势买入,15%止盈"
                elif price < self.buyPrice * 0.8:
                    self.sellWaitSignal = True
                    self.sellinfo = "上升趋势买入,20%止损"
                else:  # 上轨和下之间不予理睬
                    return

        if self.sellWaitSignal is True:  # 出现一次下穿情况，直接等待均线排列好买入
            sellSignal = True

        if sellSignal is True:  # 卖出操作
            self.__position.exitMarket()
            self.sellWaitSignal = False
            self.buyType = None
