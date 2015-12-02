class ObjectManagerMixin(object):

  def __init__(self):
    self.objects = []

  def create_object(self, obj, *args, **kwargs):
    """Add an object to current state and returns the instance"""
    new_obj_instance = obj(*args, **kwargs)
    self.add_object(new_obj_instance)

    if hasattr(self, 'object_super'):
      self.object_super.add_object(new_obj_instance)

    return new_obj_instance

  def add_object(self, inst):
    """Given an object instance, append to object list"""
    self.objects.append(inst)

  def destroy_object(self, obj):
    """Removes object from current state"""
    obj.destroy()

    if hasattr(self, 'object_super'):
      self.object_super.remove_object(obj)

    self.remove_object(obj)

  def remove_object(self, obj):
    """Actually do the removing"""
    # print self.objects, obj
    self.objects.remove(obj)

  def purge_objects(self):
    """Deletes all objects"""
    # Make a copy of objects. This needs doing as looping over a list
    # while removing items from that list causes the for loop to mis-index.
    objects_copy = list(self.objects)
    # print objects_copy
    for obj in objects_copy:
      # print obj
      self.destroy_object(obj)

  def tick_objects(self):
    """Run tick function on all objects"""
    for obj in self.objects:
      obj.tick()
