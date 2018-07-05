import os
import json

class Config:
    client_id = "ring_x"
    isMaster = False

    class web:
        port = 8000

    class animation:
        resourcePath = './../resources'

    class networking:
        server_ip = "localhost"
        server_port = 6000
        
    class light:
        pwm_pin = 18
        pwm_freq = 800000
        dma_channel = 5
        inverse = False
        strip_length = 300
        strip_sections = [[0,299]]

    class motion:
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

def getSettingFromConfigJSON(dic, config_key, setting_key):
    if config_key in dic:
        if setting_key in dic[config_key]:
            return dic[config_key][setting_key]
    print("ConfigReader - failed to load setting {0} from config {1}. Using default value.".format(setting_key,config_key))

def readConfig(path):
    """
    Read the config at file_path
    """
    if not isinstance(path, str):
        raise ValueError("The config path must be a string!")
    if not os.path.isfile(path):
        raise IOError("The config at {0} does not exist.".format(path))

    file_content = None

    try:
        file = open(path,'r')
    except:
        print("Config reader : Failed to config file at {0}".format(path))
        return
    try:
        file_content = file.read()
    except:
        print("Config reader : Failed to read lines, filepath = {0}".format(path))
    finally:
        try:
            file.close()
        except:
            print("Config reader : Failed to close file after reading, filepath = {0}".format(path))

    j = None
    try:
        j =  json.loads(file_content)
    except:
        raise IOError("Config reader : Failed to parse json")

    config = Config()
    # General
    if "client_id" in j:
        config.client_id = j["client_id"]
    else:
        print("ConfigReader - failed to load setting client_id")
    if "isMaster" in j:
        config.isMaster = j["isMaster"]
    else:
        print("ConfigReader - failed to load setting isMaster")

    #WEB
    value = getSettingFromConfigJSON(j,"web","port")
    if value is not None:
        config.web.port = value
    #NETWORKING
    value = getSettingFromConfigJSON(j,"networking","server_ip")
    if value is not None:
        config.networking.server_ip = value
    value = getSettingFromConfigJSON(j,"networking","server_port")
    if value is not None:
        config.networking.server_port = value
    #ANIMATION
    value = getSettingFromConfigJSON(j,"animation","resource_dir")
    if value is not None:
        config.animation.resourcePath = value
    #LIGHT
    value = getSettingFromConfigJSON(j,"light","pwm_pin")
    if value is not None:
        config.light.pwm_pin = value
    value = getSettingFromConfigJSON(j,"light","pwm_freq")
    if value is not None:
        config.light.pwm_freq = value
    value = getSettingFromConfigJSON(j,"light","dma_channel")
    if value is not None:
        config.light.dma_channel = value
    value = getSettingFromConfigJSON(j,"light","strip_length")
    if value is not None:
        config.light.strip_length = value
    value = getSettingFromConfigJSON(j,"light","strip_sections")
    if value is not None:
        config.light.strip_sections = value
    #MOTION
    # TODO parse motion values
    return config


