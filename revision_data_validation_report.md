# Revision Data Validation Report

Source database: `/Users/christina.feng/.minimax-agent-cn/projects/33/revision_sessions.db`

This report summarizes the validation checks used when refreshing the JSON exports.

## Export outcome

- Student export kept existing `exams` arrays and replaced only `sessions` from SQLite.
- Final student revision session count: `16602`
- Final room session count: `820`
- Preserved exam entries in student export: `4822`

## Rerun After JSON Cleanup

The JSON files were cleaned up before rerunning the checks:

- Teacher names were normalized for casing and trailing spaces.
- The duplicate room row caused by `Luciana liu` versus `Luciana Liu` was removed.
- Grade 12 Economics revision sessions for paper codes `9708/34` and `9708/44` were cancelled on all dates except `2026/05/08`, `2026/05/19`, and `2026/06/03`.
- The Lim Wan `0511/12 - INTENSIVE: Reading and Writing 12` group on `2026/05/06 08:20-12:10` was merged into room `B2040` using the provided student roster.
- Teacher multi-room overlaps are only treated as conflicts when the session name is the same. If the same teacher is in different rooms at the same time for different sessions, it is not counted as a conflict.

- Teacher conflict slots after rerun: `0`
- Room conflict slots after rerun: `14`
- Duplicate student-session rows: `2845`

Duplicate student-session rows were deduplicated in the student JSON export so repeated rows would not inflate a student's revision schedule.

## Full teacher conflicts

These rows show every remaining case where one teacher appears in more than one room at the same time for the same session.

No remaining teacher conflicts after the JSON updates and rerun.

## Full room conflicts

These rows show every remaining case where one room appears with more than one teacher at the same time after the JSON cleanup.

| Date | Start | End | Room | Teachers | Teacher List |
| --- | --- | --- | --- | ---: | --- |
| 2026/05/06 | 08:20 | 09:45 | B3011 | 2 | Christopher Burrow, Judy Zhu |
| 2026/05/07 | 13:00 | 14:25 | B1034 | 2 | Amit Bishan, Zoe Wang |
| 2026/05/08 | 08:20 | 09:45 | B1034 | 2 | Amit Bishan, Reza Hamroun |
| 2026/05/11 | 13:00 | 14:25 | B1034 | 2 | Amit Bishan, Zoe Wang |
| 2026/05/12 | 08:20 | 09:45 | B1034 | 2 | Zoe Wang, Bill Jiang |
| 2026/05/13 | 08:20 | 09:45 | B1034 | 2 | Rajesh Choyikkunimmal, Zoe Wang |
| 2026/05/15 | 08:20 | 09:45 | B1034 | 2 | Zoe Wang, Amit Bishan |
| 2026/05/18 | 13:00 | 14:25 | B1034 | 2 | Ruben Castilla, Zoe Wang |
| 2026/05/19 | 13:00 | 14:25 | B1034 | 2 | Zoe Wang, Bill Jiang |
| 2026/05/20 | 08:20 | 09:45 | B1034 | 2 | Fiona Fu, Zoe Wang |
| 2026/05/22 | 10:00 | 12:10 | B3027 | 2 | Luciana Liu, Amanda Milne |
| 2026/05/25 | 14:35 | 16:00 | B1034 | 2 | Zoe Wang, Leon Zhang |
| 2026/05/28 | 14:35 | 16:00 | B1034 | 2 | Celia Sun, Zoe Wang |
| 2026/06/03 | 14:35 | 16:00 | B1034 | 2 | Christine Du, Zoe Wang |

## Sample duplicate student-session rows

These rows show exact duplicate student assignments in SQLite before deduplication.

| Student ID | Date | Start | End | Paper | Component | Teacher | Room | Dupes |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| 1154 | 2026/05/06 | 08:20 | 09:45 | 9696/12 | Core Physical Geography 12 | Keith Seeley | B2044 | 2 |
| 1154 | 2026/05/06 | 08:20 | 09:45 | 9701/38 | Advanced Practical Skills 38 | Fiona Fu | B3010 | 2 |
| 1154 | 2026/05/06 | 10:00 | 12:10 | 9696/22 | Core Human Geography 22 | Alex Oniango | B2036 | 2 |
| 1154 | 2026/05/06 | 14:35 | 16:00 | 9709/55 | Probability & Statistics 1 (55) | Mandy Chen | B3042 | 2 |
| 1154 | 2026/05/07 | 08:20 | 12:10 | 9696/12 | INTENSIVE: Core Physical Geography 12 | Alex Oniango | B2036 | 2 |
| 1154 | 2026/05/07 | 10:00 | 12:10 | 9701/14 | Multiple Choice 14 | Judy Zhu | B2039 | 2 |
| 1154 | 2026/05/07 | 14:35 | 16:00 | 9701/24 | AS Level Structured Questions 24 | Judy Zhu | B3009 | 2 |
| 1154 | 2026/05/07 | 14:35 | 16:00 | 9701/38 | Advanced Practical Skills 38 | Fiona Fu | B2043 | 2 |
| 1154 | 2026/05/08 | 08:20 | 09:45 | 9696/22 | Core Human Geography 22 | Alex Oniango | B2036 | 2 |
| 1154 | 2026/05/08 | 10:00 | 12:10 | 9709/55 | Probability & Statistics 1 (55) | Eva Wang | B3012 | 2 |