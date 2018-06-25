from nebula.config import animation_config


def test_animation_reader__init__correctPath():
    from ...nebula.animation.animation_reader import AnimationReader

    ar = AnimationReader(animation_config.resourcePath)

    assert ar.succeeded


def test_animation_reader__get_animations__correct_list():
    from ...nebula.animation.animation_reader import AnimationReader
    expected_title = "An animation"
    ar = AnimationReader(animation_config.resourcePath)
    result = ar.get_animations()

    assert result[0] == expected_title