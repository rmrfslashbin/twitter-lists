import os
from pathlib import Path
import json

settingsDict = {
    "consumer": {
        "key": None,
        "secret": None
    },
    "access": {
        "token": None,
        "secret": None
    },
    "owner": {
        "accountName": None,
        "id": None
    }
}

class Settings:
    def __init__(self, cfgFile="./settings.json"):
        try:
            self.path = Path(os.environ["SETTINGS"])
        except KeyError:
            self.path = Path(cfgFile)
        except BaseException:
            raise
        except:
            raise

    def create(self):
        self.path.touch()
        return True

    def load(self):
        if not self.path.resolve().exists():
            self.create()
            return settingsDict
        settingsSource = self.path.resolve()

        with settingsSource.open() as f:
            try:
                self.settings = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                self.settings = settingsDict

        return self.settings

    def save(self, settings):
        self.path.resolve().exists()

        settingsSource = self.path.resolve()

        with settingsSource.open("w") as f:
            f.write(
                json.dumps(
                    settings,
                    sort_keys=True,
                    indent=2,
                    separators=(',', ': ')
                )
            )
        return True
