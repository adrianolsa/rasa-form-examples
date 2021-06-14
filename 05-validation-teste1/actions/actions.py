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
        symbol_code = slot_value

        try:
            request = requests.get("http://localhost:8080/api/stocks/info/"+symbol_code)
            if request.status_code == 200:
                print ("Status 200")
            else:
                print("Status code: "+ request.status_code)
        except:
            print("An exception occurred")

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

        # recebe em cada variavel o valor preenchido no slot
        symbol_code = tracker.get_slot("symbol_code")
        symbol_type = tracker.get_slot("symbol_type")
        symbol_qtty = tracker.get_slot("symbol_qtty")

        # cria um objeto com os atributos
        order = Order(symbol_code, symbol_type, symbol_qtty)
        # imprimi o objeto somente para teste
        order.printOrder()

        # converte o objeto "order" em json
        jsonStr = json.dumps(order.__dict__)
        # imprimi somente para teste
        print(jsonStr)

        # faz requisição para o sistema
        # url = http://localhost:8080/api/order/bot
        # parametro (json) = jsonStr
        # headers (opcional) = cabeçalho indicando que o parametro enviado no método POST é um json
        response = requests.post("http://localhost:8080/api/order/bot", data=jsonStr, headers=headers)

        # responde no chat do rasa o conteúdo devolvido pelo sistema
        dispatcher.utter_message(text=f"{response.content}!")

        return []