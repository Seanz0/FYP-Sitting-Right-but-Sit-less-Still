import time
import Functions
import LCD_Manipulation
from collections import Counter
from datetime import datetime
from collections import deque
#.................................................Global Variables.................................................
Sitting_Position=[0]*3
Sitting_Time=100
Limit=20
Sampling_Time=5
Sitting_Counter=0
Posture_Counter=0
Position="none"
def min(a,b):
    if a<= b:
        return a
    else:
        return b 
        
        
def max(a,b):
    if a>=b:
        return a
    else:
        return b

        
def Position_Identifier(FSR):
    #FSR=[0.1,1000,500,0.1,1000] Sort this scenario
    min_ry=min(FSR[3],FSR[4])
    max_ry=max(FSR[3],FSR[4])
    min_bg=min(FSR[1],FSR[2])
    max_bg=max(FSR[1],FSR[2])
    red_yel=max_ry/min_ry
    blu_gre=max_bg/min_bg
    if max_ry<1 and max_bg<1:
        print("Wasup")
        LCD_Manipulation.Sample_None()
        return 6
    if max_ry>1 and max_bg>1:#there is no open circuit so that mean all sensors are detecting weight
        if min_ry<300 and max_ry<300 and min_ry>100:
            if red_yel<1.4:
                if max_bg<1000 and min_bg>=500:
                    if blu_gre<=1.4:
                        #print(".........1")
                        return 1
                    else: 
                        print("Please resit")
                        return "none"
            else:
                print("Legs are crossed")
                return 8
        elif max_ry<100 and min_ry<100 and red_yel<=1.4:
            print("Chair is too low")
            return "none"
        
        elif min_ry<=500 and max_ry<=500 and red_yel<1.4:
           # print(".....................2")
            return 2
    elif FSR[1]<1 and FSR[2]<1 and FSR[3]<1 and FSR[4]<1:
            print("Waiting for someone")
            return "none"
    elif FSR[1]<1 and FSR[2]<1:
        print("Slouching.................3")
        return 3
    if red_yel>1.4 and blu_gre>1.4:
            if FSR[3]<FSR[4] and FSR[1]<FSR[2]:#if FSR(3)<FSR(4) and FSR(1)<FSR(2):
                print("leaning to the left......4")
                return 4
            elif FSR[3]>FSR[4] and FSR[1]>FSR[2]:#elif FSR(3)>FSR(4) and FSR(1)>FSR(2):
                print("leaning to the right.....5")
                return 5
               
    elif FSR[1]>FSR[2] and red_yel>1.4:
        print("Your left foot over the right.........................6")
        return 6
    elif FSR1<FSR[2] and red_yel>1.4:
        print("Your right foot over the left.........................7")
        return 7
    else:
        print("not identified")
        return 8
    
def Sample():
    array=[0]*10
    for i in range(10):
        FSR=Functions.mass_array()
        array[i]= Position_Identifier(FSR)
        time.sleep(0.2)
    occurence_count = Counter(array)
    print("Done")
    LCD_Manipulation.Sample_Indicate()
    Sitting_Position[2]=time.perf_counter()
    return occurence_count.most_common(1)[0][0]
    
    
        
        
def Sample_Controller(Position):
    global Sitting_Position, Limit,Sampling_Time
    if Position==0:
        New_Position=Sample()
        return New_Position    
    elif Position>1 and time.perf_counter()-Sitting_Position[1]>Limit:
        LCD_Manipulation.Position_Time(Position,Limit)
        Sitting_Position[1]=Sitting_Position[1]+Limit/2+5
        return Position
    elif Position==1 and time.perf_counter()-Sitting_Position[0]<Sitting_Time:
        if time.perf_counter()-Sitting_Position[2]>Sampling_Time:#if person is sitting in a good posture count until sitting time limit
            New_Position= Sample()
            return New_Position
        else:
            return Position
            
        
    elif Position>1 and time.perf_counter()-Sitting_Position[1]<Limit:
        if time.perf_counter()-Sitting_Position[2]>Sampling_Time:
            New_Position=Sample()
            print ("Hi there")
            return New_Position
        else:
            return Position
        
        
        
        
        
try:
    def run_main():
        global Overall_Sitting_Time,Position,Sitting_Counter
        if Position=="none":#Waiting for someone to sit on the chair
            Position=Sample_Controller(0)
            time.sleep(1)
        else:#Someone Set on the chair
            if Sitting_Position[0]==0:#beginning of the posture system
                Sitting_Position[0]=time.perf_counter()
                #Position=Sample_Controller(0)//Please Redo 1 after all the tests
                Position_Status=LCD_Manipulation.Position_Print(Position)#LCD_Manipulation ......Make a function that is activated by position
                if Position_Status==True:
                    time.sleep(2)
                    if Position==Sample_Controller(0):#When argument is zero, the controller acts as a normal sample
                        Sitting_Position[1]=time.perf_counter()
                    else:
                        Position=Sample_Controller(0)
                        Sitting_Position[1]= time.perf_counter()
                elif Position_Status==False:
                    Sitting_Position[1]=time.perf_counter()
                    
            else:#Not the beginning of the posture system
                if Position!=Sample_Controller(Position):#Sample checks if time is enough to sample again
                    Position=Sample_Controller(Position)
                    LCD_Manipulation.Position_Print(Position)
                    Sitting_Position[1]=time.perf_counter()
                if time.perf_counter()-Sitting_Position[0]>Sitting_Time:
                    LCD_Manipulation.Position_Time(Position,Sitting_Time)#LCD_Manipulation/this has to be done before any change of Position
                    if Sample_Controller==("none"):
                        Sitting_Position[0]=0
                    else:
                        Sitting_Position[0]=Sitting_Position[0]+Sitting_Time/2+5
                
        
    while True:
        run_main()
except KeyboardInterrupt:
    pass