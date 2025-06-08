from pathlib import Path

from app import get_image_path

def test_default_config_generation(tmp_path):
    from app import load_config
    cfg_path = tmp_path / 'test_config.yaml'
    config = load_config(cfg_path)

    assert cfg_path.exists()
    assert 'location' in config
    assert config['location'] == 'Factory'


def test_image_path_fallback():
    fake_id = 9999
    fallback_path = Path(__file__).parent.parent / 'assets' / 'default.png'

    assert fallback_path.exists(), 'Default fallback image missing'
    assert get_image_path(fake_id) == 'assets/default.png'
