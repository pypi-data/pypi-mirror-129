<h1 align="center">Facebook Album Downloader - FAD</h1>
<a href="#">
  <div align="center">
    <img src="./media/fad.svg" alt="logo" />
  </div>
</a>
<h3 align="center">Download all photos of an album with one-line command</h3>

<hr>

<p align="center">
  A command-line interface application that you can use to download an album
  (of a page, a group or an user) from Facebook (on new version since Sep 2020)
</p>

<hr>

<h3 align="center">Completely FREE for all purposes</h3>

<hr>

### :sparkles: Features
- **:rocket: Fast**: You can download an facebook album of 500 photos in 8 
minutes. If you have a stable network, you can reduce the timeout option to make
it run faster.
- **:package: Minimal**: FAD runs on Firefox driver in Headless mode (without
GUI). In terms of memory and CPU utilizatioon, Firefox is far better and
utilizes few resources compare with Chromium browsers.
- **:beers: Easy To Use**: FAD read its arguments from the command line. If you
are not familiar with CLI (command-line interface), you can create a JSON
configuration file. You can use FAD without programming knowledge.

<hr>

### :wrench: Installation

###### Prerequisites
- Install Python 3.9+
- Download latest [geckodriver](https://github.com/mozilla/geckodriver/releases)
from the releases page (Linux, MacOS & Windows) and extract excecutable file to
`$HOME/.local/bin/geckodriver` (on Windows File Explorer, create a directory named
`.local.`, with a dot at the end of the directory's name)

###### Install FAD
To install Facebook Album Downloader (FAD), run the following command in your
terminal emulator:

```bash
pip install facebook-album-downloader
```

If you want to see the scraper works on the browser (Debug Mode is enabled), you
have to install Firefox browser.

To **completely remove** FAD, just remove Python (if you want) and remove 
executable file. Finally, run the following command to uninstall FAD:

```bash
pip uninstall facebook-album-downloader
```

<hr>

### :camera_flash: Usage
You can run FAD script from command line or use a configuration file formatted
in JSON.

<br>

**Method 1**: Download an album with a simple command

Run `fad -h` and follow the message to add your download options.

<br>

**Method 2**: Use a configuration file

The default configuration file located `$HOME/.config/fad/config.json`, you can
edit this file to add your download options and run `fad` to use the default 
configuration file.

If you want to use a *external* configuration file, run 
`fad -C <path_to_config_file>`.

<hr>

### :page_facing_up: FAQ

**1. Can FAD download videos?**

The answer is NO.

FAD uses Selenium & Python to crawl photos. And it only accepts the url of an 
album of photos.

**2. What is an facebook album URL?**

An facebook album is a HTML page that contains a grid of photos.

**3. How to get url of an album?**

To get the url of an album, watch this Youtube video and follow the instructions.

**4. Will I paid for a premium plan or something to use FAD in the future?**

NO and NEVER. This application is completely free to use. I'm gonna take it to
Open Source Community to easy for developers who contribute to this project.

<hr>

### :memo: License
Copyright © 2021, Allan Wu

This project is [GNU GPL v3](https://github.com/wuallanx/facebook-album-downloader/blob/main/LICENSE)license.

<hr>

### :globe_with_meridians: Contact
- Author: Allan Wu (Dang Minh Ngo)
- Email: wuallanx@gmail.com
- Github: https://github.com/wuallanx
