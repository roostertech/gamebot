from com.dtmilano.android.viewclient import ViewClient


device, serialno = ViewClient.connectToDeviceOrExit(verbose=True, serialno='34eda071')
device.takeSnapshot().save('training/scenes/map/map3.png', 'PNG')

# device.takeSnapshot().save('training/scenes/load.png', 'PNG')
