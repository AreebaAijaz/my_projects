import gradio as gr
from main import extract_invoice, extract_invoice_from_image
import os

def process_text(text):
    if not text.strip():
        return {"error": "Please paste invoice text."}
    try:
        return extract_invoice(text).model_dump()
    except Exception as e:
        return {"error": str(e)}

def process_image(image):
    if image is None:
        return {"error": "Please upload an invoice image."}
    try:
        return extract_invoice_from_image(image).model_dump()
    except Exception as e:
        return {"error": str(e)}

text_interface = gr.Interface(
    fn=process_text,
    inputs=gr.Textbox(
        lines=12,
        placeholder="Paste raw invoice text here...",
        label="Raw Invoice Text"
    ),
    outputs=gr.JSON(label="Extracted & Validated Invoice"),
    description=(
        "Extracts structured invoice data using OpenAI structured outputs + Pydantic validation. "
        "Missing fields are left null rather than guessed. If the stated total doesn't match the "
        "sum of line items, total_mismatch is flagged instead of silently corrected."
    ),
    examples=[
        ["Acme Supplies Inc.\nInvoice #: INV-2091\nDate: July 15, 2026\n\nItems:\n- Widget A, Qty: 4, Price: $12.50 each\n- Widget B, Qty: 2, Price: $30.00 each\n\nTotal: $110.00"],
        ["Fast Supplies Co.\nInvoice #: INV-500\nDate: 2026-01-10\n\nItems:\n- Item A, Qty: 2, Price: $10.00 each\n- Item B, Qty: 1, Price: $5.00 each\n\nTotal: $100.00"]
    ]
)

image_interface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="filepath", label="Invoice Image"),
    outputs=gr.JSON(label="Extracted & Validated Invoice"),
    description="Upload a photo or scan of an invoice to extract structured, validated data."
)

demo = gr.TabbedInterface(
    [text_interface, image_interface],
    ["Paste Text", "Upload Image"],
    title="JSON Validated Invoice Extraction Agent"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))