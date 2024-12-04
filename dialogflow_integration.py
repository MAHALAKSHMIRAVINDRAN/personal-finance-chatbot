import os
import uuid
import logging
from google.cloud import dialogflow_v2 as dialogflow
from google.protobuf.json_format import MessageToDict

# Configure logging
logging.basicConfig(level=logging.INFO)


def detect_intent_texts(project_id, session_id, text, language_code='en'):
    """
    This function sends a query to Dialogflow and returns the response.
    :param project_id: Google Cloud Project ID
    :param session_id: Unique session identifier (can be any string)
    :param text: The text input to send to Dialogflow
    :param language_code: Language code for the input text (default is English)
    :return: Dialogflow response as a dictionary
    """
    if not project_id:
        raise ValueError("The 'project_id' parameter must be provided.")
    if not text or not isinstance(text, str):
        raise ValueError("The 'text' parameter must be a non-empty string.")

    # Create session client and session path
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    try:
        # Prepare the text input for Dialogflow
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        # Send the query and get the response
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})

        # Log and return the response as a dictionary
        result_dict = MessageToDict(response.query_result)
        logging.info("Dialogflow response: %s", result_dict)
        return result_dict
    except Exception as e:
        logging.error("Failed to detect intent: %s", str(e))
        return {"error": str(e), "message": "Failed to detect intent"}

