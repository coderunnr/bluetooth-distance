from bt_proximity import BluetoothRSSI
import time
import sys
import math
import bluetooth

NUM_LOOP = 30

nearby_devices = bluetooth.discover_devices(
        duration=10, lookup_names=True)

def main():

    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        try:
            print("  %s - %s" % (addr, name))
        except UnicodeEncodeError:
            print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))

    for addr, name in nearby_devices:
        btrssi = BluetoothRSSI(addr=addr)
        
        n=1.5    #Path loss exponent(n) = 1.5
        c = 10   #Environment constant(C) = 10
        A0 = 2   #Average RSSI value at d0
        count = 0
        total_dist = 0
        
        for i in range(1, NUM_LOOP):
            rssi = btrssi.get_rssi()
            if rssi is None:
                continue    
            rssi_bt = float(rssi)
            if(rssi_bt!=0 and i>10):                    #reduces initial false values of RSSI using initial delay of 10sec
                count=count+1
                x = float((rssi_bt-A0)/(-10*n))         #Log Normal Shadowing Model considering d0 =1m where  
                distance = (math.pow(10,x) * 100) + c
                total_dist += distance
                print "Approximate Distance:" + name + str(distance)
                print "RSSI: " + str(rssi_bt)
                time.sleep(.2)
        if count is 0:
            count = 1
        avg_distance = total_dist / count
        print "%s %s %s" % (addr, name, str(avg_distance))




if __name__ == '__main__':
    main()

