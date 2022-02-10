# automated_reset_tests
An automation script written to test the factory, settings and hard drive reset functions on Sky Q STB using a USB capture card. The default transponder test checks that changing tuner frequency disrupts the AV signal. Details of reset tests can be found in this repository as flow diagrams.

Captures are taken using OpenCV and OCR (the engine used is pytesseract wrapper for Google Tesseract) is used on the captures to verify on screen menus (OSMs).
sky-remote.js file is used for RCU emulation (from https://github.com/dalhundal/sky-remote)

sky.py has the defined classes and reset_tests.py contain the test functions.
