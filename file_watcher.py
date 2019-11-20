import pyinotify

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        print("MODIFY event:", event.pathname)

    def process_IN_OPEN(self, event):
        print("OPEN event:", event.pathname)

def main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('./config.tsv', pyinotify.ALL_EVENTS, rec=True)

    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == '__main__':
    main()