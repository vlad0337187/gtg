import gi

try:
    gi.require_version('GnomeKeyring', '1.0')
    from gi.repository import GnomeKeyring
except (ImportError, ValueError):
    # ValueError: Namespace GnomeKeyring not available  (on Ubuntu 16.04 / Mint 19)
    GnomeKeyring = None

from GTG.tools.borg import Borg
from GTG.tools.logger import Log


class GNOMEKeyring(Borg):

    def __init__(self):
        super().__init__()
        if not hasattr(self, "keyring"):
            result, self.keyring = GnomeKeyring.get_default_keyring_sync()
            if result != GnomeKeyring.Result.OK:
                raise Exception("Can't get default keyring, error=%s" % result)

    def set_password(self, name, password, userid=""):
        attrs = GnomeKeyring.Attribute.list_new()
        GnomeKeyring.Attribute.list_append_string(attrs, "backend", name)
        result, password_id = GnomeKeyring.item_create_sync(
            self.keyring,
            GnomeKeyring.ItemType.GENERIC_SECRET,
            name,
            attrs,
            password,
            True)

        if result != GnomeKeyring.Result.OK:
            raise Exception("Can't create a new password, error=%s" % result)

        return password_id

    def get_password(self, item_id):
        result, item_info = GnomeKeyring.item_get_info_sync(
            self.keyring, item_id)
        if result == GnomeKeyring.Result.OK:
            return item_info.get_secret()
        else:
            return ""


class FallbackKeyring(Borg):

    def __init__(self):
        super().__init__()
        if not hasattr(self, "keyring"):
            self.keyring = {}
            self.max_key = 1

    def set_password(self, name, password, userid=""):
        """ This implementation does nto need name and userid.
        It is there because of GNOMEKeyring """

        # Find unused key
        while self.max_key in self.keyring:
            self.max_key += 1

        self.keyring[self.max_key] = password
        return self.max_key

    def get_password(self, key):
        return self.keyring.get(key, "")

if GnomeKeyring is not None:
    Keyring = GNOMEKeyring
else:
    Log.info("GNOME keyring was not found, passwords will be not stored after\
                                                              restart of GTG")
    Keyring = FallbackKeyring
