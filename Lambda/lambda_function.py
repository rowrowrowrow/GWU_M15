### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")
    
### Functionality Helper Functions ###
def parse_float(n):
    """
    Securely converts a non-numeric value to float.
    """
    try:
        return float(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_session_state(intent_request):
    """
    Get the current session state.
    """
    return intent_request["sessionState"]

### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return get_session_state(intent_request)["intent"]["slots"]

def get_age_string(intent_request):
    """
    Get the age's interpreted value as a string.
    """
    if get_slots(intent_request)["age"]:
        return get_slots(intent_request)["age"]["value"]["interpretedValue"]
    return get_slots(intent_request)["age"]

def get_investment_amount_string(intent_request):
    """
    Get the investmentAmount's interpreted value as a string.
    """
    if get_slots(intent_request)["investmentAmount"]:
        return get_slots(intent_request)["investmentAmount"]["value"]["interpretedValue"]
    return get_slots(intent_request)["investmentAmount"]

def get_first_name_string(intent_request):
    """
    Get the firstName's interpreted value as a string.
    """
    if get_slots(intent_request)["firstName"]:
        return get_slots(intent_request)["firstName"]["value"]["interpretedValue"]
    return get_slots(intent_request)["firstName"]

def get_risk_level_string(intent_request):
    """
    Get the riskLevel's interpreted value as a string.
    """
    if get_slots(intent_request)["riskLevel"]:
        return get_slots(intent_request)["riskLevel"]["value"]["interpretedValue"]
    return get_slots(intent_request)["riskLevel"]

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionState": {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "ElicitSlot",
                "slotToElicit": slot_to_elicit,
            },
            "intent": {
                "slots": slots,
                "name": intent_name,
            }
        },
        "messages":[message]
    }


def delegate(session_attributes, slots, intent_name):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionState": {
            "sessionAttributes": session_attributes,
            "dialogAction": {"type": "Delegate"},
            "intent": {
                "slots": slots,
                "name": intent_name,
            }
        }
    }


def close(session_attributes, fulfillment_state, message, slots, intent_name):
    """
    Defines a close slot type response.
    """
    
    return {
        "sessionState": {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": fulfillment_state,
            },
            "intent": {
                "slots": slots,
                "name": intent_name,
                "state": fulfillment_state
            }
        },
        "messages":[message]
    }


"""
Step 3: Enhance the Robo Advisor with an Amazon Lambda Function

In this section, you will create an Amazon Lambda function that will validate the data provided by the user on the Robo Advisor.

1. Start by creating a new Lambda function from scratch and name it `recommendPortfolio`. Select Python 3.7 as runtime.

2. In the Lambda function code editor, continue by deleting the AWS generated default lines of code, then paste in the starter code provided in `lambda_function.py`.

3. Complete the `recommend_portfolio()` function by adding these validation rules:

    * The `age` should be greater than zero and less than 65.
    * The `investment_amount` should be equal to or greater than 5000.

4. Once the intent is fulfilled, the bot should respond with an investment recommendation based on the selected risk level as follows:

    * **none:** "100% bonds (AGG), 0% equities (SPY)"
    * **low:** "60% bonds (AGG), 40% equities (SPY)"
    * **medium:** "40% bonds (AGG), 60% equities (SPY)"
    * **high:** "20% bonds (AGG), 80% equities (SPY)"

> **Hint:** Be creative while coding your solution, you can have all the code on the `recommend_portfolio()` function, or you can split the functionality across different functions, put your Python coding skills in action!

5. Once you finish coding your Lambda function, test it using the sample test events provided for this Challenge.

6. After successfully testing your code, open the Amazon Lex Console and navigate to the `recommendPortfolio` bot configuration, integrate your new Lambda function by selecting it in the “Lambda initialization and validation” and “Fulfillment” sections.

7. Build your bot, and test it with valid and invalid data for the slots.

"""

allowed_risk_levels = [
    'none',
    'low',
    'medium',
    'high'
]

def get_recommendation_for_risk_level(risk_level):
    if risk_level is 'none':
        return "100% bonds (AGG), 0% equities (SPY)"
    if risk_level is 'low':
        return "60% bonds (AGG), 40% equities (SPY)"
    if risk_level is 'medium':
        return "40% bonds (AGG), 60% equities (SPY)"
    if risk_level is 'high':
        return "20% bonds (AGG), 80% equities (SPY)"

def validate_data(first_name, age, investment_amount, risk_level, intent_request):
    """
    Validates the data provided by the user.
    """
            
    # Validate the firstName
    if first_name is not None:
        if len(first_name) < 1:
            return build_validation_result(
                False,
                "firstName",
                "Please submit a value for your first name.",
            )
            
    # Validate the age
    if age is not None:
        age_integer = parse_int(age)
        if not age_integer < 65 or not age_integer > 0:
            return build_validation_result(
                False,
                "age",
                "Please submit an age  greater than zero and less than 65.",
            )
            
    # Validate the investmentAmount
    if investment_amount is not None:
        investment_amount_as_float = parse_float(
            investment_amount
        )  # Since parameters are strings it's important to cast values
        if investment_amount_as_float < 5000:
            return build_validation_result(
                False,
                "investmentAmount",
                "The investment amount should be greater than 5000, "
                "please provide a correct amount to invest.",
            )
            
    # Validate the riskLevel
    if risk_level is not None:
        if risk_level not in allowed_risk_levels:
            return build_validation_result(
                False,
                "riskLevel",
                f"Please provide a valid risk level, one of the following: {', '.join(allowed_risk_levels)}.",
            )

    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)


### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_first_name_string(intent_request)
    age = get_age_string(intent_request)
    investment_amount = get_investment_amount_string(intent_request)
    risk_level = get_risk_level_string(intent_request)
    source = intent_request["invocationSource"]
    
    # Gets all the slots
    slots = get_slots(intent_request)

    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Validates user's input using the validate_data function
        validation_result = validate_data(first_name, age, investment_amount, risk_level, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                get_session_state(intent_request)["sessionAttributes"],
                get_session_state(intent_request)["intent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attributes
        output_session_attributes = get_session_state(intent_request)["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request), get_session_state(intent_request)["intent"]["name"])
    
    recommendation = get_recommendation_for_risk_level(risk_level)
    
    # Return a message with conversion's result.
    return close(
        get_session_state(intent_request)["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Thank you for your information {};
            based on your risk tolerance ({}), we recommend the following portfolio allocation: {}
            """.format(
                first_name, risk_level, recommendation
            ),
        },
        slots,
        get_session_state(intent_request)["intent"]["name"]
    )


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = get_session_state(intent_request)["intent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "recommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
