# run.py    written by Duncan Murray 3/4/2015

import os
import planet
import view_world

fldr = os.getcwd() + os.sep + 'data'  + os.sep + 'worlds' 


def main():
    """
    test program for VAIS.
    Generates several planets and populates with animals and plants.
    Then places objects and tests the sequences.
    """
    print("|---------------------------------------------------")
    print("|          Virtual AI Simulator")
    print("|---------------------------------------------------")
    print("| ")
    print("| r = rebuild planets")
    
    print("| q = quit")
    print("| ")
    
    planets = load_planet_list()
    show_planet_shortlist(planets)
    print("|---------------------------------------------------")
    cmd = input('| Enter choice ?' )
    if cmd == 'r':
        rebuild_planet_samples()
    elif cmd == 'q':
        exit(0)
    elif cmd < str(len(planets)+1) and cmd > '0':
        fname = planets[int(cmd) - 1]['name'] + '.txt'
        print('viewing planet ' + fname)
        view_world.display_map(fldr + os.sep + fname)
    else:
        print('invalid command ' + cmd)
    

def load_planet_list():
    """
    load the list of prebuilt planets
    """
    planet_list = []
    with open(fldr + os.sep + 'planet_samples.csv') as f:
        hdr = f.readline()
        for line in f:
            #print("Building ", line)
            name, num_seeds, width, height, wind, rain, sun, lava = parse_planet_row(line)
            planet_list.append({'name':name, 'num_seeds':num_seeds, 'width':width, 'height':height, 'wind':wind, 'rain':rain, 'sun':sun, 'lava':lava})
    return planet_list

def show_planet_shortlist(planets):
    """

    """
    for num, p in enumerate(planets):
        txt = p['name'].ljust(15) + str(p['width']).rjust(5) + ' x ' + str(p['height']).ljust(5) 
        print('| ' + str(num+1) + " = view planet " + txt)
        
        
def rebuild_planet_samples():
    planets = []
    with open(fldr + os.sep + 'planet_samples.csv') as f:
        hdr = f.readline()
        for line in f:
            print("Building ", line)
            name, num_seeds, width, height, wind, rain, sun, lava = parse_planet_row(line)
            p = planet.Planet(name, num_seeds, width, height, wind, rain, sun, lava)
            p.evolve(100)
            print(p)
            planets.append(p)

def parse_planet_row(line):          
    row = line.split(',')
    name = row[0]
    num_seeds = int(row[1])
    width = int(row[2])
    height = int(row[3])
    wind = float(row[4])
    rain = float(row[5])
    sun = float(row[6])
    lava = float(row[7])

    return name, num_seeds, width, height, wind, rain, sun, lava
    
    
if __name__ == '__main__':
    main()    
 