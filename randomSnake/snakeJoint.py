class JOINT:
    def __init__(self, jointName, parentLink, childLink, jointPos, jointAxis):
        self.parentLink = parentLink
        self.childLink = childLink
        self.jointName = jointName
        self.jointPos = jointPos
        self.jointAxis = jointAxis