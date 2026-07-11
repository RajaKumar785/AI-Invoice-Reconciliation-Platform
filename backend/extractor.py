from openai import OpenAI
from dotenv import load_dotenv
import os

from utils.finance_parser import prepare_finance_text
from utils.table_parser import extract_table_lines
from utils.amount_parser import extract_grand_total
from utils.item_parser import structure_items

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def extract_document_data(text, document_type):

    # --------------------------------------------------
    # Clean OCR
    # --------------------------------------------------

    cleaned_text = prepare_finance_text(
        text[:6000]
    )

    # --------------------------------------------------
    # Table Extraction
    # --------------------------------------------------

    table_text = extract_table_lines(
        cleaned_text
    )

    # --------------------------------------------------
# Structured Item Extraction
# --------------------------------------------------

    structured_items = structure_items(
    cleaned_text
    )


    # --------------------------------------------------
    # Grand Total Detection
    # --------------------------------------------------

    grand_total = extract_grand_total(
        cleaned_text
    )

    # --------------------------------------------------
    # AI Prompt
    # --------------------------------------------------

    prompt = f"""
You are an Enterprise Financial Document Extraction AI.

Your task is to extract structured information from Purchase Orders and Vendor Invoices.

OCR may contain spelling mistakes.

Examples

Flardware → Hardware

ConGestie → Angle

oo → Angle

Correct ONLY obvious OCR mistakes.

IMPORTANT RULES

1. Return ONLY valid JSON.
2. Never explain anything.
3. Never use markdown.
4. Never wrap JSON inside ```.

5. Preserve document values exactly.

6. Never calculate values.

7. Extract EVERY line item separately.

8. Never merge multiple rows.

9. Ignore table headers.

10. Amount MUST be Grand Total.

11. GST must be GST percentage.

Examples

GST @18%
↓

18%

CGST 9%
SGST 9%

↓

18%

12. Purchase Orders usually have no Invoice Number.

13. If Invoice Number is absent return "".

14. If OCR contains duplicated text ignore duplicates.

Return EXACTLY this JSON

{{
    "Vendor":"",
    "PO Number":"",
    "Invoice Number":"",
    "Document Date":"",
    "Items":[
        {{
            "Description":"",
            "Quantity":"",
            "Unit Price":""
        }}
    ],
    "GST":"",
    "Amount":""
}}

DOCUMENT TYPE

{document_type}

FULL OCR

--------------------------------

{cleaned_text}

--------------------------------

TABLE OCR

--------------------------------

{table_text}

--------------------------------
STRUCTURED ITEMS

--------------------------------

{structured_items}

--------------------------------

DETECTED GRAND TOTAL

--------------------------------

{grand_total}

--------------------------------

IMPORTANT

• If Detected Grand Total is NOT empty,
always use it as Amount.

• Never calculate Grand Total.

• Never use Subtotal.

• Never invent Amount.

Return ONLY JSON.
"""
    # --------------------------------------------------
    # AI Call
    # --------------------------------------------------

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0,

        max_tokens=1500,

        messages=[

            {
                "role": "system",
                "content": (
                    "You are an Enterprise Financial Document Extraction AI. "
                    "Always return ONLY valid JSON. "
                    "Never explain anything. "
                    "Never use markdown."
                )
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    # --------------------------------------------------
    # Extract Response
    # --------------------------------------------------

    content = response.choices[0].message.content.strip()

    # Remove markdown if model returns it accidentally

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return content