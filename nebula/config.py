class web_config:
    port = 8000


class led_config:
    leds = []


class motion_config:
    # Controller settings
    pwm_pin = 18
    dir_pin = 6
    maximum_rpm = 80
    pwm_freq_in_hertz = 20000
    pwm_max_dutycycle = 100

    # Watcher settings
    pulses_per_rotation = 16
    reduction = 100
    hall_sensor_a = 5
    hall_sensor_b = 17
    hall_sensor_c = 27
