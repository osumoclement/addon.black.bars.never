# BlackBarsNever Kodi Addon - Remove black bars
# How it works
This is an addon that eliminates black bars on KODI, whether hardcoded or the video is just wide format

With addon installed and enabled, it will automatically analyze media on playback and determine 
if there are any black bars. The addon will then zoom the media exactly enough to cover the display.

The picture will not be distorted in any way as the zoom is linear,
however, on most media, small parts on the left and right will be cut off. Luckily, everything that's 
important tends to fall in the middle of tbe scene most of the time. The advantages of experiencing an 
immersive picture that fills the periphery should be enough to overweigh the disdvantage of missing sides.

# Supported platforms                          
- [x] Linux
- [x] Windows
- [x] macOS and iOS
- [ ] Android - Partially. Works if hardware acceleration is disabled. A fix may be available in future

# Installation
Download the zip file from [releases](https://github.com/osumoclement/script.black.bars.never/releases)

Launch Kodi >> Add-ons >> Get More >> Install from zip file

Feel free to ask any questions, submit feature/bug reports

# Customization
There are a few ways to customize the addon
By default, the addon automatically removes black bars. If you want to change this behavior, you can turn this off in the addon settings. You would then need to manually trigger the addon by manually calling it from elsewhere in Kodi (ie from a Skin) like this `RunScript(script.black.bars.never,toggle)`. You could even map this to a key for convenience

To check the addon status elsewhere from Kodi, use this `xbmcgui.Window(10000).getProperty('blackbarsnever_status')`. The result is either `on` or `off`

# License
BlackBarsNever is [GPLv2 licensed](https://github.com/osumoclement/script.black.bars.never/blob/main/LICENSE.txt). You may use, distribute and copy it under the license terms.
