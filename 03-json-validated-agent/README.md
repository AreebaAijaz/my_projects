# JSON Validated Invoice Extraction Agent

An AI agent that extracts structured, validated data from invoices — either raw text or an image — using OpenAI structured outputs and Pydantic validation.

🔗 **Live demo:** https://json-validated-agent.onrender.com
*(Free tier — first load may take 30-50s to wake up.)*

## What it does

Given messy invoice text or a photo of an invoice, the agent returns clean, typed JSON:

- Vendor name, invoice number, date, line items, and total
- Missing/unclear fields are left `null` instead of being guessed or hallucinated
- If the stated total doesn't match the sum of line items, it's flagged via `total_mismatch` instead of silently corrected

## Why this project matters

Raw LLM output is unstructured text — unreliable for any downstream system that needs to parse it. This project solves that with:

- **Schema enforcement**: OpenAI's structured outputs + a Pydantic schema guarantee valid JSON shape every time
- **Honesty over guessing**: the model is instructed to leave uncertain fields empty rather than fabricate plausible-looking data
- **Business-rule validation without over-correction**: a custom Pydantic validator checks totals against line items — but *flags* mismatches rather than blocking the response, since blindly forcing agreement caused the model to discard real source data

## Tech stack

- OpenAI API (structured outputs, GPT-4o vision for image input)
- Pydantic (schema definition + validation)
- Gradio (UI)
- Render (deployment)
