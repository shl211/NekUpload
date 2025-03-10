class SettingsManager:
    def __init__(self,token,database_url):
        self.token = token
        self.database_target = database_url

    def update_api_key(self,token):
        self.token = token

    def update_db_url(self,database_target):
        self.database_target = database_target
