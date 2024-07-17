import requests
import subprocess
import os

# Update with your GitLab data
GITLAB_URL = "https://gitlab.com"
PRIVATE_TOKEN = "YOUR_PRIVATE_TOKEN"
BASE_GROUP_ID = "YOUR_BASE_GROUP_ID"
CLONE_BASE_DIR = "path_to_your_local_directory"

def get_projects(group_id):
    url = f"{GITLAB_URL}/api/v4/groups/{group_id}/projects"
    headers = {"Private-Token": PRIVATE_TOKEN}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_subgroups(group_id):
    url = f"{GITLAB_URL}/api/v4/groups/{group_id}/subgroups"
    headers = {"Private-Token": PRIVATE_TOKEN}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def clone_repository(repo_url, clone_dir):
    if not os.path.exists(clone_dir):
        subprocess.run(["git", "clone", repo_url, clone_dir])
        print(f"Cloned {repo_url} to {clone_dir}")
    else:
        print(f"Directory {clone_dir} already exists, skipping.")

def process_group(group_id, base_dir):
    projects = get_projects(group_id)
    for project in projects:
        repo_url = project["ssh_url_to_repo"]
        repo_name = project["name"]
        clone_dir = os.path.join(base_dir, repo_name)
        clone_repository(repo_url, clone_dir)

    subgroups = get_subgroups(group_id)
    for subgroup in subgroups:
        subgroup_id = subgroup["id"]
        subgroup_name = subgroup["name"]
        subgroup_dir = os.path.join(base_dir, subgroup_name)
        os.makedirs(subgroup_dir, exist_ok=True)
        process_group(subgroup_id, subgroup_dir)

def main():
    os.makedirs(CLONE_BASE_DIR, exist_ok=True)
    process_group(BASE_GROUP_ID, CLONE_BASE_DIR)

if __name__ == "__main__":
    main()
