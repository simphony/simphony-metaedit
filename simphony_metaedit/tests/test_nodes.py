import unittest
from simphony_metaedit import nodes


class TestNodes(unittest.TestCase):
    def test_traversal(self):
        root = nodes.RootNode()
        animal = nodes.EntryNode(name="animal")
        root.children.append(animal)

        dog = nodes.EntryNode(name="dog")
        cat = nodes.EntryNode(name="cat")
        horse = nodes.EntryNode(name="horse")

        animal.children.extend([dog, cat, horse])

        vehicle = nodes.EntryNode(name="vehicle")
        root.children.append(vehicle)
        truck = nodes.EntryNode(name="truck")
        car = nodes.EntryNode(name="car")
        plane = nodes.EntryNode(name="plane")
        glider = nodes.EntryNode(name="sailplane")

        plane.children.append(glider)
        vehicle.children.extend([truck, car, plane])

        self.assertEqual(
            [x.name for x in nodes.traverse(root)],
            ['/',
             'animal', 'dog', 'cat', 'horse',
             'vehicle', 'truck', 'car', 'plane', 'sailplane'
             ])
