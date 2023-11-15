import 'package:app/controllers/schedule/controller.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:get_it/get_it.dart';
import 'package:intl/intl.dart';

class WeekData extends StatelessWidget {
  WeekData({super.key});

  final ScheduleWidgetController controller = GetIt.I<ScheduleWidgetController>();

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Observer(builder: (context) {
              return Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(left: 8.0),
                    child: Chip(
                      label: Text(controller.selectedWeekData.transtionDays.length == 1
                          ? DateFormat.MMMM(Localizations.localeOf(context).languageCode)
                              .format(controller.selectedWeekData.transtionDays.first)
                          : "${DateFormat.MMMM(Localizations.localeOf(context).languageCode).format(controller.selectedWeekData.transtionDays.first)} - ${DateFormat.MMMM(Localizations.localeOf(context).languageCode).format(controller.selectedWeekData.transtionDays.last)}"),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(13),
                      ),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.only(left: 8.0),
                    child: Chip(
                      label: Text(
                          "${DateFormat.d(Localizations.localeOf(context).languageCode).format(controller.selectedWeekData.weekDays.first)} - ${DateFormat.d(Localizations.localeOf(context).languageCode).format(controller.selectedWeekData.weekDays[5])}"),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(13),
                      ),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.only(left: 8.0, right: 8.0),
                    child: Chip(
                      label: Text(controller.selectedWeekData.isEven ? "Четная" : "Hечетная"),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(13),
                      ),
                    ),
                  ),
                ],
              );
            }),
          ),
        ),
        IconButton(
          onPressed: () {},
          icon: Icon(Icons.calendar_month_outlined),
        )
      ],
    );
  }
}
