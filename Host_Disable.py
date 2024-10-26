import requests
import json

# API Ayarları
API_URL_BASE = 'https://ENV/api/v2'
API_TOKEN = 'Api-Token Token'  # Değiştirilecek
HEADERS = {
    'Accept': 'application/json; charset=utf-8',
    'Authorization': API_TOKEN,
}

def get_hosts():
    """Belirtilen URL'den host bilgilerini alır."""
    url = f'{API_URL_BASE}/entities?entitySelector=type("HOST")'
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        hosts = {
            entity['entityId']: entity['displayName'] 
            for entity in data.get('entities', [])
        }
        return hosts
    else:
        print(f"Error fetching hosts: {response.status_code} - {response.text}")
        return {}

def update_host_monitoring(entity_id, enabled=False):
    """Belirtilen host için izleme ayarlarını günceller."""
    url = f'{API_URL_BASE}/settings/objects'
    payload = [
        {
            "schemaId": "builtin:host.monitoring",
            "schemaVersion": "1.4",
            "scope": entity_id,
            "value": {"enabled": enabled}
        }
    ]
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        print(f"Successfully updated {entity_id}: {enabled}")
    else:
        print(f"Error updating {entity_id}: {response.status_code} - {response.text}")

def disable_monitoring():
    """Tüm hostların izlemelerini devre dışı bırakır."""
    hosts = get_hosts()
    for entity_id in hosts.keys():
        update_host_monitoring(entity_id, enabled=False)

def enable_monitoring():
    """Tüm hostların izlemelerini etkinleştirir."""
    hosts = get_hosts()
    for entity_id in hosts.keys():
        update_host_monitoring(entity_id, enabled=True)

if __name__ == "__main__":
    import sys
    sys.argv.append("enable")  # Test 
    if len(sys.argv) > 1:
        if sys.argv[1] == "disable":
            disable_monitoring()
        elif sys.argv[1] == "enable":
            enable_monitoring()
        else:
            print("Invalid argument. Use 'disable' or 'enable'.")
    else:
        print("Please provide 'disable' or 'enable' as an argument.")
