import 'dart:async';

import 'dart:convert';


import 'package:chopper/chopper.dart';


part '../../../gen/controllers/schedule/data/service.chopper.dart';


@ChopperApi()

abstract class ScheduleService extends ChopperService {

  Future<ScheduleBackendResponse> getGroupSchedule(String groupName, String begin, String end) async {

    Response response = await _getGroupSchedule("schedule", begin, end, groupName);

    return convertResponse(response);

  }


  @Get(path: "/view")

  Future<Response> _getGroupSchedule(

    @Query("type") String type,

    @Query("begin") String begin,

    @Query("end") String end,

    @Query("group_name") groupName,

  );


  static ScheduleService create([ChopperClient? client]) => _$ScheduleService(client);

}


FutureOr<ScheduleBackendResponse> convertResponse(Response response) async {

  ScheduleBackendResponse convertertedResponse = ScheduleBackendResponse();


  convertertedResponse.statusCode = response.statusCode;

  convertertedResponse.rawResponse = response.body;


  if (response.statusCode != 200) {

    convertertedResponse.status = ScheduleBackendResponseStatus.failed;

    convertertedResponse.expectedResponse = [];

    return convertertedResponse;

  }


  try {

    String jsonBody = const Utf8Decoder().convert(response.bodyBytes);

    List<dynamic> json = jsonDecode(jsonBody);


    List<LessonBackendModel> lessons = json.map((e) => LessonBackendModel.fromJson(e)).toList();


    convertertedResponse.expectedResponse = lessons;

  } catch (ex) {

    convertertedResponse.expectedResponse = [];

    convertertedResponse.status = ScheduleBackendResponseStatus.cantConvertResponse;

    return convertertedResponse;

  }

  convertertedResponse.status = ScheduleBackendResponseStatus.success;

  return convertertedResponse;

}


class ScheduleBackendResponse {

  late final ScheduleBackendResponseStatus status;


  late final int statusCode;


  late final List<LessonBackendModel> expectedResponse;

  late final dynamic rawResponse;

}


enum ScheduleBackendResponseStatus {

  success,

  failed,

  cantConvertResponse,

}


class LessonBackendModel {

  int? eventId;

  String? eventName;

  int? order;

  String? begin;

  String? end;

  String? facility;

  String? spec;

  int? capacity;

  String? teacher;

  String? group;

  String? subgroup;


  LessonBackendModel(

      {this.eventId,

      this.eventName,

      this.order,

      this.begin,

      this.end,

      this.facility,

      this.spec,

      this.capacity,

      this.teacher,

      this.group,

      this.subgroup});


  LessonBackendModel.fromJson(Map<String, dynamic> json) {

    eventId = json['event_id'];

    eventName = json['event_name'];

    order = json['order'];

    begin = json['begin'];

    end = json['end'];

    facility = json['facility'];

    spec = json['spec'];

    capacity = json['capacity'];

    teacher = json['teacher'];

    group = json['group'];

    subgroup = json['subgroup'];

  }


  Map<String, dynamic> toJson() {

    final Map<String, dynamic> data = <String, dynamic>{};

    data['event_id'] = eventId;

    data['event_name'] = eventName;

    data['order'] = order;

    data['begin'] = begin;

    data['end'] = end;

    data['facility'] = facility;

    data['spec'] = spec;

    data['capacity'] = capacity;

    data['teacher'] = teacher;

    data['group'] = group;

    data['subgroup'] = subgroup;

    return data;

  }

}

