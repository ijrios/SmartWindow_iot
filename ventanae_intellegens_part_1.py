from machine import Pin, PWM
 
#------nos initialize initibus et output------
engine_unus = Pin(12, Pin.OUT) #engine
engine_duo = Pin(14, Pin.OUT) #engine
sensorem_carraira_unus = Pin(26,Pin.IN) #finis carraira sensorem unus
sensorem_carraira_duo = Pin(27,Pin.IN) #finis carraira sensorem duo
bottom_dexteram = Pin(32,Pin.IN)
bottom_sinistram = Pin(33,Pin.IN)
bottom_prohibere = Pin(12,Pin.IN)

def deinceps():
    engine_unus.value(1)
    engine_duo.value(0)

def retrorsum():
    engine_unus.value(0)
    engine_duo.value(1)

def main():
    
    while True:
        
        direction_dexteram = 0
        direction_sinistram = 0
        
        if direction_dexteram == 1:
            print("Izquierda")
            finis_while_1 = 0
            
            while(finis_while_1 == 1):
                if bottom_prohibere == 1 and sensorem_carraira_unus == 1:
                    finis_while_1 = 1
                    deinceps()
                    direction_dexteram = 0
        
        if direction_sinistram == 1:
            print("Izquierda")
            finis_while_2 = 0
            while(finis_while_2 == 1):
                if bottom_prohibere == 1 and sensorem_carraira_duo == 1:
                    finis_while_2 = 1
                    retrorsum()
                    direction_sinistram = 0
        
        if bottom_dexteram == 1:
            #Mandamos uno al boton de derecha
            print("Izquierda")
            direction_dexteram = 1
            direction_sinistram = 0
    
        if bottom_sinistram == 1:
            #Mandamos uno al boton de derecha
            direction_dexteram = 0
            direction_sinistram = 1
        
        
if __name__ == '__main__':
    main()




