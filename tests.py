import unittest
from polynomial import Polynomial


class PolynomialTestCase(unittest.TestCase):
    poly1 = Polynomial(1, 2, 3)
    poly2 = Polynomial(4, 5, 6)
    poly3 = Polynomial(-1, -2, -3)
    poly4 = Polynomial(-2, 0, 1)
    poly5 = Polynomial(0, 0, 0)

    def test_addition(self):
        self.assertEqual(self.poly1 + self.poly2, Polynomial(5, 7, 9), msg="увы")
        self.assertEqual(self.poly1 + self.poly3, Polynomial(0, 0, 0), msg="увы")
        self.assertEqual(self.poly1 + self.poly4, Polynomial(-1, 2, 4), msg="увы")
        self.assertEqual(self.poly1 + self.poly5, self.poly1, msg="увы")

    def test_subtraction(self):
        self.assertEqual(self.poly1 - self.poly5, self.poly1, msg="увы")
        self.assertEqual(self.poly1 - self.poly2, Polynomial(-3, -3, -3), msg="увы")
        self.assertEqual(self.poly1 - self.poly3, Polynomial(2, 4, 6), msg="увы")

    def test_unary_minus(self):
        self.assertEqual(-self.poly5, Polynomial(0, 0, 0), msg="увы")
        self.assertEqual(-self.poly1, Polynomial(-1, -2, -3), msg="увы")
        self.assertEqual(-self.poly3, Polynomial(1, 2, 3), msg="увы")

    def test_comparison(self):
        self.assertTrue(self.poly5 == Polynomial(0, 0, 0), msg="увы")
        self.assertTrue(self.poly1 == Polynomial(1, 2, 3), msg="увы")
        self.assertTrue(self.poly1 != Polynomial(3, 2, 1), msg="увы")

    def test_arithmetic(self):
        self.assertEqual(self.poly1 * 2, Polynomial(2, 4, 6), msg="увы")
        self.assertEqual(self.poly4 + 1, Polynomial(-1, 0, 1), msg="увы")
        self.assertEqual(self.poly1 + 1, Polynomial(2, 2, 3), msg="увы")
        self.assertEqual(self.poly2 - 2, Polynomial(2, 5, 6), msg="увы")

    def test_poly_degree(self):
        self.assertEqual(self.poly1.degree(), 2, msg="увы")
        self.assertEqual(self.poly2.degree(), 2, msg="увы")
        self.assertEqual(self.poly4.degree(), 2, msg="увы")
        self.assertEqual(self.poly5.degree(), 0, msg="увы")

    def test_point(self):
        self.assertEqual(self.poly1(1), 6, msg="увы")
        self.assertEqual(self.poly1(2), 17, msg="увы")
        self.assertEqual(self.poly2(2), 38, msg="увы")
        self.assertEqual(self.poly5(2), 0, msg="увы")

    def test_der(self):
        self.assertEqual(self.poly1.der(), Polynomial(2, 6), msg="увы")
        self.assertEqual(self.poly1.der(2), 6, msg="увы")
        self.assertEqual(self.poly4.der(3), Polynomial([]), msg="увы")

    def test_iter_next(self):
        needed = []
        for el in self.poly1:
            needed.append(el)
        self.assertEqual(needed, [(0, 1), (1, 2), (2, 3)], msg="увы")

        needed.clear()
        for el in self.poly2:
            needed.append(el)
        self.assertEqual(needed, [(0, 4), (1, 5), (2, 6)], msg="увы")

        needed.clear()
        for el in self.poly5:
            needed.append(el)
        self.assertEqual(needed, [(0, 0), (1, 0), (2, 0)], msg="увы")
        needed.clear()
