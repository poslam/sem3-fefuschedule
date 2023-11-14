
import 'package:app/utils.dart';
import 'package:mobx/mobx.dart';

part '../../gen/controllers/schedule/controller.g.dart';

class ScheduleController = ScheduleControllerStore with _$ScheduleController;

abstract class ScheduleControllerStore with Store {

  ScheduleControllerStore(){
    
    _anchorMonday = DateTime.now().getDateOnly();
    _anchorMonday = _anchorMonday.subtract(Duration(days: _anchorMonday.weekday));
    updateWeekData();

  }

  @observable
  WeekData selectedWeekData = WeekData();
  
  int get currentWeekOffset => _weekOffset;
  int _weekOffset = 0;

  DateTime _anchorMonday = DateTime.now();

  @action
  void setCurrentWeek(int newWeekOffset){
    _weekOffset = newWeekOffset;
    updateWeekData();
  }

  void updateWeekData(){
    List<DateTime> weekDays = List.generate(7, (index) => _anchorMonday.add(Duration(days: index + _weekOffset * 7))).toList();


    WeekData newWeekData = WeekData();
    newWeekData.weekDays = weekDays;
    newWeekData.isEven =  getWeekNumber(_anchorMonday.add(Duration(days: _weekOffset* 7))) % 2 == 0;
    
    List<DateTime> transtionDays = [];
    for(int i = 0 ; i < 6 ; i ++){

      if (weekDays[i].month != weekDays[i + 1].month){
        transtionDays.addAll([weekDays[i] , weekDays[i + 1]]);
      }
    }

    newWeekData.transtionDays = transtionDays;

    selectedWeekData = newWeekData;

  } 

}

class WeekData {

  late final List<DateTime> transtionDays;
  late final List<DateTime> weekDays;
  
  
  late final bool isEven;

}