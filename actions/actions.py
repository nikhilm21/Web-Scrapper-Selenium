from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from datetime import datetime as dt

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionFeedback(Action):

    def name(self) -> Text:
        return "actions_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = tracker.latest_message.get('text')
        print(message)

        dispatcher.utter_message(text="Thank you for your feedback. Hope we have another chance to provide a better experience in the future.")

        return []

class ActionNewUser(FormAction):

    def name(self) -> Text:
        return "feedback_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["feed"]
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "feed": [self.from_text()]
        }

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        mobile = tracker.get_slot("feed")

        print(mobile)

        dispatcher.utter_message(template="utter_submit")

        return []

class ActionBookAppointment(Action):

    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            time = tracker.get_slot('time')
            time_object = dt.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")
            print(time_object)
            time_ = time_object.strftime("%I %p")
            date = time_object.strftime("%d %b %Y")
            message = f"Ok,Scheduling your call on {date} at {time_}\n If you want to change the date or time type reschedule with updated date and time"
        except:
            message = 'Didnt get you can you enter the time again?'

        dispatcher.utter_message(message)
        return []

class ActionFees(Action):

    def name(self) -> Text:
        return "action_fees_3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        fees = [1232] #this is where api call will be recieved
        dispatcher.utter_message(text=f"Based on the information you provided, your total fees would be ${fees[0]}.This includes the following fee breakdown:\n ${fees[0] - fees[0]*0.12} - Base Fee\n ${fees[0]*0.12} - Tax Fee")


        return []

class ActionRates(Action):

    def name(self) -> Text:
        return "action_rate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time = tracker.get_slot('number')
        rates = {15: [12], 20:[10],25:[8],30:[6]}

        if time == None:
            dispatcher.utter_message("Didnt get the rate could you try again")
        else:
            try:
                time = int(time)
                for i in rates:
                    if i == time:
                        fees = rates[time][0]
                        dispatcher.utter_message(text = f"Based on the information you provided, we can offer a {time} year fixed rate refinance for rate {fees}% with no lender no application fees and no points.")
                    elif i != time:
                        if time < 15:
                            dispatcher.utter_message(text = "Please enter timeline higher then 14")
                            break
                        elif time > 30:
                            dispatcher.utter_message(text = "Please enter timeline less then 31")
                            break

            except:
                dispatcher.utter_message(text = "Didnt get the rate could you try again")
                
        return []