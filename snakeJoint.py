class JOINT:
    def __init__(self, jointName, parentLink, childLink, jointType, jointPos, jointAxis):
        self.parentLink = parentLink
        self.childLink = childLink
        self.jointType = jointType
        self.jointName = jointName
        self.jointPos = jointPos
        self.jointAxis = jointAxis