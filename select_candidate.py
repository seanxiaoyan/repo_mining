import requests
import csv
from time import sleep
import sys

# TOKEN = "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"
TOKEN = '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'


def save_current_state(selected_repo, visit_count):
    with open('selected_repo.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(selected_repo)

    print(f"visited {visit_count} repos")
    
    sys.exit(0)


# read repo.csv file
with open('ranked_repo.csv', 'r') as f:
    reader = csv.reader(f)
    repo_list = list(reader)

# for each repo, use its Rname to construct the url, and then check if this repo is a fork
count = 0

visit_count = 0

selected_repo = [repo_list[0]]

processed = set()

for repo in repo_list:
    if len(selected_repo) > 30 or visit_count > 2000:
        save_current_state(selected_repo)

    visit_count += 1
    # omit the first row
    if repo[0] == 'Rname':
        continue
    
    # check if the repo has been processed
    if repo[0] in processed:
        continue
    if repo[0].split('/')[1] in processed:
        continue
    
    # add the repo to the processed set
    processed.add(repo[0])
    processed.add(repo[0].split('/')[1])

    print(f"processing {repo[0]}")
    sleep(1)

    url = 'https://api.github.com/repos/' + repo[0]


    response = requests.get(url, headers={'Authorization': '{}'.format(TOKEN)})

    if response.status_code == 200:
        # check if the repo is a fork
        if response.json()['fork'] == True \
            and response.json()['parent']['stargazers_count']>80 \
                and response.json()['parent']['language'] == 'Python':
            parent_repo_name = response.json()['parent']['full_name']

            
            if parent_repo_name in processed:
                continue
            processed.add(parent_repo_name)
            processed.add(repo[0].split('/')[1])
            selected_repo.append([parent_repo_name, "N/A", "N/A", repo[3], repo[4], repo[5]])
            count += 1
            
        else:
            if response.json()['stargazers_count']<80 or response.json()['language'] != 'Python':
                continue

            if repo[0] in processed:
                continue
            processed.add(repo[0])
            processed.add(repo[0].split('/')[1])
            selected_repo.append([repo[0], repo[1], repo[2], repo[3], repo[4], repo[5]])
            count += 1        
        

        
    elif response.status_code == 403:
        print(f"-error: {repo[0]} - {response.json()['message']}")
    else:
        print(f"-error: {repo[0]} - {response.status_code} - {response.json()['message']}")    



