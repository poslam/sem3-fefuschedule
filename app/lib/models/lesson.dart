class LessonViewModel {
  late int eventId;
  late String eventName;
  late int order;
  late DateTime begin;
  late DateTime end;
  late String facility;
  late String spec;
  late int capacity;
  late String teacher;
  late String group;
  late String subgroup;

  LessonViewModel();

  LessonViewModel.fromJson(Map<String, dynamic> json) {
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
