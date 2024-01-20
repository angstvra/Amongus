def heat_danger(rels,tempsc):
    hi = (heat_index(rels,tempsc)-32)*(5/9)
    if hi >=125:
        return "Extreme Danger with Straneous Activities"
    elif hi >= 104:
        return "Danger with Straneous Activities"
    elif hi>= 91:
        return "Extreme Caution with Straneous Activities"
    elif hi >= 80:
        return "Caution with Straneous Activities"
    else:
        return "Relatively Fine Day"

def heat_index(rel,tempc):
    fahrenheit = (tempc*(9/5))+32
    hum = rel
    C1 = [ -42.379, 2.04901523, 10.14333127, -0.22475541, -6.83783e-03, -5.481717e-02, 1.22874e-03, 8.5282e-04, -1.99e-06]
    T2 = pow(fahrenheit, 2)
    T3 = pow(fahrenheit, 3)
    H2 = pow(hum, 2)
    H3 = pow(hum, 3)
    heatindex = C1[0] + (C1[1] * fahrenheit) + (C1[2] * hum) + (C1[3] * fahrenheit * hum) + (C1[4] * T2) + (C1[5] * H2) + (C1[6] * T2 * hum) + (C1[7] * fahrenheit * H2) + (C1[8] * T2 * H2)
    
    return heatindex
    


def rain_advisories(list1):
    try:

        sums = list1[-1]
        if (sums>30):
            return ("RED RAINFALL WARNING,SERIOUS FLOODING EXPECTED IN LOW LYING AREAS")
        elif(sums>15):
            return ("ORANGE RAINFALL WARNING,FLOODING IS THREATINING")
        elif(sums>7.5):
            return ("YELLOW RAINFALL WARNING,FLOODING IS POSSIBLE")
        
        elif(sums>2.5):
            return("Heavy Rain")
        elif(sums>0.25):
            return("Rain")
        elif(sums>0):
            return("Light Rain")
        else:
            return("No Rain")
    except:
        return("ERROR")



beaufort_tup = (1,3,6,10,16,21,
                27,33,40,47,55,63)

def beaufort(ms):
    knots = float(ms)*1.94384
    knots = int(round(knots))
    for i in range(len(beaufort_tup)):
        if knots <= beaufort_tup[i]:
            return i
    return len(beaufort_tup)

beaufort_tup_string = ("Calm, smoke rises vertically",
                    "Smoke drift indicates wind direction, still wind vanes",
                    "Wind felt on face, leaves rustle, vanes begin to move",
                    "Leaves and small twigs constantly moving, light flags extended",
                    "Dust, leaves, and loose paper lifted, small tree branches move",
                    "Small trees in leaf begin to sway",
                    "Larger tree branches moving, whistling in wires",
                    "Whole trees moving, resistance felt walking against wind",
                    "Twigs breaking off trees, generally impedes progress",
                    "Slight structural damage occurs, slate blows off roofs",
                    "Seldom experienced on land, trees broken or uprooted, considerable structural damage",
                    "WIDESPREAD DAMAGE",
                    "VIOLENCE AND DESTRUCTION"
                    )

def advisory_in_beaufort(ms):
    index_string = beaufort(ms)
    try:
        return beaufort_tup_string[index_string]
    except:
        return "ERROR"
    
