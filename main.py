import sys
import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

def main():
    load_dotenv()

    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="A simple CLI AI Code Assistant using the Gemini API.",
        epilog="Example: python main.py 'How do I build a calculator app?' --verbose" 
    )

    # Required positional argument for the user prompt
    parser.add_argument(
        "prompt",
        type=str,
        nargs='+', # Accepts one or more arguments and joins them into a list
        help="The prompt to send to the AI."
    )

    # Optional flag for verbose output
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true", # Sets the variable to True if the flag is present
        help="Print additional metadata (like token counts)."
    )

    args = parser.parse_args()

    # Join the list of prompt arguments back into a single string
    user_prompt = " ".join(args.prompt)

    # --- Agent Logic ---

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
        )
    except Exception as e:
        print(f"An error occurred during content generation: {e}")
        sys.exit(1)

    # Conditionally print additional information
    if args.verbose:
        print("--- 🤖 Request Metadata ---")
        # Check if usage_metadata is available before accessing its attributes
        if response.usage_metadata:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens:{response.usage_metadata.candidates_token_count}")
        else:
            print("Token usage metadata not available.")
        print("---------------------------\n")
    
    # Print the main response
    print("✨ **AI Response:**")
    print(response.text)

if __name__ == "__main__":
    main()
