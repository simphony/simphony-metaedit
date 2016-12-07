from traits.api import HasTraits, Str, List, This


class EntryNode(HasTraits):
    name = Str('<unknown>')
    path = Str('<unknown>')
    children = List(This)


class FileNode(HasTraits):
    name = Str('<unknown>')
    path = Str('/')
    children = List(EntryNode)


class RootNode(HasTraits):
    name = Str("/")
    path = Str('/')
    children = List(FileNode)
