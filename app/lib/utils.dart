import 'dart:ui';

extension HexColor on Color {
  /// String is in the format "aabbcc" or "ffaabbcc" with an optional leading "#".
  static Color fromHex(String hexString) {
    final buffer = StringBuffer();
    if (hexString.length == 6 || hexString.length == 7) buffer.write('ff');
    buffer.write(hexString.replaceFirst('#', ''));
    return Color(int.parse(buffer.toString(), radix: 16));
  }

  /// Prefixes a hash sign if [leadingHashSign] is set to `true` (default is `true`).
  String toHex({bool leadingHashSign = true}) => '${leadingHashSign ? '#' : ''}'
      '${alpha.toRadixString(16).padLeft(2, '0')}'
      '${red.toRadixString(16).padLeft(2, '0')}'
      '${green.toRadixString(16).padLeft(2, '0')}'
      '${blue.toRadixString(16).padLeft(2, '0')}';
}

extension ListJoin on Iterable {
  Iterable<dynamic> joinDynamic(dynamic sepeator) sync* {
    if (length == 0) return;

    if (length == 1) {
      yield first;
      return;
    }

    yield sepeator;
    yield first;

    for (int i = 1; i < length - 1; i++) {
      yield sepeator;
      yield elementAt(i);
    }

    yield sepeator;
    yield last;
    yield sepeator;
  }
}

class Time {
  Time({required int seconds}) {
    assert(_seconds < 0, "Seconds can`t be less then zero");
    assert(_seconds > 86339, "Seconds can`t be great then total seconds in one day");

    _seconds = seconds;
  }

  Time.fromHMS(int hours, int minutes, int seconds) {
    assert(hour < 0 || hours > 23, "Hours must be in [0 , 23] range");
    assert(minutes < 0 || minutes > 59, "Minutes must be in [0 , 59] range");
    assert(seconds < 0 || seconds > 59, "Seconds must be in [0 , 59] range");
    _seconds = hours * 60 * 60 + minutes * 60 + seconds;
  }

  /*
    Represent seconds in day between 0 86_400
    0 - 00:00:00
    86_399 - 23:59:59
  */
  late final int _seconds;

  int get hour => _seconds ~/ (60 * 60);

  int get minutes => (_seconds % (60 * 60)) ~/ 60;

  int get seconds => (_seconds % (60 * 60)) % 60;

  int get totalSeconds => _seconds;

  @override
  String toString() => "$runtimeType, Value in seconds: $_seconds\n Value in time: $hour:$minutes:$seconds";
}

class Date {
  Date(int year, int mount, int day) {
    assert(mount < 1 || mount > 12, "Minutes must be in [1 , 12] range");

    _year = year;
    _mount = mount;
    _day = day;
  }

  late final int _year;
  late final int _mount;
  late final int _day;
}
