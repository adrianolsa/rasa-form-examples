from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


import json         #para requisição http/json
import requests     #para requisição http


from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker


class ValidateMilitarForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_militar_form"

    @staticmethod
    def patente_db() -> List[Text]:
        """Database of supported cuisines"""

        return ["cel","tc","maj","cap","ten","st","asp of","sgt","cb","sd"]


    def validate_militar_patente(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validar Formulário de Consulta de Dados do Militar"""

        value = slot_value

        # If the name is super short, it might be wrong.
        if value.lower() in self.patente_db():
            # validation succeeded, set the value of the "parametro" slot to value
            return {"militar_patente": value}
        else:
            dispatcher.utter_message(response="utter_wrong_patente")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"militar_patente": None}



class Militar():

    def __init__(self, patente, nome_guerra, obm):
        self.patente = patente
        self.nome_guerra = nome_guerra
        self.obm = obm

    def printAskRG(self):
        print(f"Você quer saber o RG do {self.patente} {self.nome_guerra} do {self.obm}?")



class ActionFindRG(Action):

    def name(self) -> Text:
        return "action_find_rg"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        # cria um objeto com os atributos
        militar = Militar(tracker.get_slot("militar_patente"), tracker.get_slot("militar_nome_guerra"), tracker.get_slot("militar_obm"))
        # imprimi o objeto somente para teste
        militar.printAskRG()

        # converte o objeto "militar" em json
        jsonStr = json.dumps(militar.__dict__)
        # imprimi somente para teste
        print(jsonStr)

        # faz requisição para o sistema
        # url = http://localhost:8080/api/bot
        # parametro (json) = jsonStr
        # headers (opcional) = cabeçalho indicando que o parametro enviado no método POST é um json
        response = requests.post("http://localhost:8082/bot/find/rg", data=jsonStr, headers=headers)

        # responde no chat do rasa o conteúdo devolvido pelo sistema
        dispatcher.utter_message(text=f"{response.content}!")

        return []