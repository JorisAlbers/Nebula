from ..nebula.config import Config, readConfig
import os

def test_readConfig_file_configIsCorrectlySet():
    #EXPECTED VALUES
    ex_config = Config()
    #General
    ex_config.client_id = "aapnootmies"
    ex_config.isMaster = True
    #Animation
    ex_config.animation_config.resourcePath = "testpath"
    #Networking
    ex_config.networking_config.server_ip = "100.90.80.70"
    ex_config.networking_config.server_port = 1234
    #light
    ex_config.light_config.pwm_pin = 200
    ex_config.light_config.pwm_freq = 10
    ex_config.light_config.dma_channel = 30
    ex_config.light_config.inverse = True
    ex_config.light_config.strip_length = 100
    ex_config.light_config.strip_sections = [[99,0]]
    #web
    ex_config.web_config.port = 9876
    #motion
    #TODO add motion tests

    #LOGIC
    dirname = os.path.dirname(__file__)
    file_name = "config_testfile.json"
    file_path = os.path.join(dirname,file_name)
    config = readConfig(file_path)

    #ASSERTS
    assert(ex_config.client_id == config.client_id)
    assert(ex_config.isMaster == config.isMaster)
    #Animation
    assert(ex_config.animation_config.resourcePath == config.animation_config.resourcePath)
    #Networking
    assert(ex_config.networking_config.server_ip == config.networking_config.server_ip)
    assert(ex_config.networking_config.server_port == config.networking_config.server_port)
    #light
    assert(ex_config.light_config.pwm_pin == config.light_config.pwm_pin)
    assert(ex_config.light_config.pwm_freq == config.light_config.pwm_freq)
    assert(ex_config.light_config.dma_channel == config.light_config.dma_channel)
    assert(ex_config.light_config.inverse == config.light_config.inverse)
    assert(ex_config.light_config.strip_length == config.light_config.strip_length)
    assert(ex_config.light_config.strip_sections == config.light_config.strip_sections)
    #WEB
    assert(ex_config.web_config.port == config.web_config.port)

    # Motion
    #TODO add motion asserts