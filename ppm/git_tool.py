import git


def clone(from_url, to_path):
    """
    """
    git.Repo.clone_from(url=from_url, to_path=to_path)

def fork(from_url, to_path):
    """
    """

    # Clone the git
    clone(from_url=from_url, to_path=to_path)

    # Be careful: path must contain an existing .git folder.
    repo = git.Repo(path=to_path)

    # Because there has been a 'clone' operation, there exists a 'origin' remote ref.
    # Rename the "origin" remote into 'upstream'
    remote = git.remote.Remote(repo, 'origin')
    remote.rename('upstream')