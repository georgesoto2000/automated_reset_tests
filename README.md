# automated_reset_tests
An automation script written to test the factory, settings and hard drive reset functions on Sky Q STB using a USB capture card. A settings reset should revert settings to default and not affect the HDD, a hard drive reset should wipe the hard drive but not change the settings and the factory reset should perform both a settings and hard drive reset. The setup for performing this is a USB capture card attached to the device running the script and a smart plug powering the Sky Q box.

Captures are taken using OpenCV and OCR (the engine used is pytesseract wrapper for Google Tesseract) is used on the captures to verify on screen menus (OSMs)
sky-remote.js file is used for RCU emulation (from https://github.com/dalhundal/sky-remote)
