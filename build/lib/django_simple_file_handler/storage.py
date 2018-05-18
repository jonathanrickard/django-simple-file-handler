from django.core.files.storage import (
    FileSystemStorage
)


class RemoveOldFile(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
