from framework.db import models
from framework.lib.general import cprint
import os


class ConfigDB(object):
    def __init__(self, Core):
        self.Core = Core
        self.ConfigDBSession = self.Core.DB.CreateScopedSession(os.path.expanduser(self.Core.Config.FrameworkConfigGet("CONFIG_DB_PATH")), models.GeneralBase)
        self.LoadConfigDBFromFile(self.Core.Config.FrameworkConfigGet('DEFAULT_GENERAL_PROFILE'))

    def LoadConfigDBFromFile(self, file_path):
        cprint("Loading Configuration from: " + file_path + " ..")
        configuration = self.GetConfigurationFromFile(file_path)
        # configuration = [(key, value), (key, value),]
        session = self.ConfigDBSession()
        for key, value in configuration:
            session.add(models.ConfigSetting(key = key, value = value))
        session.commit()
        session.close()

    def GetConfigurationFromFile(self, config_file):
        configuration = []
        ConfigFile = open(config_file, 'r').read().splitlines() # To remove stupid '\n' at the end
        for line in ConfigFile:
            if not line or '#' == line[0]: continue
            try:
                key, value = line.split(":", 1)
                key, value = key.strip(), value.strip()
                configuration.append((key, value))
            except ValueError:
                cprint("Invalid configuration line")
        return configuration

    def Get(self, Key):
        session = self.ConfigDBSession()
        obj = session.query(models.ConfigSetting).get(Key)
        session.close()
        if obj:
            return(obj.value)
        return(None)
