import os.path
import subprocess
import ppm
import ppm.exceptions
import ppm.tool


class Checker():

    def __init__(self, project_name):
        """
        """
        self.project_name = project_name
        self.project_path = ppm.python_projects_path / project_name
        self.result = {'type':'',
                       'git status':''}

    def check_structure_consistency(self):
        """
        """
        project_type = ppm.tool.get_project_type(self.project_path, self.project_name)
        if project_type != 'package' and project_type != 'app':
            raise ppm.exceptions.ProjectStructureInconsistencyException

    def check_virtual_environment(self):
        """
        """
        if not os.path.isdir(self.project_path / 'venv'):
            raise ppm.exceptions.ProjectVirtualEnvironmentNotFoundException

    def check_local_repository(self):
        """
        """
        if not os.path.isdir(self.project_path / 'src/.git'):
            raise ppm.exceptions.ProjectLocalRepositoryNotFoundException



    def get_git_status(self):
        """
        """
            cp = subprocess.run(["git", "remote"], cwd=self.project_path / 'src', capture_output=True)
            
            if "origin" not in cp.stdout.decode('UTF-8'):
                return "remote repository not found"

            cp = subprocess.run(["git", "status"], cwd=self.project_path / 'src', capture_output=True)
            
            if (   "Changes not staged for commit" in cp.stdout.decode('UTF-8')
                or "Changes to be committed"       in cp.stdout.decode('UTF-8')):
                return "uncommitted changes"
                
            if "Your branch is ahead of 'origin/master'" in cp.stdout.decode('UTF-8'):
                return "remote outdated"
                
            if "nothing to commit, working directory clean" in cp.stdout.decode('UTF-8'):
                return "ok"
                
            return "???"
