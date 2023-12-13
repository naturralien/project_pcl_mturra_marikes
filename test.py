import json

result_data = []
with open('text.txt', 'r') as f:
    for content in f:
        words = content.strip().split(',')
        result_data.extend([{'Name': word} for word in words])
        result_data.pop() #remove the last element of the list because it's empty
        json_str = json.dumps(result_data)
        print(json_str)

with open('text_output.json', 'w') as f:
    json.dump(result_data, f)