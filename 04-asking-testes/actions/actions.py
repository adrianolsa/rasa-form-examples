from typing import Dict, Text, List

from rasa_sdk import Tracker
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action



class OrderAction(Action):
    def name(self) -> Text:
        return "action_order"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        symbol_code = tracker.get_slot("symbol_code")
        symbol_type = tracker.get_slot("symbol_type")
        symbol_qtty = tracker.get_slot("symbol_qtty")
        if symbol_type == "":
            dispatcher.utter_message(text=f"Qual operação para {symbol_code}? Compra ou Venda?")
        elif symbol_qtty == "":
            dispatcher.utter_message(text=f"Qual a qtde de {symbol_type} para {symbol_code}?")
        return []
