import 'package:app/controllers/schedule/controller.dart';
import 'package:app/logger.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:get_it/get_it.dart';

class DatePicker extends StatelessWidget {
  DatePicker({super.key});

  final ScheduleWidgetController controller = GetIt.I<ScheduleWidgetController>();

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Theme.of(context).colorScheme.secondaryContainer,
      margin: EdgeInsets.zero,
      elevation: 5,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(13),
        child: SizedBox(
          height: 60,
          child: PageView.builder(
            controller: controller.datePickerPageController,
            onPageChanged: (index) => logger.i(index),
            itemBuilder: (BuildContext context, int index) => Observer(builder: (context) {
              return Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: controller
                    .getWeekData(index)
                    .weekDays
                    .getRange(0, 6)
                    .map(
                      (day) => Expanded(
                          child: DateButton(
                        date: day.day.toString(),
                        isSelected: day == controller.selectedDay,
                        onTap: () => controller.setSelectedDay(day),
                      )),
                    )
                    .toList(),
              );
            }),
          ),
        ),
      ),
    );
  }
}

class DateButton extends StatelessWidget {
  const DateButton({
    super.key,
    required this.date,
    required this.isSelected,
    required this.onTap,
  });

  final String date;
  final bool isSelected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 1,
      child: InkWell(
        borderRadius: BorderRadius.circular(13),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(4.0),
          child: AnimatedContainer(
            duration: Durations.medium2,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(13),
              color: isSelected
                  ? Theme.of(context).colorScheme.primaryContainer
                  : Theme.of(context).colorScheme.onSecondaryContainer,
            ),
            child: Center(
              child: Text(
                date,
                style: Theme.of(context).textTheme.bodyMedium!.copyWith(
                    color: isSelected
                        ? Theme.of(context).colorScheme.onPrimaryContainer
                        : Theme.of(context).colorScheme.secondaryContainer),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
