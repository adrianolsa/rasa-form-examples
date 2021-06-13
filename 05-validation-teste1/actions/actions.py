from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


import json         #para requisição http/json
import requests     #para requisição http


from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker


class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_form"

    def validate_symbol_code(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `symbol_code` value."""

        # If the name is super short, it might be wrong.
        print(f"symbol code given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"symbol_code": None}
        else:
            return {"symbol_code": slot_value}

    def validate_symbol_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `symbol_type` value."""

        # If the name is super short, it might be wrong.
        print(f"symbol type given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"symbol_type": None}
        else:
            return {"symbol_type": slot_value}


class Order():

    def __init__(self, symbol, type, qtty):
        self.symbol = symbol
        self.type = type
        self.qtty = qtty

    def printOrder(self):
        print(f"Você quer fazer a {self.type} de {self.qtty} {self.symbol}")



class ActionCreateOrder(Action):

    def name(self) -> Text:
        return "action_create_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        symbol_code = tracker.get_slot("symbol_code")
        symbol_type = tracker.get_slot("symbol_type")
        symbol_qtty = tracker.get_slot("symbol_qtty")

        order = Order(symbol_code, symbol_type, symbol_qtty)
        order.printOrder()


        jsonStr = json.dumps(order.__dict__)
        print(jsonStr)

        response = requests.post("http://localhost:8080/api/order/bot", data=jsonStr, headers=headers)

        dispatcher.utter_message(text=f"{response.content}!")
        # if not name:
        #     dispatcher.utter_message(text="I don't know your name.")
        # else:
        #     dispatcher.utter_message(text=f"Your name is {name}!")
        return []