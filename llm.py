from groq import Groq
from google import genai

from config import DEFAULT_TEMPERATURE
from prompts import SYSTEM_PROMPT, create_profile_context


def ask_groq(api_key, model, messages, profile):
    """
    Send the conversation to Groq and return the AI response.
    """

    client = Groq(api_key=api_key)

    profile_context = create_profile_context(profile)

    full_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + "\n" + profile_context
        }
    ]

    full_messages.extend(messages)

    response = client.chat.completions.create(
        model=model,
        messages=full_messages,
        temperature=DEFAULT_TEMPERATURE,
    )

    return response.choices[0].message.content


def ask_gemini(api_key, model, messages, profile):
    """
    Send the conversation to Google Gemini
    and return the AI response.
    """

    client = genai.Client(api_key=api_key)

    profile_context = create_profile_context(profile)

    conversation = (
        SYSTEM_PROMPT
        + "\n"
        + profile_context
        + "\n\n"
    )

    for message in messages:

        role = message["role"].upper()

        conversation += (
            f"{role}: {message['content']}\n\n"
        )

    response = client.models.generate_content(
        model=model,
        contents=conversation,
    )

    return response.text


def ask_llm(
    provider,
    api_key,
    model,
    messages,
    profile
):
    """
    Select the appropriate AI provider.
    """

    if not api_key:

        raise ValueError(
            "API key is missing. "
            "Please enter your API key in the sidebar."
        )

    if provider == "Groq":

        return ask_groq(
            api_key,
            model,
            messages,
            profile
        )

    if provider == "Google Gemini":

        return ask_gemini(
            api_key,
            model,
            messages,
            profile
        )

    raise ValueError(
        "Unsupported AI provider."
    )