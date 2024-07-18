import json
with open('Free_Proxy_List.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

output_lines = []
for entry in data:
    ip = entry['ip']
    port = entry['port']
    formatted_entry = f"{ip}:{port}\n"
    output_lines.append(formatted_entry)

with open('formatted_proxies.txt', 'a', encoding='utf-8') as f:
    f.writelines(output_lines)

print("Formatted proxies saved to 'formatted_proxies.txt'.")