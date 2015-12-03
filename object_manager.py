class ObjectManagerMixin(object):
  """Provides a mechanism for managing objects owned by the class. Passes
  created and destroyed objects to a 'parent class' so it can keep track too"""

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

  def purge_objects(self, by_type=None):
    """Deletes all objects, optionally only delete objects of a certain type"""
    if by_type:
      # If type specified, filter the object list by this type
      objects_to_purge = filter(
        lambda obj: isinstance(obj, by_type), self.objects
      )
    else:
      # Make a copy of objects. This needs doing as looping over a list
      # while removing items from that list causes the for loop to mis-index.
      objects_to_purge = list(self.objects)

    for obj in objects_to_purge:
      self.destroy_object(obj)

  def tick_objects(self):
    """Run tick function on all objects"""
    for obj in self.objects:
      obj.tick()
