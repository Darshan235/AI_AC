# Invoice Number Generator (Frontend Only)

This is a simple web-based tool that generates a **unique invoice number** based only on a customer's name.

## Features
- Takes a single input: **Customer Name**
- Generates an invoice number in the format:  
  `PREFIX-YYYYMMDDHHMMSS-RAND4`
- Prefix is auto-created from customer initials
- Timestamp ensures chronological uniqueness
- Random block ensures randomness even with duplicates
- Includes buttons to **copy** invoice number and **generate new**

## How to Use
1. Open `index.html` in any web browser.
2. Type the customer's name.
3. Click **Generate Invoice**.
4. Copy or generate a new one as needed.

## Technologies Used
- HTML5
- CSS3
- Vanilla JavaScript (no frameworks)

## Files Included
- `/frontend/index.html` — main UI
- `/frontend/styles.css` — styling
- `/frontend/app.js` — logic for invoice creation
- `ai_notes.txt` — explains how AI assisted in building this frontend
- `input.txt` — sample input
- `output.txt` — sample invoice output
