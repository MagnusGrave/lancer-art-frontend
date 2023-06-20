# Our data structure that holds an image's path and it's file tags.
class ImageObject:
    def __init__(self, file_path, tags):
        # The files path relative to the project directory
        self.file_path = file_path
        # A list of strings of all the metadata tags found in the file
        self.tags = tags
        