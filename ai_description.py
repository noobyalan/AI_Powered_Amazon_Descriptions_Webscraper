import openai, json

with open('output.json', 'r', encoding='utf-8') as f:
    goods_dict = json.load(f)

with open('item_summarizer.txt', 'r', encoding='utf-8') as f:
    system_prompt = f.read()

openai_api_key = 'sk-xxx'
openai_backend = None

client = openai.OpenAI(api_key=openai_api_key, base_url=openai_backend)
index = 0
for items in goods_dict:
    index += 1
    print(f"Processing product {index}/{len(goods_dict)}: {items}")
    product = goods_dict[items]
    colors = [sku['english_name'] for sku in product['skus']]
    product_input = f"{product['title']}\n Available colors: {', '.join(colors)}"
    product_summary = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': product_input
            }
        ],
        stream=False)
    product['ai_title'] = product_summary.choices[0].message.content.split('\n')[0]
    product['ai_description'] = '\n'.join(product_summary.choices[0].message.content.split('\n')[2:])

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(goods_dict, f, ensure_ascii=False, indent=2)
