import os
from github import Github
from github import Auth


def push_to_github():
    github_token = os.getenv('GITHUB_TOKEN')
    user = os.getenv('USER')
    langs = os.getenv('LANGS')
    branch = os.getenv('BRANCH')

    auth = Auth.Token(github_token)

    g = Github(auth=auth)

    repo = g.get_repo(str(user))

    files = [f"{lang}.md" for lang in langs.split(",")]
    commit_message = 'Update translations'
    branch_name = 'translations'

    try:
        repo.get_branch(branch_name)
    except Exception as e:
        repo.create_git_ref(
            ref=f'refs/heads/{branch_name}', sha=repo.get_branch(str(branch)).commit.sha)

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"File {file_path} not found. Skipping.")
            continue

        try:
            file_content = repo.get_contents(file_path, ref=branch_name)
            repo.update_file(file_path, commit_message,
                             content, file_content.sha, branch=branch_name)
        except:
            repo.create_file(file_path, commit_message,
                             content, branch=branch_name)

    print('Files uploaded successfully.')


push_to_github()
