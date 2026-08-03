import os
from dotenv import load_dotenv 
from openai import OpenAI 
from schema import Invoice
import base64


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



system_prompt = (
    "Extract structured invoice data from the text provided. "
    "Only fill in a field if it is explicitly stated or unambiguous in the source text. "
    "If a value is missing, ambiguous, or would require guessing (e.g. an incomplete date, "
    "an unstated total), leave that field as null rather than inferring or calculating it."
)



# # bad_total_text = """
# # Fast Supplies Co.
# # Invoice #: INV-500
# # Date: 2026-01-10

# # Items:
# # - Item A, Qty: 2, Price: $10.00 each
# # - Item B, Qty: 1, Price: $5.00 each

# # Total: $100.00
# # """

def extract_invoice(text, max_retries=3):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]

    for attempt in range(max_retries):
        try:
            response = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=messages,
                response_format=Invoice
            )
            refusal = response.choices[0].message.refusal
            if refusal:
                raise ValueError(f"Model refused: {refusal}")

            return response.choices[0].message.parsed

        except Exception as e:
            print(f"Attempt {attempt+1} failed validation: {e}")
            messages.append({"role": "user", "content": f"Your previous output failed validation: {e}. Please correct it and try again."})

    raise ValueError("Max retries exceeded, could not get valid invoice.")


# # if __name__ == "__main__":
# #     result = extract_invoice(bad_total_text)
# #     print(result)





def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def extract_invoice_from_image(image_path, max_retries=3):
    base64_image = encode_image(image_path)
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the invoice data from this image."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]

    for attempt in range(max_retries):
        try:
            response = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=messages,
                response_format=Invoice
            )
            refusal = response.choices[0].message.refusal
            if refusal:
                raise ValueError(f"Model refused: {refusal}")
            return response.choices[0].message.parsed
        except Exception as e:
            print(f"Attempt {attempt+1} failed validation: {e}")
            messages.append({"role": "user", "content": f"Your previous output failed validation: {e}. Please correct it and try again."})

    raise ValueError("Max retries exceeded, could not get valid invoice.")