import time

class Sixad:
    self.hidd_number_1 = self.hidd_number_2 = self.hidd_number_3 = self.hidd_number_4 = self.hidd_number_5 = self.hidd_number_6 = self.hidd_number_7 = self.hidd_number_8 = ""
    self.ROOT = "sudo"
    def look4Root(self):
        if not "kdesudo" in self.ROOT and "kdesu" in shared.ROOT: #Fix for openSUSE's kdesu not echoing to terminal (opens separate session for sudo)
            return 1
        elif "YES" in getoutput(self.ROOT+" echo YES"):
            return 1
        else:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Operation not permitted - Not enough rights"))
            return 0

    # Return value: number of found devices
    def func_UpdateBluetoothNames(self):
        self.Check4BluetoothDevices = getoutput("hcitool con")
        self.nOfDevices = 0
        if "ACL" in self.Check4BluetoothDevices:
            self.hidd_number_1 = self.hidd_number_2 = self.hidd_number_3 = self.hidd_number_4 = self.hidd_number_5 = self.hidd_number_6 = self.hidd_number_7 = self.hidd_number_8 = ""
            self.nOfDevices = int(getoutput("echo '"+self.Check4BluetoothDevices+"' | grep ACL -n | tail -n 1 | awk '{printf$1}' | awk 'sub(\":\",\"\")'")) - 1
            if self.nOfDevices > 0: self.hidd_number_1 = getoutput("echo '"+self.Check4BluetoothDevices+"' | head -n 2 | tail -n 1 | awk '{printf$3}'")
            if self.nOfDevices > 1: self.hidd_number_2 = getoutput("echo '"+self.Check4BluetoothDevices+"' | head -n 3 | tail -n 1 | awk '{printf$3}'")
            if self.nOfDevices > 2: self.hidd_number_3 = getoutput("echo '"+self.Check4BluetoothDevices+"' | head -n 4 | tail -n 1 | awk '{printf$3}'")
            if self.nOfDevices > 3: self.hidd_number_4 = getoutput("echo '"+self.Check4BluetoothDevices+"' | head -n 5 | tail -n 1 | awk '{printf$3}'")
            if self.nOfDevices > 4: self.hidd_number_5 = getoutput("echo '"+self.Check4BluetoothDevices+"' | head -n 6 | tail -n 1 | awk '{printf$3}'")
            if self.nOfDevices > 5: self.hidd_number_6 = getoutput("echo '"+self.Check4BluetoothDevices+"' | head -n 7 | tail -n 1 | awk '{printf$3}'")
            if self.nOfDevices > 6: self.hidd_number_7 = getoutput("echo '"+self.Check4BluetoothDevices+"' | head -n 8 | tail -n 1 | awk '{printf$3}'")
            if self.nOfDevices > 7: self.hidd_number_8 = getoutput("echo '"+self.Check4BluetoothDevices+"' | head -n 9 | tail -n 1 | awk '{printf$3}'")
        return self.nOfDevices

    # Parameter: Number of Device(1-8)
    # Return value: battery state of device
    def func_Battery(self, id):
        shared.ROOT = "sudo"
        if (id == 1): self.DeviceToCheck = self.hidd_number_1
        elif (id == 2): self.DeviceToCheck = self.hidd_number_2
        elif (id == 3): self.DeviceToCheck = self.hidd_number_3
        elif (id == 4): self.DeviceToCheck = self.hidd_number_4
        elif (id == 5): self.DeviceToCheck = self.hidd_number_5
        elif (id == 6): self.DeviceToCheck = self.hidd_number_6
        elif (id == 7): self.DeviceToCheck = self.hidd_number_7
        elif (id == 8): self.DeviceToCheck = self.hidd_number_8
        else: print str(self.tr("Device not connected; Cannot check battery"))
        if look4Root(self): self.SixaxisBat = str(getoutput(self.ROOT+" hcidump -R -O '"+self.DeviceToCheck+"' | head -n 5 | tail -n 1 | awk '{printf$1}' & sleep 1 && "+self.ROOT+" killall hcidump > /dev/null"))
        else: self.SixaxisBat = ""
        if self.SixaxisBat.isdigit():
            return int(self.SixaxisBat)
        else:
            if self.SixaxisBat == "EE": self.barBattery.setMaximum(0)
            elif self.SixaxisBat == "HCI": print "Device not connected; Cannot check battery (2)" #(2) - to know what is the exact error
            else: print "Error while trying to check battery"

    def func_GetDevice(self, id):
        if (id == 1): return self.hidd_number_1
        elif (id == 2): return self.hidd_number_2
        elif (id == 3): return self.hidd_number_3
        elif (id == 4): return self.hidd_number_4
        elif (id == 5): return self.hidd_number_5
        elif (id == 6): return self.hidd_number_6
        elif (id == 7): return self.hidd_number_7
        elif (id == 8): return self.hidd_number_8
        else: return -1;

if __name__ == "__main__":
    sixadControl = Sixad()
    
    while True:
        time.sleep(5)
        sixadControl.Check4BluetoothDevices()
        for i in range(1, 8):
            print "Device " + i + " Battery: " + sixadControl.func_Battery(i)