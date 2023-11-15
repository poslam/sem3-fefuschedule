import 'package:app/utils.dart';
import 'package:flutter/material.dart';
import 'package:mobx/mobx.dart';

part '../../gen/controllers/schedule/controller.g.dart';

class ScheduleWidgetController = ScheduleWidgetControllerStore with _$ScheduleWidgetController;

abstract class ScheduleWidgetControllerStore with Store {
  final DateTime minMondayDisplay;

  ScheduleWidgetControllerStore({required this.minMondayDisplay}) {
    _anchorMonday = minMondayDisplay.getDateOnly();
    _anchorMonday = _anchorMonday.subtract(Duration(days: _anchorMonday.weekday - 1));

    selectedDay = DateTime.now().getDateOnly();

    DateTime currMonday = DateTime.now().getDateOnly();
    currMonday = currMonday.subtract(Duration(days: currMonday.weekday - 1));

    datePickerPageController = PageController(
      initialPage: (currMonday.difference(_anchorMonday).inDays ~/ 7),
    );

    datePageScrollController = PageController(
      initialPage: DateTime.now().getDateOnly().difference(_anchorMonday).inDays,
    );

    _weekOffset = (currMonday.difference(_anchorMonday).inDays ~/ 7);
    _dayOffset = DateTime.now().getDateOnly().difference(_anchorMonday).inDays;

    selectedWeekData = getWeekData(currentWeekOffset);
  }

  PageController datePickerPageController = PageController();
  PageController datePageScrollController = PageController();

  @observable
  WeekData selectedWeekData = WeekData();

  @observable
  DateTime selectedDay = DateTime.now();

  int get currentWeekOffset => _weekOffset;
  int _weekOffset = 0;
  int _dayOffset = 0;
  DateTime get anchorMonday => _anchorMonday;
  DateTime _anchorMonday = DateTime.now();

  @action
  void setSelectedDay(DateTime newSelectedDay) {
    int diff = newSelectedDay.difference(selectedDay).inDays;
    datePageScrollController.jumpToPage(
      _dayOffset + diff,
    );
    _dayOffset += diff;
    selectedDay = newSelectedDay.getDateOnly();
  }

  @action
  void setDayOffSet(int newDayOffset) {
    _dayOffset = newDayOffset;
    DateTime newSelectedDay = _anchorMonday.add(Duration(days: _dayOffset)).getDateOnly();

    if (newSelectedDay.weekday == 7 && newSelectedDay.isBefore(selectedDay)) {
      newSelectedDay = newSelectedDay.subtract(const Duration(days: 1));
      _dayOffset -= 1;
      datePageScrollController.jumpToPage(_dayOffset);
    }

    if (newSelectedDay.weekday == 7 && newSelectedDay.isAfter(selectedDay)) {
      newSelectedDay = newSelectedDay.add(const Duration(days: 1));
      _dayOffset += 1;
      datePageScrollController.jumpToPage(_dayOffset);
    }

    int diff = getWeekNumber(newSelectedDay) - getWeekNumber(selectedDay);

    if (diff != 0) {
      setCurrentWeek(_weekOffset + diff);
      datePickerPageController.animateToPage(_weekOffset, duration: Durations.medium2, curve: Curves.linear);
    }

    selectedDay = newSelectedDay;
  }

  @action
  void setCurrentWeek(int newWeekOffset) {
    _weekOffset = newWeekOffset;
    selectedWeekData = getWeekData(_weekOffset);
  }

  WeekData getWeekData(int weekOffset) {
    List<DateTime> weekDays =
        List.generate(7, (index) => _anchorMonday.add(Duration(days: index + weekOffset * 7)).getDateOnly()).toList();

    WeekData newWeekData = WeekData();
    newWeekData.weekDays = weekDays;
    newWeekData.isEven = getWeekNumber(_anchorMonday.add(Duration(days: weekOffset * 7))) % 2 == 0;

    List<DateTime> transtionDays = [];
    for (int i = 0; i < 6; i++) {
      if (weekDays[i].month != weekDays[i + 1].month) {
        transtionDays.addAll([weekDays[i], weekDays[i + 1]]);
      }
    }

    if (transtionDays.isEmpty) {
      transtionDays.add(weekDays[0]);
    }

    newWeekData.transtionDays = transtionDays;

    return newWeekData;
  }
}

class WeekData {
  late final List<DateTime> transtionDays;
  late final List<DateTime> weekDays;

  late final bool isEven;
}
