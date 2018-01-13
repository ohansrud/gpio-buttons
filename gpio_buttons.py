#!/usr/bin/python -u
import RPi.GPIO as GPIO
import os
from time   import sleep
from timeit import default_timer as timer

print('Starting ' + __file__ )

try:
    CH_RESET = 17   # system restart / poweroff
    CH_BUTTON1 = 22 # kodi restart / stop
    CH_BUTTON2 = 27 # unassigned

    BTN_PRESS_SHORT = 2
    BTN_PRESS_LONG = 5

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(CH_RESET,   GPIO.IN)
    GPIO.setup(CH_BUTTON1, GPIO.IN)
    GPIO.setup(CH_BUTTON2, GPIO.IN)

    def button_duration(channel):
        start = timer()

        while GPIO.input(channel) == GPIO.HIGH:
            sleep(0.01)

        end = timer()
        elapsed = end - start

        print('channel=[%s], elapsed=[%0.3f]'% (channel, elapsed))

        return elapsed

    # button will restart / poweroff system
    def callback_reset(channel):
        GPIO.remove_event_detect(channel)

        print('reset-Edge detected on channel %s'%channel)

        elapsed = button_duration(channel)

        if elapsed < BTN_PRESS_LONG:
            print('reboot')
            os.system("reboot")

        elif elapsed >= BTN_PRESS_LONG:
            print('poweroff')
            os.system("poweroff")

        else:
            print('ERROR elapsed=[%s]'% elasped)

        GPIO.add_event_detect(CH_RESET,   GPIO.RISING, callback=callback_reset,   bouncetime=300)

    # button will restart / stop kodi
    def callback_button1(channel):
        print('1-Edge detected on channel %s'%channel)
        GPIO.remove_event_detect(channel)

        print('reset-Edge detected on channel %s'%channel)

        elapsed = button_duration(channel)

        if elapsed < BTN_PRESS_SHORT:
            print('restart KODI')
            os.system("./usr/local/sbin/gpio_buttons_kodi restart")

        elif elapsed >= BTN_PRESS_SHORT:
            print('stop KODI')
            os.system("./usr/local/sbin/gpio_buttons_kodi stop")

        else:
            print('ERROR elapsed=[%s]'% elasped)

        GPIO.add_event_detect(CH_BUTTON1, GPIO.RISING, callback=callback_button1, bouncetime=300)

    # spare button action for future use
    def callback_button2(channel):
        print('Edge detected on channel %s'%channel)
        GPIO.remove_event_detect(channel)

        elapsed = button_duration(channel)

        if elapsed < BTN_PRESS_SHORT:
            print('button2 < BTN_PRESS_SHORT')

        elif elapsed >= BTN_PRESS_SHORT:
            print('button2 >= BTN_PRESS_SHORT')

        else:
            print('ERROR elapsed=[%s]'% elasped)

        GPIO.add_event_detect(CH_BUTTON2, GPIO.RISING, callback=callback_button2, bouncetime=300)

    GPIO.add_event_detect(CH_RESET,   GPIO.RISING, callback=callback_reset,   bouncetime=300)
    GPIO.add_event_detect(CH_BUTTON1, GPIO.RISING, callback=callback_button1, bouncetime=300)
    #GPIO.add_event_detect(CH_BUTTON2, GPIO.RISING, callback=callback_button2, bouncetime=300)

    while True:
        sleep(10)

except KeyboardInterrupt:
    print('Program terminated nicely.')
finally:
    GPIO.cleanup() # Clean up regardless of how the try: block was terminated.
