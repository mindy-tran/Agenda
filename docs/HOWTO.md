# HOWTO complete the Appointments project

You will create a source file called appt.py that defines two Python classes, Appt for a single appointment and Agenda for a list of appointments. These classes are used by appt\_io.py and check\_agenda.py to provide the output shown above. In addition to appt\_io.py and check\_agenda.py, we have provided some example input in test\_data, and a test suite in test\_appt.py. Use test\_appt.py to check your progress as you work through the project.

Although you will build appt.py from scratch, many parts are provided for you in the instructions below.


## Skeleton of appt.py

Start by creating a docstring for the file. Indicate your name and briefly describe what this Python source file provides (which is the classes Appt and Agenda).

After the docstring comment, create the code to be run if this program is executed as the main Python program. It should look like this:

```python
if __name__ == "__main__":
    print("Running usage examples")` 
```

This code doesn't do anything useful yet, but let's execute the test suite anyway. Execute test\_appt.py in PyCharm, or at the command line, like this:

`$ python3 test_appointment.py` 

The output should look somethine like this:

```text
Traceback (most recent call last):
  File "test_appointment.py", line 3, in from appt_io import parse_appt, parse_agenda, read_agenda
  File "/Users/michal/Dropbox/19W-211/projects/appointments/appt_io.py", line 13, in def parse_appt(appt_text: str) -> appt.Appt:
AttributeError: module 'appt' has no attribute 'Appt'` 
```

The test suite is trying to use class Appt, and we haven't created class Appt yet. Let's fix that. Introduce it like this:

```python
class Appt:
    """An appointment has a start time, an end time, and a title.
    The start and end time should be on the same day.
    Usage example:
        appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
        appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
        if appt2 > appt1:
            print(f"appt1 '{appt1}' was over when appt2 '{appt2}'  started")
        elif appt1.overlaps(appt2):
            print("Oh no, a conflict in the schedule!")
            print(appt1.intersect(appt2))
    Should print:
        Oh no, a conflict in the schedule!
        2018-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """
```

At this point the Appt class doesn't actually do anything, but perhaps we can at least get past the first failure in the test suite. We'll run the test suite again, and this time the output will look something like this:

```
Traceback (most recent call last):
  File "/Users/michal/Dropbox/19W-211/projects/appointments/test_appointment.py", line 3, in from appt_io import parse_appt, parse_agenda, read_agenda
  File "/Users/michal/Dropbox/19W-211/projects/appointments/appt_io.py", line 38, in def read_agenda(file: Iterable[str]) -> appt.Agenda:
AttributeError: module 'appt' has no attribute 'Agenda' 
```

OK, same problem, we need a class Agenda. We'll just create a dummy one for now:

`class Agenda:
    """FIXME in a bit"""` 

Now if we execute the test suite, we get a long list of errors. Progress!

### Building the Appt class

We'll ignore the tests of the Agenda class for now (even though those error messages may appear first in the output) and focus on completing the Appt class. In the test suite we can see that TestAppt is usng a function in appt\_io.py to create an Appt object from a string. The function in appt\_io in turn calls the constructor of Appt, which is the class we need to write. The call in parse\_appt uses some functions that are probably unfamiliar to build the arguments to the constructor, but we don't need to puzzle that out; we can see from the call

 `appt.Appt(period_start, period_finish, desc)` 

and from the example in the usage example

`appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")` 

that the constructor should take two datetime objects and a string.

datetime objects are defined in a Python library module, so before we can make use of them, we need to _import_ that module into appt.py. The import statement comes after the file's main docstring and before other code. We want to import the datetime class from datetime.py. The from form of import allows us to do that and then refer to the class datetime in the rest of the file without qualifying it as datetime.datetime:

`from datetime import datetime` 

Since this module will use datetime objects throughout, you should spend a few minutes reading documentation for that class. If [https://docs.python.org/3/library/index.html](https://docs.python.org/3/library/index.html) isn't already bookmarked in your browser, it should be. Search for _datetime_ and follow the link.

Now we can create the constructor method and specify that two of its arguments should be datetime objects. The constructor method (which is always called \_\_init\_\_ in Python) should look like this:

```python
   def __init__(self, start: datetime, finish: datetime, desc: str):
        """An appointment from start time to finish time, with description desc.
        Start and finish should be the same day.
        """
        assert finish > start, f"Period finish ({finish}) must be after start ({start})"
        self.start = start
        self.finish = finish
        self.desc = desc
```

Note the assertion at the beginning of the constructor: The program will (intentionally) crash if we try to create an appointment that takes zero time or that ends before it starts. This is called a _precondition_ check. The Appt method checks its precondition and crashes immediately, in a predictable way, if it is violated. This is much better than silently accepting bad data and then crashing or giving erroneous results later in some unpredictable manner.

How is that comparison `finish > start` working? How does Python know how to compare two datetime objects? It's magic! No, really. It uses a trick called “magic methods” Officially they are called “special methods”, but everyone calls them “magic methods”.

When you write an expression like `x < y`, Python interprets it as a call on a method like `__lt__` (less than). 
This is the case even for the built-in classes like `int` and `str`. Don't believe me? Try this in a Python console:

```
>>> (5).__lt__(3)
False
>>> (3).__lt__(5)
True
>>> "squid".__gt__("octopus")
True
```

The datetime class has defined methods for comparing datetime 
objects. We need to do the same thing for Appt objects. In the 
test suite in test\_appts.py, we can see that test case 
`test_00_equality` and `test_01_order` compare appointments using
 `==`, `<` and `>`. 

```python
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
        self.assertTrue(self.naptime > self.more_coffee)` 
```

For appointments, we want `<` to mean “before” and `>` to mean “after”. One appointment is after another if it has ended when the other starts. For example, if I have a meeting from 10am to 11am, and class beginning 11am, then my meeting is before my class. But if my meeting is from 10am to 11:30am, and class starts at 11am, then my meeting is not _before_ my class even though it starts earlier. If two appointments overlap, we will say that neither one is before (<) the other.

For appointments, the operations you need are:

* `<` : 
“before”. Appointment _a_ is before appointment _b_ iff the finish time of _a_ is equal or earlier than the start time of _b_. Magic method name is \_\_lt\_\_ ,

* `>` : 
“after”. Appointment _a_ is after appointment _b_ iff the start time of _a_ is equal or after the finish time of _b_. Magic method name is \_\_gt\_\_ .

* `==` : 
“equal”. We say that two appointments are equal if they have the same start and end times, _even if they have different titles._ Magic method name is \_\_eq\_\_ .

* `!=` : 
“not equal”. You do not need to implement a magic method for !=. Python calls the the \_\_eq\_\_ method and negates the result.

Here is an implementation of \_\_eq\_\_:

```python
def __eq__(self, other: 'Appt') -> bool:
        """Equality means same time period, ignoring description"""
        return self.start == other.start and self.finish == other.finish
```

You need to write similar implementations for `__lt__` and 
`__gt__`. When you have added these methods to the Appt class, two of the nine test cases in test\_appt.py should pass:

```
EEEEE..EE
...
 ----------------------------------------------------------------------
Ran 9 tests in 0.009s

FAILED (errors=7)
```

Tests test_00_equality and test_01_order should now be passing. Tests test\_02\_overlap and test\_03\_intersect check methods we have not yet implemented.


### Checking for overlapping appointments

Our ultimate goal is to check for conflicting appointments. For example, if we have scheduled a lunch meeting from noon to 1:30pm, and scheduled another meeting from 1pm to 2pm, then there is a conflict in our schedule because those appointments overlap in time. You must implement a method overlap to determine whether two appointments overlap in time, and a method intersect to determine the period period of overlap. These methods must not alter the appointments being compared.

The header of method overlap in class Appt should look like this:

```
 def overlaps(self, other: 'Appt') -> bool:
        """Is there a non-zero overlap between these periods?"""
```

Note that you have already implemented methods to determine whether an appointment _a_ is over when appointment _b_ starts (a < b) or vice versa (a > b). You should make use of these rather than coding the same logic again. This is called the _DRY_ principle: Don't Repeat Yourself.

You must also create method intersect for determining the period of overlap between two appointments. self.overlaps(other) is a _precondition_ of intersect and must be tested at the beginning of the method. The result of method intersect should be a new Appt object. The usage example in the docstring for class Appt illustrates how the description of the new appointment should be formed from the descriptons of the two overlapping appointments.

When you have successfully implemented overlaps and intersect, test cases test\_02\_overlap and test\_03\_intersect should pass. Only the test cases for class Agenda should still fail, because you haven't written that class yet.

```
EEEEE....
======================================================================
ERROR: test_0_conflict (__main__.TestAgendaConflicts)
A small agenda that does have a conflict
----------------------------------------------------------------------
....
AttributeError: 'Agenda' object has no attribute 'append'

----------------------------------------------------------------------
Ran 9 tests in 0.007s

FAILED (errors=5)
``` 

### Formatting appointments

At this point we are passing all the tests for class Appt, but there is one last thing to take care of before moving on to class Agenda. If we print an appointment, it doesn't look very nice:

```
>>> from appt import Appt
>>> from datetime import datetime
>>> ap = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
>>>print(ap)
<appt.Appt object at 0x10cc1e4e0>
``` 

This default formatting does not cause any of our test cases to fail yet, but it will cause problems later when we are reading and writing agenda files, and it is clearly not very useful. A user of our scheduling software is more likely to care that coffee break begins at 3:00pm than that it is stored in an object at memory address 0x10cc1e4e0. Let's fix it now.

Some of the built in functions in Python also invoke magic methods. The str function is one of these. The print function calls the str function on each variable it prints, and str(x) in turn calls magic method x.\_\_str\_\_(). Therefore we need to provide a \_\_str\_\_ method for class Appt.

We want the output format of an appointment to be the same as the input format. The [xkcd strip](https://xkcd.com) reminds us that there is a right way to do this:

![](https://imgs.xkcd.com/comics/iso_8601.png)

Fortunately the datetime class provides methods for producing this format. To save you some time reading the documentation for datetime and experimenting with the formatting methods, a definition for the \_\_str\_\_ method of Appt is provided for you here:
```
 def __str__(self) -> str:
        """The textual format of an appointment is
        yyyy-mm-dd hh:mm hh:mm  | description
        Note that this is accurate only if start and finish
        are on the same day.
        """
        date_iso = self.start.date().isoformat()
        start_iso = self.start.time().isoformat(timespec='minutes')
        finish_iso = self.finish.time().isoformat(timespec='minutes')
        return f"{date_iso} {start_iso} {finish_iso} | {self.desc}"` 

```

### The Agenda class

An agenda is almost like a list of Appt objects. In fact, we would like to use all the methods of the list class, such as append, the len function, and the indexing operations like \[i\] to access individual appointments. We'd like to follow the _DRY_ principle and not rewrite these. However, we need a few more methods, including methods to detect conflicting appointments.

Fortunately we do not have to start from scratch. We can say that an Agenda is a kind of list, with all the methods of the standard list class, plus a few more that we will design:

```python
class Agenda(list):
    """An Agenda is a collection of appointments.
    It has most of the methods of a list, such as
    'append' and iteration, and in
    addition it has a few special methods, including
    a method for finding conflicting appointments.

    Usage:
    appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
    appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
    agenda = Agenda()
    agenda.append(appt1)
    agenda.append(appt2)
    if agenda.unconflicted():
        print(f"Agenda has no conflicts")
    else:
        print(f"In agenda:\n{agenda.text()}")
        print(f"Conflicts:\n {agenda.conflicts().text()}")

    Expected output:
    In agenda:
    2018-03-15 13:30 15:30 | Early afternoon nap
    2018-03-15 15:00 16:00 | Coffee break
    Conflicts:
    2018-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """
```

The line class Agenda(list): says we are making a new class Agenda but not starting from scratch. We are starting with class list and making some modifications. We say that list is the _superclass_ of Agenda, and that Agenda is a _subclass_ of list. We can also say that class Agenda _extends_ class list.

We do not need to write a constructor. We will create a new, empty Agenda object as Agenda(). The constructor for list will suit our purposes without change.

We do need a method to format an Agenda object. list has a \_\_str\_\_ method, but it doesn't produce the format we want, with each appointment on a line by itself. We'll add a new method text that produces the format we want in printed schedules. This can be quite short if we make use of a list comprehension and the join method:

```python
  def text(self) -> str:
        """Returns a string in the same form as we
        expect to find in an input file.  Note that this
        is different from the __str__ method inherited
        from 'list', which is still available.
        """
        as_list = [str(appt) for appt in self]
        return "\n".join(as_list)` 
```

The other important methods we need to add are one to determine whether there are any conflicts, and one to produce a list of conflicts. If we have a method for producing the list of conflicts as an Agenda object, the method for determining whether there are conflicts can be trivial:

```python
def unconflicted(self) -> bool:
        """True if none of the appointments in this agenda overlap.
        Side effect: Agenda is sorted.
        """
        return len(self.conflicts()) == 0;
``` 

So, all we really need to do is produce an Agenda object with the conflicts (overlapping appointments). It's signature should look like this:

 ```python
 def conflicts(self) -> 'Agenda':
        """Returns an agenda consisting of the conflicts
        (overlaps) between appointments in this agenda.
        """
```

We already have overlaps method and an intersect method in class Appt. It seems like we could simply loop through the items in the Agenda, comparing each element to every other element. However, recall this point in the required behavior section of the assignment:

*Your algorithm must run in time O(n lg n) where n is max(number of appointments, number of conflicts).*

Consider the simple algorithm thatuses nested loops to compare each element to every other element. If there 1000 appointments, the first must be compared to 999 other appointments, the second must be compared to 9998 other appointments, and so on. The total running time would be O(n2) where n is the number of appointments. We just do better.

The requirement for time O(n lg n) (called log-linear time) is a hint of a better method. That just happens to be the efficiency of the best comparison-based sorting methods. It is, in particular, the efficiency of the sort method of the Python list class. Also, this sort method is even faster for lists that are already in order. In that case it runs in time O(n), where n is the length of the list. This means there is little penalty for sorting a list that is already sorted.

We can make the conflict-finding method much more efficient if we start by putting the Appt objects in order by start time. But this will be a _side effect_ of the conflicts method, so we'd better note that in the docstring:

```python
def conflicts(self) -> 'Agenda':
        """Returns an agenda consisting of the conflicts
        (overlaps) between this agenda and the other.
        Side effect: This agenda is sorted
        """
```

We can _almost_ just use the sort method of list, but we need to specify that Appt objects should be sorted by start times. The sort method provides a way specify a _sort key_ in the form of a function that extracts the part to be compared. We'll override the sort method in class agenda to sort by start times:

```python
 def sort(self, key=lambda appt: appt.start, reverse=False):
        """We sort by start time unless another
        sort key is given.
        """
        super().sort(key=key, reverse=reverse)
``` 

There are a couple of things to notice in this method. First is that we provide two keyword arguments, key and reverse. The key argument is provided because we want to make sorting by start time the default. The other keyword argument, reverse, is provided just because the sort method of class list has a reverse option. We're not particularly interested in it here, but we pass it on to the sort method of list for compatibility. (PyCharm will complain if we don't.)

The second thing to notice is the called to super.sort(). Recall that since we declared the class as Agenda(list), list is the _superclass_ of class Agenda. If we just wrote self.sort(), we would be making a recursive call on the same sort method we are writing. By calling super().sort() we can call the sort method of the superclass, i.e., class list.

Now that we can sort appointments in an agenda by time, how can we make use of that to find all the conflicts in log-linear time? Drawing some pictures will help us reason about the algorithm. Suppose we have appointments _a_..._e_ with start and finish times as shown here:

![](img/appt-overlap.png)

These appear in the Agenda object in order _a, b, c, d, e_, that is, in order of their start times (because we sorted them in that order). Now consider which appointments _a_ must be compared with.

![](img/appt-overlap-a.png)

We must compare _a_ with _b_ and then with each subsequent appointment until we reach _d_. When we reach _d_ and notice that _d_ starts _after a is finished_, we do not have to look farther. Any Appt object that appears after _e_ in the sorted sequence must also start after _a_ has finished.

Next consider the set of appointments we must compare _b_ with. We do not need to consider _a_ again, because we have already found that conflict. We must consider the appointments that appear _after_ _b_ in the sorted list, but only until we find one that starts after _b_ has finished.

![](img/appt-overlap-b.png)

From this we can see that we can search for conflicts with nested loops, cutting the inner loop short with a break statement. The outer _for_ loop iterates through all the appointments in the Agenda list. The inner _for_ loop starts at the item just after the current appointment. It could continue to the end of the sequence, if all the appointments overlapped, but it can be cut off as soon as we encounter an appointment that starts after the appointment selected by the outer loop.

If you think carefully about this algorithm, you will see that the worst case running time is proportional to the number of appointments plus the number of conflicts. This satisfies our performance requirement. It should easily pass the timing test in test\_1\_fast:

```python

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
        log.debug(f"Checked {len(self.big)} entries in {elapsed_seconds} seconds")` 
```

When you have provided a correct conflicts method, along with sort, text, and unconflicted, the test cases in test\_appointment.py should pass:

```
.DEBUG:__main__:Checked 5000 entries in 0.006273803999647498 seconds
.DEBUG:__main__:Checked 1002 entries in 0.00219668002682738 seconds
.......
----------------------------------------------------------------------
Ran 9 tests in 0.529s

OK
```