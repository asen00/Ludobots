from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, sensorYN):

        self.depth  = 3

        if sensorYN == 1: ## link has a sensor
            
            self.string1 = '<material name="Has sensor">'

            self.string2 = '    <color rgba="0.2 0.66 0.31 1.0"/>'

            self.string3 = '</material>'
       
        else: ## link does not have sensor

            self.string1 = '<material name="No sensor">'

            self.string2 = '    <color rgba="0.44 0.78 0.91 1.0"/>'

            self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
