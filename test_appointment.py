import unittest
import time
from appt_io import parse_appt, parse_agenda, read_agenda
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class TestAppt(unittest.TestCase):
    """Basic Unit Tests for Appt class"""

    def setUp(self):
        self.coffee = parse_appt("2019-01-01 08:00 10:00 | Coffee with neighbors")
        self.coffee_same = parse_appt("2019-01-01 08:00 10:00 | Should be same as coffee")
        self.brunch = parse_appt("2019-01-01 09:00  13:00 | Brunch with neighbors")
        self.brunch_same = parse_appt("2019-01-01 09:00  13:00 | Should be same as brunch")
        self.more_coffee = parse_appt("2019-01-01 13:00 15:00 | More coffee")
        self.naptime = parse_appt("2019-01-01 16:00 18:00 | Afternoon nap")
        self.last_year = parse_appt("2018-01-01 09:00  13:00 | Brunch with neighbors")
        self.next_month = parse_appt("2019-02-01 09:00  13:00 | Brunch with neighbors")

    def test_00_equality(self):
        self.assertTrue(self.brunch == self.brunch)
        self.assertTrue(self.coffee == self.coffee_same)
        self.assertTrue(self.coffee != self.brunch)

    def test_01_order(self):
        self.assertTrue(self.coffee < self.more_coffee)
        self.assertFalse(self.coffee > self.more_coffee)
        self.assertTrue(self.more_coffee > self.coffee)
        self.assertFalse(self.more_coffee < self.coffee)
        self.assertTrue(self.last_year < self.brunch)
        self.assertTrue(self.brunch < self.next_month)
        self.assertTrue(self.naptime > self.more_coffee)

    def test_02_overlap(self):
        self.assertTrue(self.coffee.overlaps(self.brunch))
        self.assertTrue(self.brunch.overlaps(self.coffee))
        self.assertFalse(self.coffee.overlaps(self.more_coffee))
        self.assertFalse(self.brunch.overlaps(self.more_coffee))

    def test_03_intersect(self):
        coffee_at_brunch = self.coffee.intersect(self.brunch)
        self.assertEqual(coffee_at_brunch,
                         parse_appt("2019-01-01 09:00 10:00 | Title doesn't matter"))
        # Original appointments should be unmodified
        self.assertEqual(self.coffee, self.coffee_same)
        self.assertEqual(self.brunch, self.brunch_same)


def crush(s: str) -> str:
    """Remove whitespace.  Useful in comparison.
    Note, does not remove comments.
    """
    return "".join(s.split())


def show_diff(observed: str, expected: str):
    """If strings differ other than in whitespace,
    print both expected and observed.
    """
    if crush(observed) != crush(expected):
        print(f"*** Expected:\n{expected}\n*** Observed:\n{observed}\n***")


class TestAgendaInOut(unittest.TestCase):
    """Test functions that convert text to and from Appt and Agenda"""

    def setUp(self):
        self.example = """
          2019-01-25 10:00 11:00 | sample 10-11 am Jan 25
          2019-01-25 13:00 15:00 | sample 1-3pm Jan 25
          2019-02-01 08:00 08:30 | sample 8am Feb 1
        """
        self.unsorted = """
          2019-01-25 10:00 11:00 | sample 10-11 am Jan 25
          2019-02-01 08:00 08:30 | sample 8am Feb 1
          2019-01-25 13:00 15:00 | sample 1-3pm Jan 25
        """

    def test01_inout(self):
        ag = parse_agenda(self.example)
        out = ag.text()
        show_diff(out, self.example)
        self.assertEqual(crush(self.example), crush(out))

    def test02_sorting(self):
        ag = parse_agenda(self.unsorted)
        ag.sort()
        out = ag.text()
        show_diff(out, self.example)
        self.assertEqual(crush(self.example), crush(out))


class TestAgendaConflicts(unittest.TestCase):
    """Can we test for conflicts?  Can we do it quickly?"""
    def setUp(self):
        small = """
        2018-01-01 09:15 10:30 | drowsy
        2018-01-01 10:15 11:20 | coffee
        2018-01-01 11:30 12:00 | waking
        """
        small_conflicts = """
        2018-01-01 10:15 10:30 |  drowsy and  coffee
        """
        self.small = parse_agenda(small)
        self.small_conflicts = parse_agenda(small_conflicts)
        big = open("test_data/thousand.txt")
        self.big = read_agenda(big)
        big.close()

    def test_0_conflict(self):
        """A small agenda that does have a conflict"""
        self.assertEqual(self.small.conflicts(), self.small_conflicts)

    def test_1_fast(self):
        """A linear time algorithm should be able to test
        an agenda with 5000 elements in well under a second,
        even on a fairly slow computer.
        """
        time_before = time.perf_counter()
        self.assertTrue(self.big.unconflicted())
        time_after = time.perf_counter()
        elapsed_seconds = time_after - time_before
        self.assertLess(elapsed_seconds, 2, "Are you sure your algorithm is linear time?")
        log.debug(f"Checked {len(self.big)} entries in {elapsed_seconds} seconds")

    def test_2_conflicts(self):
        """Like thousand.txt but with a couple of conflicts"""
        expected_txt = """
        2018-12-02 02:30 02:59 |   oops
        2018-12-02 03:00 03:59 |   oops  
        2018-12-02 04:00 04:59 |   oops
        2018-12-02 05:00 05:30 |   oops
        2018-12-07 06:30 06:59 |   oops
        2018-12-07 07:00 07:30 |   oops
        """
        expected_conflicts = parse_agenda(expected_txt)
        expected_conflicts.sort()
        oopsy_file = open("test_data/thousand2.txt")
        agenda = read_agenda(oopsy_file)
        oopsy_file.close()
        time_before = time.perf_counter()
        oops = agenda.conflicts()
        time_after = time.perf_counter()
        elapsed_seconds = time_after - time_before
        self.assertLess(elapsed_seconds, 3, "Are you sure your algorithm is linear time?")
        log.debug(f"Checked {len(agenda)} entries in {elapsed_seconds} seconds")
        oops.sort()
        self.assertEqual(oops, expected_conflicts)


if __name__ == "__main__":
    unittest.main()
