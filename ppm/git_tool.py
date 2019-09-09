import git


def fork_repository(repo_to_fork_path, new_repo_path):
    """
    TO CHECK!
    Note: repo_to_fork_path can be:
    - https://github.com/afaucon/templated_package
    - C:/Data/templated_package.git
    """
    
    # Initialize a new git
    # -> git init
    r = git.Repo.init(new_repo_path)

    # Add the repository to fork as an Upstream Remote
    # -> git remote add upstream repo_to_fork_path
    # References:
    #   https://gitpython.readthedocs.io/en/stable/reference.html?highlight=add%20upstream#git.remote.Remote.add
    #   https://gitpython.readthedocs.io/en/stable/reference.html?highlight=create_remote#git.repo.base.Repo.create_remote
    remote = r.create_remote("upstream", url=repo_to_fork_path)

    # Update the repository
    # -> git pull upstream master
    upstream = r.remotes.upstream
    upstream.pull("+refs/heads/*:refs/remotes/upstream/*")