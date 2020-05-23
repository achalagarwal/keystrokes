import dbus, dbus.service, dbus.exceptions
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository.GObject import MainLoop

import notify2

# class RandomData(dbus.service.Object):
#     def __init__(self, bus_name):
#         super().__init__(bus_name, "/com/larry_price/test/RandomData")
#         random.seed()

#     @dbus.service.method("com.larry_price.test.RandomData",
#                          in_signature='i', out_signature='s')
#     def quick(self, bits=8):
#         return str(random.getrandbits(bits))

class DesktopNotification(dbus.service.Object):
    def __init__(self, busname,):
        super().__init__(bus_name, "/com/keystrokes/notif/show")
    
    # @dbus.service.signal("com.larry_price.test.RandomData", signature='ss')
    # def showDesktopNotification(self, thread_id, result):
    #     pass
    
    @dbus.service.method("com.keystrokes.notif.show", )
    # @dbus.service.method("com.keystrokes.notif.show", in_signature='i', out_signature='s')
    def showDesktopNotification(self, head, desc):
        # open("./ab","wb")
        

        try:
            n = notify2.Notification("Heading","Body with all the details")
            n.show()
            return True
        except:
            return False

# Initialize a main loop
dbusLoop = DBusGMainLoop(set_as_default=True)
notify2.init("keystrokes",dbusLoop)

loop = MainLoop()

# Declare a name where our service can be reached
try:
    bus_name = dbus.service.BusName("com.keystrokes.notifs",
                                    bus=dbus.SessionBus(),
                                    do_not_queue=True)
    DesktopNotification(bus_name)
except dbus.exceptions.NameExistsException:
    print("service is already running")
    sys.exit(1)

# Run the loop
try:
    loop.run()
except KeyboardInterrupt:
    print("keyboard interrupt received")
except Exception as e:
    print("Unexpected exception occurred: '{}'".format(str(e)))
finally:
    loop.quit()

# dbus.set_default_main_loop(dbus.mainloop.NativeMainLoop())
# from dbus.mainloop import NativeMainLoop



# n = notify2.Notification("Heading","Body with all the details")
# def click_callback(a,b,c):
#     print(a)
#     print(b)
#     print(c)
#     n = notify2.Notification('None','None')
#     n.show()
#     # print("asd")
# n.add_action("p", "Send anyways",click_callback,"User clicked ")
# # n.add_action("", "Send anyways",click_callback,"User clicked ")
# # n.connect("closed",print_callback)

# n.show()

# MainLoop().run()
