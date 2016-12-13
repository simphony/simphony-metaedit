import unittest
from simphony_metaedit import nodes


class TestNodes(unittest.TestCase):
    def test_traversal(self):
        root = nodes.Root()
        animal = nodes.Concept(name="animal")
        root.children.append(animal)

        dog = nodes.Concept(name="dog")
        cat = nodes.Concept(name="cat")
        horse = nodes.Concept(name="horse")

        animal.children.extend([dog, cat, horse])

        vehicle = nodes.Concept(name="vehicle")
        root.children.append(vehicle)
        truck = nodes.Concept(name="truck")
        car = nodes.Concept(name="car")
        plane = nodes.Concept(name="plane")
        glider = nodes.Concept(name="sailplane")

        plane.children.append(glider)
        vehicle.children.extend([truck, car, plane])

        self.assertEqual(
            [x.name for x in nodes.traverse(root)],
            ['/',
             'animal', 'dog', 'cat', 'horse',
             'vehicle', 'truck', 'car', 'plane', 'sailplane'
             ])
