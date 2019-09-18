import git


def clone(from_url, to_path):
    """
    """
    git.Repo.clone_from(url=from_url, to_path=to_path)

def fork_repository(repo_to_fork_path, new_repo_path):
    """
    Note: repo_to_fork_path must be:
    - https://github.com/afaucon/templated_package
    """

    # Clone the git
    clone(from_url=repo_to_fork_path, to_path=new_repo_path)

    # Be careful: path must contain an existing .git folder.
    repo = git.Repo(path=new_repo_path)

    # Because there has been a 'clone' operation, there exists a 'origin' remote ref.
    # Rename the "origin" remote into 'upstream'
    remote = git.remote.Remote(repo, 'origin')
    remote.rename('upstream')