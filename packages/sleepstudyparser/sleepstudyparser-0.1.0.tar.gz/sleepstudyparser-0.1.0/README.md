# Sleep Study Parser

Simple package which can be used to parse the sleep study report from Windows 11.

## Usage

Below we are parsing a sleep study report where 12th state is like this:
![img.png](sleepstudyparser/static/img.png)

To get the same thing via Python we can do this:

```python
>>> from sleepstudyparser.SleepStudyParser import SleepStudyParser
>>> ssp = SleepStudyParser(number_of_days=2, report_name="DummySleepStudyReport", report_path=r"C:\temp")
>>> obj = ssp.parse()
>>> len(obj.states)
84
>>> obj.states[11].start_time
2021-11-15 07:16:48+00:00
>>> obj.states[11].duration
13:15:33
>>> obj.states[11].state_type
SessionType.SLEEP
>>> obj.states[11].drips.sw_drips
100
>>> obj.states[11].drips.hw_drips
68
```