import os
from github import Github


def push_to_github():
    github_token = os.getenv('GITHUB_TOKEN')
    user = os.getenv('USER')
    langs = os.getenv("LANGS")

    g = Github(github_token)

    repo = g.get_repo(str(user))

    files = [f"{lang}.md" for lang in langs.split(",")]
    commit_message = 'Update translations'
    branch_name = 'translations'

    repo.create_git_ref(
        ref=f'refs/heads/{branch_name}', sha=repo.get_branch('main').commit.sha)

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        repo.create_file(file_path, commit_message,
                         content, branch=branch_name)

    print('Files uploaded successfully.')


push_to_github()
