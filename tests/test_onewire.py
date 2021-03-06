import pytest

pytest.importorskip("onewire")

from labgrid.driver import OneWirePIODriver
from labgrid.resource import OneWirePIO

@pytest.fixture(scope='function')
def onewire_port(target):
    return OneWirePIO(target, "pio", "testhost", "path")

@pytest.fixture(scope='function')
def onewire_driver(target, onewire_port, monkeypatch, mocker):
    onewire_mock = mocker.MagicMock
    onewire_mock.set = mocker.MagicMock()
    onewire_mock.get = mocker.MagicMock()
    import onewire
    monkeypatch.setattr(onewire, 'Onewire', onewire_mock)
    s = OneWirePIODriver(target, "pio")
    target.activate(s)
    return s

def test_onewire_resource_instance(target):
    o = OneWirePIO(target, "pio", "testhost", "path")
    assert (isinstance(o, OneWirePIO))

def test_onewire_driver_instance(target, onewire_driver):
    isinstance(onewire_driver, OneWirePIODriver)

def test_onewire_set(onewire_driver):
    onewire_driver.set(True)
    onewire_driver._onewire.set.assert_called_once_with("path", '1')

def test_onewire_unset(onewire_driver):
    onewire_driver.set(False)
    onewire_driver._onewire.set.assert_called_once_with("path", '0')

def test_onewire_get(onewire_driver):
    onewire_driver.get()
    onewire_driver._onewire.get.assert_called_once_with("path")
