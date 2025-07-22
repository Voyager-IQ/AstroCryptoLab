from openai import OpenAI
import json

# Configure the client to connect to the local LM Studio server
# The API key is not required for local servers but the library expects a value.
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def analyze_text_with_gpt(text_content: str) -> dict:
    """
    Analyzes a news article using a local GPT model to extract sentiment,
    mentioned assets, and market signals.

    Args:
        text_content: The summary or content of the news article.

    Returns:
        A dictionary with the analysis results, or an error message.
    """
    # This prompt is designed to guide the model towards a structured, JSON-like output.
    # It clearly defines the expected fields and potential values.
    prompt = f"""
    As a specialized cryptocurrency financial analyst, your task is to analyze the following news article.
    Provide your analysis in a structured format. The required fields are:
    - "sentiment": Classify the overall tone (e.g., "Positive", "Neutral", "Negative").
    - "mentioned_assets": List all cryptocurrency assets, tokens, or projects mentioned (e.g., ["Bitcoin", "Ethereum"]). If none, use an empty list.
    - "investment_signal": Based on the text, describe the potential market interest or hype (e.g., "Strong buy signal", "Potential for hype", "Bearish sentiment", "Informational only").

    Here is the news article:
    ---
    {text_content}
    ---

    Provide only the structured analysis based on the text.
    """

    try:
        completion = client.chat.completions.create(
            # Select the model you have loaded in LM Studio
            # e.g., "Nous-Hermes-2-Mistral-7B-DPO-GGUF"
            # You can get the exact model name from the LM Studio UI.
            model="local-model",
            messages=[
                {"role": "system", "content": "You are a cryptocurrency financial analyst providing structured data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,  # Lower temperature for more deterministic, analytical output
        )

        response_content = completion.choices[0].message.content

        # Basic parsing of the response. A more robust solution might use regex
        # or ask the model to return valid JSON.
        lines = response_content.strip().split('\n')
        analysis_result = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().replace('"', '').replace('-', '').strip()
                value = value.strip().replace('"', '')
                analysis_result[key] = value

        # Default values if keys are missing
        return {
            'sentiment': analysis_result.get('sentiment', 'N/A'),
            'mentioned_assets': analysis_result.get('mentioned_assets', 'N/A'),
            'investment_signal': analysis_result.get('investment_signal', 'N/A')
        }

    except Exception as e:
        print(f"An error occurred during GPT processing: {e}")
        return {
            'sentiment': 'Error',
            'mentioned_assets': 'Error',
            'investment_signal': str(e)
        }

