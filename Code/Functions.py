#Functions that are useful for getting the sensor readings
#..............................................Imports needed...................................................................................
import busio
import time
import digitalio
import board 
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO
from gpiozero import LED
#..............................................Initialising Force Sensors to their Power Supplies............................ 
FSR1=LED(12)#the LED function is has a simple OUTPUT functionality that enable gpio pins to turn on/off
FSR2=LED(16)
FSR3=LED(20)
FSR4=LED(21)
FSR5=LED(25)
#...............................................Ensuring all Sensors are off................................................
FSR1.off()
FSR2.off()
FSR3.off()
FSR4.off()
FSR5.off()
#..............................................Initialising the Analog to Digital converter.................................
#*********WARNING********-The initialising of the ADC should not be done inside a function this prevents the too many files error
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
#..............................................Begin...........................................................................
def main():#This function is for testing the functions inside this library
    print("It Works ")
    x=0
    while True:
        if x==1:
            print(round(Resistance_Reading(2)),end =" ")
            print(round(Resistance_Reading(1)))
            print(round(Resistance_Reading(4)),end =" ")
            print(round(Resistance_Reading(3)))
            print(round(Resistance_Reading(5)))
            print("....................................")
            time.sleep(3)
        else:
            print(str(round(Resistance_Reading(3)))+"""""Red"""" Voltage Divider Resistance")
            """"print(str(round(Resistance_Reading(4)))+"Yellow")
            print(str(round(Resistance_Reading(1)))+"Blue",end =" ")"""
            print(str(round(Resistance_Reading(2)))+"""""Green"""" Wheatstone Resistance")
            #print(str(round(Resistance_Reading(5)))+"White blue")
            print(str(ADC_Reading(4))+" Voltage Divider Voltage")
            print(str(ADC_Reading(3))+" Wheattone Resistance")
            print("....................................")
            time.sleep(3)
           """ print(str(mass_reading(3))+"Red",end =" ")
            print(str(mass_reading(4))+"Yellow")
            print(str(mass_reading(1))+"Blue",end =" ")
            print(str(mass_reading(2))+"Green")
            print(str(mass_reading(5))+"White blue")
            print("....................................")
            time.sleep(3)"""
def FSR_off():#ensures that all force sensors are off 
    FSR1.off()
    FSR2.off()
    FSR3.off()
    FSR4.off()
    FSR5.off()

def ADC_Reading(channel_num):#Gets the raw voltage of the specified channel 
    if channel_num==0:
        chan0 = AnalogIn(mcp, MCP.P0)
        voltage1=chan0.voltage
        return voltage1+0.16436
    if channel_num==1:
        chan1 = AnalogIn(mcp, MCP.P1)
        voltage2=chan1.voltage
        return voltage2+0.20947665
    if channel_num==2:
        chan2 = AnalogIn(mcp, MCP.P2)
        voltage3=chan2.voltage
        return voltage3
    if channel_num==3:
        chan3 = AnalogIn(mcp, MCP.P3)
        voltage4=chan3.voltage
        return voltage4
    if channel_num==4:
        chan4 = AnalogIn(mcp, MCP.P4)
        voltage5=chan4.voltage
        return voltage5
    if channel_num==5:
        chan5 = AnalogIn(mcp, MCP.P5)
        voltage6=chan5.voltage
        return voltage6
    if channel_num==6:
        chan6 = AnalogIn(mcp, MCP.P6)
        voltage7=chan6.voltage
        return voltage7
    if channel_num==7:
        chan7 = AnalogIn(mcp, MCP.P7)
        voltage8 = chan7.voltage
        return voltage8

def Resistance_Reading(FSR_num):#Depending on the electrical circuit and the resistors used this will convert the input voltage to the corresponding voltage 
    if FSR_num==1:
        FSR_off()
        FSR1.on()
        L_Voltage=ADC_Reading(0)
        R_Voltage=ADC_Reading(1)
        S_Voltage=ADC_Reading(2)
        WS=R_Voltage-L_Voltage
        Ratio = S_Voltage/(WS+L_Voltage)#The formula to give the resistance for the wheatstone bridge needs to be done in 2 steps to avoid the zero division error
        if Ratio==1:
            print("Hello")
            return 55555555
        WSR=3900*(Ratio-1)**-1
        if WSR>1000000 or Ratio==1 or WSR<0:
            print("what")
            return 55555555
        FSR_off()
        return round(WSR)
    if FSR_num==2:
        FSR_off()
        FSR2.on()
        L_Voltage=ADC_Reading(0)
        R_Voltage=ADC_Reading(1)
        S_Voltage=ADC_Reading(3)
        WS=R_Voltage-L_Voltage
        Ratio = S_Voltage/(WS+L_Voltage)
        if Ratio==1:
            return 55555555
        WSR=3900*(Ratio-1)**-1
        if Ratio==1 or WSR>1000000 or WSR<0:
            return 55555555
        FSR_off()
        return round(WSR)
    if FSR_num==3:
        FSR_off()
        FSR3.on()
        V_known=ADC_Reading(1)
        V_Source=ADC_Reading(4)
        Current=V_known/3900
        if Current==0:
            return 55555555
        VDR=(V_Source-V_known)/Current
        return round(VDR)
    if FSR_num==4:
        FSR_off()
        FSR4.on()
        V_known = ADC_Reading(1)
        V_Source=ADC_Reading(5)
        Current=V_known/3900
        if Current==0:
            return 55555555
        VDR=(V_Source-V_known)/Current
        return round(VDR)
    if FSR_num==5:
        FSR_off()
        FSR5.on()
        V_known=ADC_Reading(1)
        V_Source=ADC_Reading(6)
        Current=V_known/3900
        if Current==0:
            return 55555555
        VDR=(V_Source-V_known)/Current
        return round(VDR)
        
def mass_reading(FSR_num):
    mass= (6*10**(8)*Resistance_Reading(FSR_num)**-1.593)/1000#the resistance to mass function that converts derived from y=6E+8x^-1.593
    return mass
def resistance_array():
    array=[0]*6
    array[1]=Resistance_Reading(1)
    array[2]=Resistance_Reading(2)
    array[3]=Resistance_Reading(3)
    array[4]=Resistance_Reading(4)
    array[5]=Resistance_Reading(5)
    return array

def mass_array():
    array=[0]*6
    array[1]=mass_reading(1)
    array[2]=mass_reading(2)
    array[3]=mass_reading(3)
    array[4]=mass_reading(4)
    array[5]=mass_reading(5)
    return array

if __name__=='__main__':
    main()
    
    