import requests
import json

# Membaca auth_data dari file hashes.txt
def read_auth_data(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

auth_data_list = read_auth_data('hashes.txt')

# URL untuk GET requests
quest_ids = [17, 7, 6, 5, 4, 3, 1]

# URL untuk POST requests
task_ids = [39, 4, 3, 2, 19, 13, 7, 9, 8, 10, 11, 23]

# Mapping tasks to their respective quests
task_to_quest_map = {
    2: 1,
    3: 1,
    4: 1,
    7: 3,
    8: 4,
    9: 4,
    10: 5,
    11: 6,
    13: 7,
    19: 7,
    23: 17,
    39: 1
}

def get_quest(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get("account_quest", {}).get("is_complete", False)
    except requests.RequestException as e:
        print(f"Failed to GET quest from {url}: {e}")
        return False

def post_task(url):
    try:
        response = requests.post(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get("account_task", {}).get("is_complete", False)
    except requests.RequestException as e:
        print(f"Failed to POST task to {url}: {e}")
        return False

def process_account(auth_data):
    quest_urls = {quest_id: f'https://api.supermeow.vip/meow/quests/{quest_id}/?{auth_data}' for quest_id in quest_ids}
    post_urls = {task_id: f'https://api.supermeow.vip/meow/tasks/{task_id}/do?{auth_data}' for task_id in task_ids}

    # Melakukan GET requests untuk semua quest
    all_quests_complete = True
    for quest_id, quest_url in quest_urls.items():
        quest_complete = get_quest(quest_url)
        if not quest_complete:
            all_quests_complete = False
            break

    if not all_quests_complete:
        print("Proceeding with tasks as one or more quests are incomplete...\n")
        # Melakukan POST requests
        for task_id, post_url in post_urls.items():
            print(f"Completing task {task_id}...")
            task_complete = post_task(post_url)
            if task_complete:
                print(f"Task {task_id} complete.")
            else:
                print(f"Task {task_id} not complete.")

            # Cross-check the associated quest to confirm task completion
            associated_quest_id = task_to_quest_map[task_id]
            associated_quest_url = quest_urls[associated_quest_id]
            quest_complete = get_quest(associated_quest_url)
            if quest_complete:
                print(f"Quest {associated_quest_id} complete after task {task_id}.")
            else:
                print(f"Quest {associated_quest_id} still not complete after task {task_id}.\n")
    else:
        print("All quests are already complete.")

def main():
    for index, auth_data in enumerate(auth_data_list, start=1):
        print(f"\nProcessing account {index}...\n{'-'*20}")
        process_account(auth_data)

if __name__ == "__main__":
    main()
