from cursor import Database


def initialize_once():

    if Database().is_table_available('auth',keep_alive=True):
        return None
    else:
        master_key = Database().initialize()
        return master_key
