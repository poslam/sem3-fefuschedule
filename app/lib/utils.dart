import 'dart:ui';
import 'package:intl/intl.dart';

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

extension DateTimeDateOnly on DateTime {
  DateTime getDateOnly(){
    return DateTime( year , month , day );
  }
}

int getWeekNumber(DateTime date) {
  int dayOfYear = int.parse(DateFormat("D").format(date));
  int weekNumber = ((dayOfYear - date.weekday + 10) / 7).floor();
  return weekNumber;
}