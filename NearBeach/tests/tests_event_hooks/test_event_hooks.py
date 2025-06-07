from NearBeach import event_hooks
from django.test import TestCase
from unittest import mock



class EventHooksEmitTest(TestCase):
    def setUp(self):
        self._registry = event_hooks.Registry(list)
        self._registry.register_event_type("test", str)
        self._mock = mock.MagicMock()
        self._registry.register_func("test")(self._mock)
        self._patch_print = mock.patch("builtins.print")


    def test_emit_with_valid(self):
        self._registry.emit("test", "test_value")
        self._mock.assert_called_with("test_value")

    def test_emit_with_invalid_type(self):
        with self._patch_print as patched:
            self._registry.emit("test", 1)
        patched.assert_called_once()
        self._mock.assert_not_called()

    def test_emit_with_too_many_types(self):
        with self._patch_print as patched:
            self._registry.emit("test", "test_value", "invalid")
        patched.assert_called_once()
        self._mock.assert_not_called()
