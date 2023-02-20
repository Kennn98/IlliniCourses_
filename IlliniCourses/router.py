"""
Django database router for IlliniCourses

For more information about this file, please see:
https://docs.djangoproject.com/en/3.1/topics/db/multi-db/#automatic-database-routing
"""

# create a router that reroute all tag related data to mongodb
class DBRouter(object):
    # db alias
    sql = "default"
    mongo = "mongo"
    # models that should go to mongodb
    mongo_model = set(["Tag", "Taglist", "tag", "taglist", "UserForm", "userform", "User", "user"])
    # also add lower case
    # determine the right database to read
    def db_for_read(self, model, **hints):
        model_name = model.__name__
        #print("read model name", model_name, "lable", model._meta.app_label)
        app_name = model._meta.app_label
        if(model_name in self.mongo_model and app_name == "course"):
            #print("goto mongo")
            return self.mongo
        #print("goto sql")
        return self.sql

    # determine the right database to write
    def db_for_write(self, model, **hints):
        #print("read model name", model_name)
        model_name = model.__name__
        app_name = model._meta.app_label
        if(model_name in self.mongo_model and app_name == "course"):
            #print("goto mongo")
            return self.mongo
        #print("goto sql")
        return self.sql

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        # filter out some model that should not go into mongo
        # data that are allowed to write in mongodb
        #print("migration request", db, app_label)
        if(db == self.mongo):
            if(app_label == "course"):
                if(model_name in self.mongo_model):
                    #print("accept")
                    return True
            #print("deny")
            return False
        elif(db == self.sql):
            if(app_label == "course"):
                if(model_name in self.mongo_model):
                    #print("deny")
                    return False
            #print("accept")
            return True
        #print("accept")
        return True
