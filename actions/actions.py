# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import requests
import time
import datetime
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker

###### Global variables ######
DATE_FORMAT = '%Y年%m月%d日'
TIME_FORMAT = '%H时%M分%S秒'
weekdayToStr = ['一', '二', '三', '四', '五', '六', '日']


#############################
# 时间查询
class ActionTimeQuery(Action):
    def name(self) -> Text:
        return "action_time_query"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        current_time = "现在的时间是：{}".format(time.strftime(TIME_FORMAT, time.localtime()))
        dispatcher.utter_message(text=current_time)

        return []

# 日期查询
class ActionDateQuery(Action):
    def name(self) -> Text:
        return "action_date_query"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        date_item = tracker.get_slot('date')
        offset = 0

        if "明天" is date_item:
            offset = 1
        elif "昨天" is date_item:
            offset = -1

        date_str = '{}是：{} 星期{}'.format(date_item, time.strftime('%Y年%m月%d日',
                                                                 time.localtime()),
                                        weekdayToStr[datetime.datetime.now().weekday()])
        dispatcher.utter_message(date_str)

        return []

# 营业时间查询
class ActionServiceTimeQuery(Action):
    def name(self):
        return "action_service_time_query"

    def run(self, dispatcher, tracker, domain):
        facilities = tracker.get_slot('facilities')
        response = opening_hours(facilities)
        dispatcher.utter_message(response)
        return []

def opening_hours(facilities):
    if facilities == "餐厅":
        response="早餐供应时间为早上7：00-10：30"
        return response
    if facilities == "商店":
        response="早餐营业时间为早上6：00-凌晨2：00"
        return response
    if facilities == "健身房":
        response="健身房开放时间为早上8：00-晚上21：30"
        return response
    if facilities == "游泳池":
        response="游泳池开放时间为早上8：00-晚上16：30"
        return response

# 地点查询
class ActionLocationQuery(Action):
    def name(self):
        return "action_location_query"

    def run(self, dispatcher, tracker, domain):
        facilities = tracker.get_slot('facilities')
        response = direction(facilities)
        dispatcher.utter_message(response)
        return []

def direction(facilities):
    if facilities == "餐厅":
        response="餐厅在一楼大堂的正前方，往前稍走几步就到了。让我带你去吧"
        return response
    if facilities == "商店":
        response="商店在酒店的对面，离开酒店后往前直行20m就到了。让我带你去吧"
        return response
    if facilities == "健身房":
        response="健身房在酒店的二楼，乘坐电梯到达二楼后右转，沿着走廊直行至尽头就到了。让我带你去吧"
        return response
    if facilities == "游泳池":
        response="游泳池在酒店的后方，离开酒店大门后左转20米到第一个路口右转就到了。让我带你去吧"
        return response



############ default action ############
class SelfActionDefaultFallback(Action):
    def name(self):
        return "self_action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get('text')
        message = get_response(text)

        if message['code'] == 100000:
            dispatcher.utter_message("{}".format(message['text']))
        else:
            dispatcher.utter_template('utter_default', tracker)

        return []


def get_response(msg):
    key = '557cb44c862a415aaf738f0cc30c5be1'
    api = 'http://www.tuling123.com/openapi/api?key={}&info={}'.format(
        key, msg)
    return requests.get(api).json()