import dbus, dbus.service, dbus.exceptions
import sys

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository.GObject import MainLoop

import notify2
import logging
logging.basicConfig(filename='dbus_keystroke_notifs.log', level=logging.INFO)
logging.info('Started')
# class RandomData(dbus.service.Object):
#     def __init__(self, bus_name):
#         super().__init__(bus_name, "/com/larry_price/test/RandomData")
#         random.seed()

#     @dbus.service.method("com.larry_price.test.RandomData",
#                          in_signature='i', out_signature='s')
#     def quick(self, bits=8):
#         return str(random.getrandbits(bits))

def click_callback(arg1):
    logging.info("click callback called")
    print("lol",arg1)

def finger_callback(finger, obj, uid):
    print(finger, obj, uid)

class DesktopNotification(dbus.service.Object):
    def __init__(self, busname,):
        super().__init__(bus_name, "/com/keystrokes/notif/show")
    
    # @dbus.service.signal("com.larry_price.test.RandomData", signature='ss')
    # def showDesktopNotification(self, thread_id, result):
    #     pass

    # @dbus.service.method("com.keystrokes.notif.show", in_signature='i', out_signature='s')

    @dbus.service.method("com.keystrokes.notif",in_signature='sss', out_signature='i')
    def finger(self, head, desc, uid):
        # open("./ab","wb")
        

        try:
            n = notify2.Notification(head,desc)
            n.add_action("0", "0",finger_callback,uid)
            n.add_action("1", "1",finger_callback,uid)
            n.add_action("2", "2",finger_callback,uid)
            n.add_action("3", "3",finger_callback,uid)
            n.add_action("4", "4",finger_callback,uid)
            n.add_action("5", "5",finger_callback,uid)
            n.add_action("6", "6",finger_callback,uid)
            n.add_action("7", "7",finger_callback,uid)
            n.connect("closed",click_callback)
            n.show()
            return 0
        except:
            return 1

    @dbus.service.method("com.keystrokes.notif",in_signature='sss', out_signature='i')
    def show(self, head, desc, uid):
        # open("./ab","wb")
        

        try:
            n = notify2.Notification(head,desc)
            n.connect("closed",click_callback)
            n.show()
            return 0
        except:
            return 1
    
    @dbus.service.method("com.keystrokes.notif",in_signature='sss', out_signature='i')
    def boolean(self, head, desc, uid):
        # open("./ab","wb")
        

        try:
            n = notify2.Notification(head,desc)
            n.add_action("yes", "Yes",boolean_callback,uid)
            n.add_action("no", "No",boolean_callback,uid)
            n.connect("closed",click_callback)
            n.show()
            return 0
        except:
            return 1
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
