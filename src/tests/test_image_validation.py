import pytest


@pytest.mark.image_validation
def test_home_has_no_broken_images(home_page):
    broken_images = home_page.find_broken_images()
    assert not broken_images, f"Broken images found: {broken_images}"
