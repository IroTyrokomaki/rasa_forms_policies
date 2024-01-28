import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from random import choice
from rasa_sdk.events import UserUtteranceReverted


class ActionProvideTrafficConditions(Action):
    def name(self) -> Text:
        return "action_provide_traffic_conditions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="action_provide_traffic_conditions")
        return []


class ActionProvideGasStation(Action):
    def name(self) -> Text:
        return "action_provide_gas_station"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="action_provide_gas_station")
        return []


class ActionGreetUser(Action):
    def name(self) -> Text:
        return "utter_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_greet")
        return []


class ActionSayGoodbye(Action):
    def name(self) -> Text:
        return "utter_goodbye"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_goodbye")
        return []


class ActionDeny(Action):
    def name(self) -> Text:
        return "utter_deny"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_deny")
        return []


class ActionAcknowledge(Action):
    def name(self) -> Text:
        return "utter_affirm"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_affirm")
        return []


class ActionThankYou(Action):
    def name(self) -> Text:
        return "utter_thank_you"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_thank_you")
        return []


class ActionIAmABot(Action):
    def name(self) -> Text:
        return "utter_iamabot"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("I am a bot, powered by Rasa.")
        return []


class ActionProvideWeather(Action):
    def name(self) -> Text:
        return "action_provide_weather"

    def convert_to_celsius(self, temperature_kelvin: float) -> float:
        # Convert temperature from Kelvin to Celsius
        return temperature_kelvin - 273.15


    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        location = tracker.get_slot("location")
        date = tracker.get_slot("date")

        # OpenWeatherMap API key
        api_key = 'dbc2d076ce1dab247b144d7963b9a582'

        # Construct the date parameter for the API request
        if date:
            date_parameter = f"&dt={date}"
        else:
            date_parameter = ""

        weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}{date_parameter}&appid={api_key}"
        response = requests.get(weather_api_url)

        # Check if the API request was successful
        if response.status_code == 200:
            weather_data = response.json()

            # Extract temperature and weather condition from the API response
            temperature_kelvin = weather_data["main"]["temp"]
            temperature_celsius = round(self.convert_to_celsius(temperature_kelvin), 1)
            weather_condition = weather_data["weather"][0]["description"]

            # Select a random response from the list
            response = choice(domain["responses"]["action_provide_weather"])

            # Replace placeholders in the response with actual values
            formatted_response = response["text"].format(
                temperature=temperature_celsius, weather_condition=weather_condition, location=location, date=date
            )

            # Informs the user if the API request fails
            dispatcher.utter_message(text=formatted_response)
        else:
            dispatcher.utter_message(
                text=f"Sorry, I couldn't retrieve the weather information for {location} on {date} at the moment. "
                     f"Please try again.")

        return []


class ActionAskDate(Action):
    def name(self) -> Text:
        return "action_ask_date"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Your action logic goes here
        dispatcher.utter_message(template="action_ask_date")
        return []


class ActionAskLocation(Action):
    def name(self) -> Text:
        return "action_ask_location"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Your action logic goes here
        dispatcher.utter_message(template="action_ask_location")
        return []


class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="action_default_fallback")

        return [UserUtteranceReverted()]
