import datetime as dt
import json         #para requisição http/json
import requests     #para requisição http


from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        return []


class ActionRandom(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_random"

    def run(self, dispatcher, tracker, domain):
#         with actions.tracing.extract_start_span(tracer, domain["headers"], self.name()):
            request = json.loads(requests.get("http://api.icndb.com/jokes/random").text)
            joke = request["value"][
                "joke"
            ]  # extract a joke from returned json response
            dispatcher.utter_message(joke)  # send the message back to the user
            return []

# class ActionReceiveName(Action):
#
#     def name(self) -> Text:
#         return "action_receive_name"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#             symbol = tracker.latest_message['text']
#             request = json.loads(requests.get("http://localhost:8080/api/stocks/info/"+{symbol}).text)
# #             joke = request["value"][
# #                 "joke"
# #             ]  # extract a joke from returned json response
#             print(request)
#             dispatcher.utter_message(request)  # send the message back to the user
#             return [SlotSet("name", symbol)]


class ActionReceiveName(Action):

    def name(self) -> Text:
        return "action_receive_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']
        print(text)
        dispatcher.utter_message(text=f"I'll remember your name {text}!")
        return [SlotSet("name", text)]



class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        if not name:
            dispatcher.utter_message(text="I don't know your name.")
        else:
            dispatcher.utter_message(text=f"Your name is {name}!")
        return []

class ActionSymbolInfo(Action):

    def name(self) -> Text:
        return "action_symbol_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symbol = tracker.latest_message['text']
        print(text)
        dispatcher.utter_message(text=f"I'll remember your name {symbol}!")
        return []
