class TestMultiply(TestCase):
    def test_both_positive(self):
        a, b = 4, 2
        answer = 8
        self.assertEqual(multiply(a, b), answer)

    def test_both_negative(self):
        a, b = -4, -2
        answer = 8
        self.assertEqual(multiply(a, b), answer)

    def test_first_positive(self):
        a, b = 4, -2
        answer = -8
        self.assertEqual(multiply(a, b), answer)

    def test_second_positive(self):
        a, b = -4, 2
        answer = -8
        self.assertEqual(multiply(a, b), answer)

    def test_first_float(self):
        a, b = 4.3, 3
        answer = 12.9
        self.assertEqual(multiply(a, b), answer)

    def test_second_float(self):
        a, b = 3, 4.3
        answer = 12.9
        self.assertEqual(multiply(a, b), answer)

    def test_both_float(self):
        a, b = 8.6, 5.2
        answer = 44.72
        self.assertEqual(multiply(a, b), answer)

    def test_first_big(self):
        a, b = 1111125125125678987611111241412124124124142124, 3
        answer = 3333375375377036962833333724236372372372426372
        self.assertEqual(multiply(a, b), answer)

    def test_second_big(self):
        a, b = 7, 1295789237590279035903523709325790532790235790532790235790328
        answer = 9070524663131953251324665965280533729531650533729531650532296
        self.assertEqual(multiply(a, b), answer)

    def test_both_big(self):
        a, b = 51797258251798521798251798251789215789512789512789215789, 57328327589753986490607950458858544590
        answer = 2969450189310193539048523728246557476158539797933756200738600074661187275378397298387988531510
        self.assertEqual(multiply(a, b), answer)

    def test_first_little(self):
        a, b = 0.0000000000000000000000000000000000000003, 125256
        answer = 3.75768e-35
        self.assertEqual(multiply(a, b), answer)

    def test_second_little(self):
        a, b = 513253, 0.000000000000000000000000000000000000000000000035
        answer = 1.7963854999999998e-41
        self.assertEqual(multiply(a, b), answer)

    def test_both_little(self):
        a, b = 2.4e-35, 5.495e-48
        answer = 1.3188000000000003e-82
        self.assertEqual(multiply(a, b), answer)

    def test_exp_first(self):
        a, b = 1.124124e13, 4
        answer = 44964960000000.0
        self.assertEqual(multiply(a, b), answer)

    def test_second_zero(self):
        a, b = 1.124124e243, 0
        answer = 0
        self.assertEqual(multiply(a, b), answer)

    def test_first_zero(self):
        a, b = 0, 1.124124e243
        answer = 0
        self.assertEqual(multiply(a, b), answer)

    def test_both_zero(self):
        a, b = 0, 0
        answer = 0
        self.assertEqual(multiply(a, b), answer)