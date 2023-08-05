from unittest import TestCase

from asm_6502 import Assembler


class TestAssembleLAS(TestCase):

    def setUp(self) -> None:
        self.assembler = Assembler()

    def test_las_absolute_y(self):
        code = "LAS $ABCD,Y"
        results = self.assembler.assemble(code, add_entry=False)
        self.assertEqual([
            (0x0000, [0xBB, 0xCD, 0xAB]),
        ], results)
