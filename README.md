Here's a GitHub README for the script you provided:

---

# AI-Powered Product Descriptions Generator

This project utilizes OpenAI's GPT-4o-mini model to generate AI-powered product titles and descriptions based on a list of products stored in a JSON file. The script reads product data and system prompts, sends the product information to the OpenAI API, and updates the JSON file with AI-generated titles and descriptions.

## Requirements

- Python 3.x
- OpenAI API key
- Install the following Python libraries:
  - `openai`
  - `json`

You can install the required Python packages using `pip`:

```bash
pip install openai
```

## Setup

1. **Create the necessary files:**
   - **`output.json`**: This file should contain the product data with details such as title, skus, etc. The script will read from this file and update it with AI-generated product titles and descriptions.
   - **`item_summarizer.txt`**: This file should contain the system prompt for the AI to generate product descriptions. The system prompt helps guide the AI's output.

2. **Set your OpenAI API key**:
   Replace `'sk-xxx'` in the code with your actual OpenAI API key.

## How It Works

1. The script loads the product data from `output.json`.
2. It reads the system prompt from `item_summarizer.txt`.
3. It processes each product in the JSON, sending product details (such as title and available colors) to OpenAI's API.
4. It generates an AI-powered title and description for each product.
5. The script updates the product data in the `output.json` file with the AI-generated content.

## Code Walkthrough

```python
import openai, json

# Load the product data from the JSON file
with open('output.json', 'r', encoding='utf-8') as f:
    goods_dict = json.load(f)

# Load the system prompt from the text file
with open('item_summarizer.txt', 'r', encoding='utf-8') as f:
    system_prompt = f.read()

# Set your OpenAI API key
openai_api_key = 'sk-xxx'
openai_backend = None

# Initialize the OpenAI client
client = openai.OpenAI(api_key=openai_api_key, base_url=openai_backend)

# Process each product in the goods_dict
index = 0
for items in goods_dict:
    index += 1
    print(f"Processing product {index}/{len(goods_dict)}: {items}")
    product = goods_dict[items]
    
    # Extract available colors
    colors = [sku['english_name'] for sku in product['skus']]
    
    # Prepare the input for AI generation
    product_input = f"{product['title']}\n Available colors: {', '.join(colors)}"
    
    # Call OpenAI API to generate the product summary
    product_summary = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': product_input}
        ],
        stream=False
    )
    
    # Update the product with AI-generated title and description
    product['ai_title'] = product_summary.choices[0].message.content.split('\n')[0]
    product['ai_description'] = '\n'.join(product_summary.choices[0].message.content.split('\n')[2:])

# Save the updated product data to the JSON file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(goods_dict, f, ensure_ascii=False, indent=2)
```

## Output

After running the script, the `output.json` file will be updated with the following additional fields for each product:

- `ai_title`: The AI-generated product title.
- `ai_description`: The AI-generated product description.

## Example Output (JSON)

```json
{
  "product1": {
    "title": "Sample Product 1",
    "skus": [
      {"english_name": "Red"},
      {"english_name": "Blue"}
    ],
    "ai_title": "AI Generated Title for Product 1",
    "ai_description": "This is the AI-generated description for Product 1. It includes all the features and details."
  },
  "product2": {
    "title": "Sample Product 2",
    "skus": [
      {"english_name": "Green"},
      {"english_name": "Yellow"}
    ],
    "ai_title": "AI Generated Title for Product 2",
    "ai_description": "This is the AI-generated description for Product 2. It highlights the product's key aspects."
  }
}
```

