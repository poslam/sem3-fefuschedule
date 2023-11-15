import 'package:app/controllers/schedule/data/service.dart';


import 'package:app/models/lesson.dart';


class ScheduleConverter {

  ScheduleConverter({required ScheduleService scheduleService}) : _scheduleService = scheduleService;


  final ScheduleService _scheduleService;


  Future<ScheduleResponse> getGroupSchedule(String groupName, DateTime begin, DateTime end) async {

    String beginStr = "${begin.year}-${begin.month}-${begin.day}T00:00:00";


    String endStr = "${end.year}-${end.month}-${end.day}T00:00:00";


    ScheduleBackendResponse backendResponse;


    ScheduleResponse response = ScheduleResponse();


    try {

      backendResponse = await _scheduleService.getGroupSchedule(groupName, beginStr, endStr);

    } catch (ex) {

      return response;

    }


    if (backendResponse.status != ScheduleBackendResponseStatus.success) {

      response.backendResponse = backendResponse;


      return response;

    }


    List<LessonViewModel> lessons = convertLessons(backendResponse.expectedResponse).toList();


    response.status = ScheduleResponseStatus.sucsess;


    response.lessons = lessons;


    response.backendResponse = backendResponse;


    return response;

  }

}


Iterable<LessonViewModel> convertLessons(List<LessonBackendModel> lessons) sync* {

  for (LessonBackendModel lesson in lessons) {

    LessonViewModel viewModel = LessonViewModel();


    viewModel.eventId = lesson.eventId ?? -1;


    viewModel.eventName = lesson.eventName ?? "#####";


    viewModel.order = lesson.order ?? -1;


    viewModel.begin = DateTime.tryParse(lesson.begin ?? "") ?? DateTime.now();


    viewModel.end = DateTime.tryParse(lesson.end ?? "") ?? DateTime.now();


    viewModel.facility = lesson.facility ?? "#####";


    viewModel.spec = lesson.spec ?? "#####";


    viewModel.capacity = lesson.capacity ?? -1;


    viewModel.teacher = lesson.teacher ?? "#####";


    viewModel.group = lesson.group ?? "#####";


    viewModel.subgroup = lesson.subgroup ?? "0";


    yield viewModel;

  }

}


class ScheduleResponse {

  ScheduleResponseStatus status = ScheduleResponseStatus.newtworkTrouble;


  List<LessonViewModel> lessons = [];


  ScheduleBackendResponse? backendResponse;

}


enum ScheduleResponseStatus {

  sucsess,


  newtworkTrouble,

}

