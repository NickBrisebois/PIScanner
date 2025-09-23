Scanner client to run on Raspberry Pi Zero 2W

Right now this just stores the scanned images to /tmp so you'll need to
pull those off the device via USB or network. The plan is to send them
to a separate server in the future to render as a 3D model.

Dependencies:
-------------
```
python3.11
libgl1-mesa-glx
systemd
make (optional)
```

Installing
----------
`sudo python ./install.py`
or
`sudo make install`
