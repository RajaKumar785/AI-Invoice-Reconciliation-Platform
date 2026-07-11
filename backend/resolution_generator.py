from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_resolution_note(po_data, invoice_data, match_result):

    prompt = f"""
You are a Senior Finance Audit Officer working in an enterprise ERP system.

Your responsibility is to review the comparison between a Purchase Order and a Vendor Invoice.

Purchase Order
----------------
{po_data}

Vendor Invoice
----------------
{invoice_data}

Comparison Result
----------------
{match_result}

Prepare a professional finance resolution.

Instructions:

1. Mention whether the invoice should be APPROVED or kept ON HOLD.

2. Explain every mismatch clearly.

3. Mention possible financial risks such as:
- Wrong Vendor
- Wrong PO
- GST Difference
- Quantity Difference
- Price Difference
- Amount Difference

4. Mention overall risk level.

5. Give a recommendation for the Finance Team.

6. Keep the response professional.

7. Maximum 150 words.

Return only the resolution note.
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0,

        messages=[

            {
                "role": "system",
                "content": "You are an experienced Finance Auditor and ERP Reconciliation Expert."
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    return response.choices[0].message.content