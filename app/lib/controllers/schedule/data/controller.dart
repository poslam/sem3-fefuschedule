import 'package:app/controllers/schedule/data/converter.dart';

import 'package:app/logger.dart';

import 'package:app/models/lesson.dart';

import 'package:app/utils.dart';

import 'package:flutter/material.dart';

import 'package:mobx/mobx.dart';

part '../../../gen/controllers/schedule/data/controller.g.dart';

class ScheduleController = ScheduleControllerStore with _$ScheduleController;

abstract class ScheduleControllerStore with Store {
  ScheduleControllerStore({required ScheduleConverter scheduleConverter}) : _scheduleConverter = scheduleConverter;

  final ScheduleConverter _scheduleConverter;

  @observable
  Set<DateTime> fetchedDays = {};

  final Map<DateTime, Map<TimeOfDay, dynamic>> totalData = {};

  Map<TimeOfDay, dynamic> _initData = {
    TimeOfDay(hour: 8, minute: 30): {
      "timeLabel": "08:30 - 10:00",
      "number": 1,
      "lessons": [],
    },
    TimeOfDay(hour: 10, minute: 10): {
      "timeLabel": "10:10 - 11:40",
      "number": 2,
      "lessons": [],
    },
    TimeOfDay(hour: 11, minute: 50): {
      "timeLabel": "11:50 - 13:20",
      "number": 3,
      "lessons": [],
    },
    TimeOfDay(hour: 13, minute: 30): {
      "timeLabel": "13:30 - 15:00",
      "number": 4,
      "lessons": [],
    },
    TimeOfDay(hour: 15, minute: 10): {
      "timeLabel": "15:10 - 16:40",
      "number": 5,
      "lessons": [],
    },
    TimeOfDay(hour: 16, minute: 50): {
      "timeLabel": "16:50 - 18:20",
      "number": 6,
      "lessons": [],
    },
    TimeOfDay(hour: 18, minute: 30): {
      "timeLabel": "18:30 - 20:00",
      "number": 7,
      "lessons": [],
    },
    TimeOfDay(hour: 20, minute: 10): {
      "timeLabel": "20:10 - 21:40",
      "number": 8,
      "lessons": [],
    },
  };

  @action
  Future<void> fectchNewLessongs(DateTime begin, DateTime end) async {
    begin = begin.getDateOnly();

    end = end.getDateOnly();

    ScheduleResponse response = await _scheduleConverter.getGroupSchedule(
      "Б9122-01.03.02сп",
      begin,
      end,
    );

    if (response.status != ScheduleResponseStatus.sucsess) {
      return;
    }

    for (LessonViewModel lesson in response.lessons) {
      DateTime key = lesson.begin.getDateOnly();

      TimeOfDay beginTime = TimeOfDay(hour: lesson.begin.hour, minute: lesson.begin.minute);

      if (!totalData.containsKey(key))
        totalData[key] = {
          TimeOfDay(hour: 8, minute: 30): {
            "timeLabel": "08:30 - 10:00",
            "number": 1,
            "lessons": [],
          },
          TimeOfDay(hour: 10, minute: 10): {
            "timeLabel": "10:10 - 11:40",
            "number": 2,
            "lessons": [],
          },
          TimeOfDay(hour: 11, minute: 50): {
            "timeLabel": "11:50 - 13:20",
            "number": 3,
            "lessons": [],
          },
          TimeOfDay(hour: 13, minute: 30): {
            "timeLabel": "13:30 - 15:00",
            "number": 4,
            "lessons": [],
          },
          TimeOfDay(hour: 15, minute: 10): {
            "timeLabel": "15:10 - 16:40",
            "number": 5,
            "lessons": [],
          },
          TimeOfDay(hour: 16, minute: 50): {
            "timeLabel": "16:50 - 18:20",
            "number": 6,
            "lessons": [],
          },
          TimeOfDay(hour: 18, minute: 30): {
            "timeLabel": "18:30 - 20:00",
            "number": 7,
            "lessons": [],
          },
          TimeOfDay(hour: 20, minute: 10): {
            "timeLabel": "20:10 - 21:40",
            "number": 8,
            "lessons": [],
          },
        };

      totalData[key]![beginTime]["lessons"].add(lesson);
    }

    Set<DateTime> prevSet = {...fetchedDays};

    for (int i = 0; i < end.difference(begin).inDays; i++) {
      prevSet.add(begin.add(Duration(days: i)).getDateOnly());
    }

    fetchedDays = prevSet;

    logger.i("Fetched lessong between $begin - $end");
  }

  Map<TimeOfDay, dynamic> getLessonsDataByDay(DateTime day) {
    if (totalData.containsKey(day)) return totalData[day]!;

    return {
      TimeOfDay(hour: 8, minute: 30): {
        "timeLabel": "08:30 - 10:00",
        "number": 1,
        "lessons": [],
      },
      TimeOfDay(hour: 10, minute: 10): {
        "timeLabel": "10:10 - 11:40",
        "number": 2,
        "lessons": [],
      },
      TimeOfDay(hour: 11, minute: 50): {
        "timeLabel": "11:50 - 13:20",
        "number": 3,
        "lessons": [],
      },
      TimeOfDay(hour: 13, minute: 30): {
        "timeLabel": "13:30 - 15:00",
        "number": 4,
        "lessons": [],
      },
      TimeOfDay(hour: 15, minute: 10): {
        "timeLabel": "15:10 - 16:40",
        "number": 5,
        "lessons": [],
      },
      TimeOfDay(hour: 16, minute: 50): {
        "timeLabel": "16:50 - 18:20",
        "number": 6,
        "lessons": [],
      },
      TimeOfDay(hour: 18, minute: 30): {
        "timeLabel": "18:30 - 20:00",
        "number": 7,
        "lessons": [],
      },
      TimeOfDay(hour: 20, minute: 10): {
        "timeLabel": "20:10 - 21:40",
        "number": 8,
        "lessons": [],
      },
    };
  }
}
