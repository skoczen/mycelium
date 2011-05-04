import random

class MasterSlaveRouter(object):
    """A router that sets up a simple master (called default)/slave configuration"""

    def db_for_read(self, model, **hints):
        "Point all read operations to a random slave"
        # return random.choice(['slave','default'])
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all write operations to the master"
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation between two objects in the db pool"
        # db_list = ('default','slave')
        # if obj1._state.db in db_list and obj2._state.db in db_list:
        #     return True
        # return None
        return True

    def allow_syncdb(self, db, model):
        "Explicitly put all models on all databases."
        return True