# Beep At Me

**Warning: Early prototype / testing! Use at your own risk**

Plays an audio file in your browser so you can passively monitor a print with a browser window minimized, and receive an audio notice on print completion.

Somewhat ironically, the default audio file isn't a beep.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/ntoff/OctoPrint-Beepatme/archive/master.zip

## Configuration

* Audio volume level 0 - 100% is pretty self explanatory
* Audo file path is the fully qualified path to an audio file, must be reachable and loadable from the URL bar in your browser, not all browsers support all file formats and anything prefixed with `file:///` most likely won't work.