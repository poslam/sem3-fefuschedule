import 'package:app/controllers/schedule/controller.dart';
import 'package:app/utils.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:get_it/get_it.dart';
import 'package:intl/intl.dart';

class WeekDayIndicator extends StatelessWidget {
  WeekDayIndicator({super.key});

  final ScheduleWidgetController controller = GetIt.I<ScheduleWidgetController>();

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 30,
      child: Observer(
          builder: (context) => Row(
                // mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: controller.selectedWeekData.weekDays
                    .getRange(0, 6)
                    .map((day) => Expanded(
                          child: Padding(
                            padding: const EdgeInsets.all(2.0),
                            child: Center(
                              child: Text(
                                DateFormat.E(Localizations.localeOf(context).languageCode).format(day),
                                style: Theme.of(context).textTheme.bodyLarge!.copyWith(
                                      color: Theme.of(context).colorScheme.onSecondaryContainer,
                                    ),
                              ),
                            ),
                          ),
                        ))
                    .toList(),
              )),
    );
  }
}
