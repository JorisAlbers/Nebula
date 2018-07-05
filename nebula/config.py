class config:
    class web_config:
        port = 8000


    class animation_config:
        resourcePath = './../resources'
        
    class led_config:
        pwm_pin = 18
        pwm_freq = 800000
        dma_channel = 5
        inverse = False
        strip_length = 300
        strip_sections = [[0,299]]



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
