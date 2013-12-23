Super Guitar Solo Effects with Extra Feelings Wow Very Rube Golberg
=====================================================================

So, I'm sure you like guitars, and have a bunch of money laying around you want to burn, but can't think of a good project. You're also a crack programmer,
and want to learn more about things like Arduinos and Wireless programming and Xbees, but at the same time, make some cool stuff you can shred, while also 
converting as much money into microcontrollers as possible.

Well, look no further. You can now make it so that doing cool things like this:

Actually has an effect on the sounds coming out of your guitar.

We do this by hooking up an accelerometer to the headstock of your guitar, and using an Arduino FIO with the XBee v2 to send the data in real time to an X2e
XBee gateway device. This device then tranforms those raw measurements into OSC data to send to your computer, which is wired into your guitar, and has guitar
effects wired up to be controlled by OSC in something like Ableton Live.

Of course, the easiest way to do this would be to figure out a way to velcro a cell phone to your guitar headstock, and then just pump out the raw accelerometer
info to an OSC server. But that's too easy.

So, if you've also got the time to read how [OpenSoundControl](http://opensoundcontrol.org/), XBee v2, i2c, and PureData all work, we should be good. If not,
just wing it, and run into walls like I did.

List of Hardware Requirements
------------------------------

*Arduino FIO v3.0* - I got mine from SparkFun, make sure you take the XBee off when programming it, because otherwise the programmer won't work
*XBee V2* - I used the mesh version of XBee because I plan on having multiple inputs. I got the PRO version because it means I can wirelessly control things from very far away.
*LiPo battery* - I used the biggest one I could find, that was 3.3v 
*ADXL345* - Super precise and fast, and complete overkill, just like every other part of this hack. We'll use it over i2c, because that's supported already. 
*XBee X2e Gateway* - Embedded Linux device that runs a stripped version of Python 2.7. Most OSC libraries are in Python3000 world now, and it took me a while to find 2.7 code. Fun.
*Solder & Header Pins* - There is no right way to wire up header pins on the FIO for breadboard use. Either you can't press the reset button, or you can't easily access the XBee to reprogram.
*FTDI Cable* - Don't worry, I didn't have one of these either. More money to burn through. 

Software Requirements
----------------------

*Ableton Live* - This is just what I used. There's free demo over on their site, it's pretty amazing software.
*PureData Extended* - We'll use this to convert the OSC data coming in via UDP to MIDI, so we can select effects and feelings for different virtual pedals.

Getting Started
----------------

The first thing to do is to solder up the header pins with at least the FTDI pins facing the opposite way as the rest of the pins you solder in. This way, you'll be able to reprogram
it without taking it off your damn breadboard.

Next, wire up Analog 4 (labeled A4 on the FIO) to SDA on the ADXL345 breakout board. Then wire up Analog 5 (again, A5 on the FIO board) to SCL on the ADXL345 breakout. Finally, connect
3v3 on the FIO to the VCC on the ADXL, and GND to GND on the ADXL. 

Congratulations, you're now an Electrical Engineer. 

Before you put on the XBee Pro, try plugging in the FTDI headers and using the code in the accelr/ directory. You should obviously launch and install the Arduino software, and go to 
Tools -> Board -> Arduino Fio before programming. Send the program to the device by clicking the upload button. If everything is wired up properly, you should be able to go to Tools ->
Serial Monitor, set your baud rate to 9600, and see some numbers looking like this:

11:33:00
22:11:00

As you move the breadboard around, you should see those numbers start to change.

Congratulations, you are now an Embedded Developer.

We can now unplug the device from the FTDI cables, plug in our charged LiPo battery (just use the USB cable input to charge it), plug in our XBee, and send wireless signals to the gateway.

You'll need to copy over all the gateway code to the X2e device, and my favorite way of doing that is with scp in the directory of this project. Obviously replace 127.0.0.1 with the IP of 
your X2e:

    $ scp *.py python@127.0.0.1:

Then, you can log in and run the awesome python script that converts the incoming packets to UDP packets to send to your server. Oh wait, you don't have a server, do you?

Run PureData Extended (it's free and runs on everything), press command+1 on Mac (I don't know what it is elsewhere), and type in "import mrpeach". Then command+1 again,
and type in "udpreceive 9000", command+1 again, "unpackOSC", and finally, command+1 "print".

When you're in PureData you'll see some weird looking rectangles on all the boxes you just made. This is used to connect things. When you hover over them, they make circles to connect things.
Connect the bottom left of "udpreceive" to the top left of "unpackOSC", and the bottom left of "unpackOSC" to "print". Press command+e to get out of edit mode and make your OSC server live.

Congratulations, you are now an edgy electronic musician.

Now, open up the file you sent to the X2e and substitute your IP address and port number. If you did "udpreceive 9000" like above, your port number will be... 9000! (Gateway only has vi.
Press i to insert text, when finished hit escape, and then type in ":wq<enter>")

Yes, vim is far inferior to emacs.

One thing remaining, and that's to make sure you're sending everything from end to end. Look at the console in puredata-extended, plug in the battery and switch on your Fio, and log in to
the X2e and run that program! (Probably best in that order)

    $ ssh python@127.0.0.1
    $ python pipeit.py

And that's it! Magic OSC being sent to control... everything!

Congratulations, you are now wizard and can now cast magic missle... effects from your guitar!








