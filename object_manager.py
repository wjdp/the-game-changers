class ObjectManagerMixin(object):
  objects = []

  def create_object(self, obj, *args, **kwargs):
    """Add an object to current state and returns the instance"""
    new_obj_instance = obj(*args, **kwargs)
    self.objects.append(new_obj_instance)

    if hasattr(self, 'object_super'):
      self.object_super.append_object(new_obj_instance)

    return new_obj_instance

  def add_object(self, inst):
    """Given an object instance, append to object list"""
    self.objects.append(new_obj_instance)

  def delete_object(self, obj):
    """Removes object from current state"""
    obj.destroy()
    self.objects.remove(obj)

  def purge_objects(self):
    """Deletes all objects"""
    for obj in self.objects:
      self.delete_object(obj)

  def tick_objects(self):
    """Run tick function on all objects"""
    for obj in self.objects:
      obj.tick()
