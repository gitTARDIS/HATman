import pyarianne
import time

global wait_time
wait_time=100

def dostuffonCallback():
    print("Calling from python!: "+wait_time)
    wait_time-=1
    if wait_time>0:
        return 1
    else:
        return 0

world=pyarianne.World()
perceptionHandler=pyarianne.PerceptionHandler()

print("Starting pyclient")
pyarianne.setIdleMethod(dostuffonCallback)
pyarianne.connectToArianne("127.0.0.1",32150)
if pyarianne.login("miguel","qwerty"):
    chars=pyarianne.availableCharacters()
    
    if pyarianne.chooseCharacter(chars[0]):
        i=0
        if pyarianne.hasRPMap():
            listObjects=pyarianne.getRPMap()
            print("Printing the whole map sent")
            for j in listObjects:
                print(j.toString())
                
        while i in range(10):            
            if pyarianne.hasPerception():
                perception=pyarianne.getPerception()
                perceptionHandler.applyPerception(perception, world)

                print("Perception --BEGIN--")
                for object in world.objects:
                    print(world.objects[object].toString())
                print("Perception -- END --")
                i=i+1

        pyarianne.logout()
    else:
        print("CAN'T CHOOSE: "+pyarianne.errorReason())
    
else:
    print("CAN'T LOGIN: "+pyarianne.errorReason())

print("Finishing pyclient")
    
           

