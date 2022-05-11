# Running the project
This project should be run on a Raspberry Pi. Most of the code was left commented in order to be able to troubleshoot this on a Windows 10 environment, but nonetheless, most
functions in these files require a Raspberry Pi to run them (because of GPIO amongst other things).

The file where all the magic happens is `finaldash.py`. If you want to test other files individually, they should have a `main` function inside of them, but `finaldash.py`
contains the dashboard code. Please keep in mind that you need to have [Mosquitto](https://mosquitto.org/download/) downloaded and installed in order to run this dashboard.

Finally, please make sure that you have the libraries defined in all the files installed, which include `dash` and its co-dependencies.

# Warnings
- I take no responsibility and cannot be held liable for any damage caused to your device(s) running this code. 
- This code is provided "as-is", you are free to re-use it without crediting me.
- Please make sure that you follow the above instructions, else the dashboard will fail to load
- Do not ask me to help you debug this. I know that it's broken but have no further plans to continue development.
