import json
import os


class AnimationReader(object):
    def __init__(self, resourceFolderPath):
        self.resourceFolderPath = resourceFolderPath
        self.succeeded = True

    def get_animations(self):
        fileList = os.listdir(self.resourceFolderPath)
        result = []
        for i in fileList:
            with open(self.resourceFolderPath + '/' + i) as f:
                data = json.load(f)
                result.append(data['title'])
        return result