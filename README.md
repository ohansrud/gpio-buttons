# GPIO-Buttons
Systemd service to handle GPIO button events on the Raspberry Pi.

## References

<https://pypi.python.org/pypi/RPi.GPIO>


## Requirements
        python-rpi.gpio

## Install

Copy gpio-buttons.py to /usr/local/sbin/
Set chmod +x and chmod to root

Copy gpio-buttons.service to /etc/systemd/system/

        $ sudo systemctl daemon-reload
        $ sudo systemctl enable gpio_buttons.service //Set autostart on boot
        $ sudo systemctl start gpio_buttons.service
        $ sudo systemctl status gpio_buttons.service //Check that service runs
