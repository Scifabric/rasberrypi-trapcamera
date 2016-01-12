[![Build Status](https://travis-ci.org/PyBossa/rasberrypi-trapcamera.svg)](https://travis-ci.org/PyBossa/rasberrypi-trapcamera) [![Coverage Status](https://coveralls.io/repos/PyBossa/rasberrypi-trapcamera/badge.svg?branch=master&service=github)](https://coveralls.io/github/PyBossa/rasberrypi-trapcamera?branch=master)
# A PyBossa command line tool for Raspberry PI camera

This command line tool allows you to use a Raspberry PI camera in a 
citizen science project without having to hack or code anything.

The camera can be configured via Rasberry tools, and then all you
have to do is to set a cron job to take pictures at regular times
(i.e. every 10 minutes) to capture an image, upload it to Flickr, and
create a PyBossa task.

The goal is to analyze with the crowd the images that are being captured
by your camera almost in real time, as as soon as the images are captured
they are uploaded and shared via a PyBossa server.

## Install

You can install it using *pip*:

```bash

pip install pybossa-raspberry-trapcamera

```

Then, you should have a new command line tool named: trapcamera.

**NOTE**: you can install it in the system, or if you prefer in a virtual environment.

## Configuration

Trapcamera command line tool can be used with a configuration file. This basically 
allows you to avoid to write all options in the prompt. In this repository you can
find a template with the available options.

Copy the file to your home folder and name it like this: *.trapcamera.cfg*. Then modify
its fields accordingly.

Trapcamera uses Flickr and PyBossa to store the photos and create the tasks respectively.

### Creating a Flickr web app

Before moving forward, go to [https://www.flickr.com/services/apps/create/](https://www.flickr.com/services/apps/create/) and create a Flickr app. This will give you the API key
as well as the secret that you will. Once you have it, just open your config file and
search for the *[flickr]* section, and add your credentials there.

### Choosing a license for your photos

Flickr provides several licenses for your photos. Each license has an ID. By default
trapcamera uses a CC-BY license, but you can change it. If you want to change it, just
use the ID of the license that you want. You can find a list of licenses and its IDs 
[here](https://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html).

### Data storage

By default, trapcamera will create two folders:

 * offline: for storing the images and tasks that were not possible to create because there was no Internet connection.
 * images: where the captured images will be stored while they're uploaded to Flickr.

You can change the location if you want, so check the *[data]* section and adapt it to
your needs.

**NOTE**: Images will be deleted once they're uploaded to Flickr, as you'll have a full
copy of the original photo in the service. This is done to avoid filling the Raspberry PI
memory.

### Creating a PyBossa project

Once you have the data, the pictures, you'll want to analyze them. In this case we'll
use our PyBossa technology. In order to use PyBossa you'll need a PyBossa account and a project.

If you don't have a PyBossa server, you can always use our hosted server: [http://crowdcrafting.org](http://crowdcrafting.org). Just head to the server, sign up, create a project and get its ID (check the project config section). Then get your API key (from your account) and add
those credentials to the config file. You will do that in the *[pybossa]* section. Be sure
to use the proper PyBossa server in the endpoint, otherwise it will not work.

## Testing it

Before moving ahead, you'll need to enable your Raspberry Pi Camera. To do it, just
run this command in your raspberry Pi:

```bash
sudo raspi-config
```

Follow the screen instructions. Reboot the Raspberry Pi once you've finished. Now you
are ready to use the tool.

To test it, just run the following command:

```bash
trapcamera capture
```
If everything goes well, you'll get a photo :-) The command returns the name of the
picture. Open it, and check it. If you see a rocket, then, something went wrong. Check
the camera and be sure that it's properly connected.

### Authenticating trapcamera with Flickr

Well, now you can capture pictures, so let's upload them to Flickr. To do this step
we'll need to authenticate ourselves in Flickr. For doing this step, just run the following
command:

```bash
trapcamera authenticate
```

That should launch your Raspberry Pi web browser. It will ask you permissions to upload
photos. Go ahead, say yes, and close the window. This will leave a token in your Raspberry Pi
that will authenticate all the Flickr API calls. If you didn't get any error, now you should be able to upload the previous picture with this command:

```bash
trapcamera upload --photofile images/uuid.jpg
```

The command should upload the photo and delete the local copy. Go to your Flickr account. There, you should see the picture and album with your photo. If this is working, then we can move to the next step and start analysing them.


### Creating PyBossa tasks: image pattern recognition

Now that you can capture and upload photos, it's time to create tasks. You can do all these çsteps with one single command:

```
trapcamera capture_upload_task
```

That will capture a picture, upload it to Flickr, delete your local copy to free space, and
create a task in your PyBossa server. The command will return the Task ID so you can access it
directly in your project.

To analyze the images we recommend you to use the Image Pattern Recognition template.

# Copyright / License

Copyright (C) 2016 [SciFabric LTD](http://scifabric.com).

License: see LICENSE file.
