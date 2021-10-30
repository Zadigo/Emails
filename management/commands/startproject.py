from management.base import ProjectCommand
from zineb.management.base import ProjectCommand


class Command(ProjectCommand):
    def add_arguments(self, parser):
        parser.add_argument('project_name')
