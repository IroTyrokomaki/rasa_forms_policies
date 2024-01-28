# chatbot_scenarios_with_rasa_forms_and_policies README

A rasa form called "weather_form" has been built in the "ask_weather" scenario to collect data, namely for slot filling of location and date. The necessary slots are defined in the form, and they are mapped from matching entities (location and date). To handle the logic of retrieving weather data via the OpenWeatherMap API https://openweathermap.org/ and replying to the user, an action called "action_provide_weather" has also been developed (actions.py).

## How the Form is Used for Data Collection:
1.	The weather_form is activated when the user triggers the "ask_weather" intent.
2.	The form requests and fills the required slots (location and date) based on user input.
3.	The action "action_provide_weather" is then executed to fetch weather information using the provided location and date.
4.	The retrieved data is used to generate a response, and the conversation continues.

## Chatbot Response to Invalid Inputs or Irrelevant Chitchat

The chatbot includes a fallback action called "action_default_fallback" (actions.py) designed to handle invalid inputs. In cases where the user's input does not align with any pre-defined intent or does not add to the ongoing conversation context, the fallback action is activated. In particular, it sends a fallback message to the user, signaling that the input is not comprehended. This feature ensures a polite response when the chatbot encounters unexpected or irrelevant user inputs.

# Rasa Policies Experimentation
## RulePolicy

### Proper Functioning Example:
Consider a scenario where the user submits the weather inquiry with both location and date. The RulePolicy is effective in this scenario as it correctly activates the weather_form, captures the relevant slots (location and date), and then triggers the action_provide_weather once both slots are filled. The rule "Submit Weather form with location and date" is properly executed.

User Input
- User: What's the weather like in Athens tomorrow?

rules:
- rule: Submit Weather form with location and date
  condition:
    - active_loop: weather_form
    - slot_was_set:
        - requested_slot: location
        - requested_slot: date
          
  steps:
    - action: weather_form
    - active_loop: null
    - action: action_provide_weather

### Non-Functioning Example:
Consider a scenario where the user submits incomplete information, lacking the location. The RulePolicy may incorrectly respond to incomplete queries, demonstrating a scenario where it doesn't work optimally for handling missing slot values.

User Input
- User: What's the weather like tomorrow?

rules:
- rule: Submit Weather form with date
  condition:
    - active_loop: weather_form
    - slot_was_set:
        - requested_slot: date
          
  steps:
    - action: weather_form
    - active_loop: null
    - action: action_provide_weather

## MemoizationPolicy

### Proper Functioning Example:
Consider a user engaging in a weather-related conversation, providing their location and asking about the weather. If the user has previously interacted with the weather_form and mentioned the location, the MemoizationPolicy effectively predicts the next action by recognizing the user's historical interaction.

a. User Input (earlier)
- User: What's the weather like in Rethymno?

rules:
- rule: Submit Weather form with location
  condition:
    - active_loop: weather_form
    - slot_was_set:
        - requested_slot: location
          
  steps:
    - action: weather_form
    - active_loop: null
    - action: action_provide_weather

b. User Input (now)
- User: Tell me the weather tomorrow.

rules:
- rule: Submit Weather form with date
  condition:
    - active_loop: weather_form
    - slot_was_set:
        - requested_slot: date
          
  steps:
    - action: weather_form
    - active_loop: null
    - action: action_provide_weather
 
### Non-Functioning Example:
Consider a scenario where the user has already mentioned the location in a prior interaction, and the MemoizationPolicy fails to recognize this context. Despite the user providing the location earlier, the MemoizationPolicy fails to appropriately utilize the user's historical input and unnecessarily repeats a question about the location.

a. User Input (earlier)
- User: What's the weather like in Rethymno?

rules:
- rule: Submit Weather form with location
  condition:
    - active_loop: weather_form
    - slot_was_set:
        - requested_slot: location
          
  steps:
    - action: weather_form
    - active_loop: null
    - action: action_provide_weather

b. User Input (now)
- User: Tell me about the weekend forecast.
  
rules:
- rule: Submit Weather form with location
  condition:
    - active_loop: weather_form
    - slot_was_set:
        - requested_slot: location
          
  steps:
    - action: weather_form
    - active_loop: null
    - action: action_provide_weather

## TEDPolicy

### Proper Functioning Example:
Consider a scenario where the user uses various ways to express the same intent of asking about the weather such as "What's the weather like tomorrow in Athens?" or "Tell me the forecast in Athens for tomorrow.". The TEDPolicy successfully generalizes patterns in these variations and accurately predicts the activation of the weather_form and subsequent action_provide_weather.

User Input 
- User: What's the weather like in Athens tomorrow?

rules:
- rule: Submit Weather form with location and date
  condition:
    - active_loop: weather_form
    - slot_was_set:
        - requested_slot: location
        - requested_slot: date
          
  steps:
    - action: weather_form
    - active_loop: null
    - action: action_provide_weather


### Non-Functioning Example 
In this non-functioning example, the TEDPolicy may not effectively generalize from variations in the order of slot values provided by the user, leading to a misprediction of the correct action within the weather form.

User Input 
- User: Tell me the forecast in Athens for today.

rules:
- rule: Submit Weather form with location
  condition:
    - active_loop: weather_form
    - slot_was_set:
        - requested_slot: location
          
  steps:
    - action: weather_form
    - active_loop: null
    - action: action_provide_weather

# Optimizing the TEDPolicy

### Overview
This repository focuses on optimizing the chatbot policy, with a primary emphasis on enhancing the TEDPolicy. The main objective is to improve the model's capacity to generalize from diverse user inputs and accurately predict the correct actions across various scenarios.

## Optimization Goals
1.	Generalization: Enable the model to understand and respond effectively to diverse user inputs, especially in scenarios where users express the same intent in different ways.
2.	Prediction Accuracy: Enhance the accuracy of the TEDPolicy in predicting the correct actions based on historical conversation context.

## Optimization Process

## TEDPolicy Hyperparameter Tuning
•	max_history: Increased the max_history parameter to 20 to capture a more extended context of user inputs, allowing the model to better understand the conversation flow.

•	epochs: Adjusted the epochs parameter to 150 to ensure sufficient training iterations for effective learning while avoiding overfitting.

•	constrain_similarities: Enabled constrain_similarities to prevent overly similar examples from dominating the training process.

## Test Cases for TEDPolicy Optimization
To assess the impact of the optimization, the following indicative test cases were implemented:

### 1. Varied Weather Expressions Test:
•	User input: "What's the weather in Athens today?"

•	User input: "Tell me the current weather for today"

•	User input: "Describe the temperature in Crete"

•	Expected: TEDPolicy accurately predicts the activation of the weather_form and action_provide_weather.

### 2. Invalid Input Test:
•	User input: "I’m lost"

•	User input: "Huh?"

•	Expected: TEDPolicy correctly triggers a fallback response, recognizing the invalid user input.








