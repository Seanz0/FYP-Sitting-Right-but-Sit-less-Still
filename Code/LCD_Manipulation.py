import lcd
import time
Sitting_Improve=["","Lean Back on the back rest","Put your hips close to the back rest","Lean to the right now","Lean to the left now","Put yout right leg on top of the left","Put your left leg on top of the right"]
Sitting_Responses=["Good sitting posture","Leaning too Forward. Please seat back","You are slouching, make sure your hips are close to you back rest","You are leaning to the left","You are leaning to the right","Your left leg ontop of the right","Your right leg ontop of the right"]
lcd.lcd_init()
def Split_Print(line_string):
    start=0
    end=5
    char_num=len(line_string)
    remainder=char_num%5
    iterate=round(char_num/5)
    if len(line_string)>5:
        for i in range(iterate):
            print(line_string[start:end])
            if i==iterate-1 and char_num%5>0:
                print(line_string[start+5:end+remainder])
                #you can print twice on different lines if you want to deal with the 16X2 LCD
            start=start+5
            end=end+5
    else:
        print(line_string)




def Position_Print(position):
    global Sitting_Responses
    if position==8:
        print("Not advisable, please sit normally")
        print("Please try leaning on the backrest")
        return True
    else:
        print(position)
        #print(Sitting_Responses[position-1])
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string("Sean",1)
        return False
        
def Sample_Indicate():
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Sampled",1)

def Sample_None():
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Wasup",1)
        

def Position_Time(Pos,Time):
    global Sitting_Improve
    if Time==100:
        #print("You may take a walk to stretch")
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string("Stand",1)
        time.sleep(5)
    else:
        print(Sitting_Improve[Pos-1])
        time.sleep(5)
    
        

    