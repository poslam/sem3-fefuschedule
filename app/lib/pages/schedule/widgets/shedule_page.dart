import 'package:app/controllers/schedule/controller.dart';
import 'package:app/controllers/schedule/data/controller.dart';
import 'package:app/controllers/schedule/data/service.dart';
import 'package:app/logger.dart';
import 'package:app/models/lesson.dart';
import 'package:app/pages/schedule/widgets/date_picker.dart';
import 'package:app/pages/schedule/widgets/week_day_indicator.dart';
import 'package:app/utils.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:get_it/get_it.dart';
import 'package:loading_animation_widget/loading_animation_widget.dart';

class ShedulePage extends StatelessWidget {
  ShedulePage({super.key});

  final ScheduleWidgetController controller = GetIt.I<ScheduleWidgetController>();
  final ScheduleController dataController = GetIt.I<ScheduleController>();

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4.0, right: 4.0),
          child: WeekDayIndicator(),
        ),
        Padding(
          padding: const EdgeInsets.only(left: 4.0, right: 4.0, bottom: 8.0),
          child: DatePicker(),
        ),
        Flexible(
          child: PageView.builder(
              controller: controller.datePageScrollController,
              onPageChanged: (index) => controller.setDayOffSet(index),
              itemBuilder: (context, index) => Observer(builder: (context) {
                    DateTime currDay = controller.anchorMonday.add(Duration(days: index)).getDateOnly();

                    bool isDayFetched = (dataController.fetchedDays.contains(currDay));

                    if (!isDayFetched)
                      return Center(
                        child: LoadingAnimationWidget.twoRotatingArc(
                            color: Theme.of(context).colorScheme.primary, size: 60),
                      );

                    return ListView(
                      children: dataController
                          .getLessonsDataByDay(currDay)
                          .keys
                          .map((key) {
                            Map<String, dynamic> data = dataController.getLessonsDataByDay(currDay)[key];

                            return EventCard(
                              number: data["number"].toString(),
                              timeLabel: data["timeLabel"],
                              lessons: data["lessons"].cast<LessonViewModel>(),
                            );
                          })
                          .joinDynamic(
                            Divider(
                              color: Theme.of(context).colorScheme.secondary,
                            ),
                          )
                          .toList()
                          .cast<Widget>(),
                    );
                  })),
        ),
      ],
    );
  }
}

class EventCard extends StatelessWidget {
  const EventCard({super.key, required this.number, required this.timeLabel, required this.lessons});

  final String number;
  final String timeLabel;
  final List<LessonViewModel> lessons;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Chip(
              color: MaterialStatePropertyAll<Color>(Theme.of(context).colorScheme.primaryContainer),
              label: Text(
                number,
                style: Theme.of(context)
                    .textTheme
                    .titleSmall!
                    .copyWith(color: Theme.of(context).colorScheme.onPrimaryContainer),
              ),
            ),
            Chip(
              color: MaterialStatePropertyAll<Color>(Theme.of(context).colorScheme.secondaryContainer),
              label: Text(
                timeLabel,
                style: Theme.of(context)
                    .textTheme
                    .titleSmall!
                    .copyWith(color: Theme.of(context).colorScheme.onSecondaryContainer),
              ),
            )
          ],
        ),
        SizedBox(
          height: 160,
          child: Card(
            color: Theme.of(context).colorScheme.primary.withOpacity(0.6),
            elevation: 5,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(13)),
            child: lessons.length == 0
                ? Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(13),
                      color: Colors.grey.withOpacity(0.6),
                    ),
                    child: Center(
                      child: Text(
                        "Занятий нет :/",
                        style: Theme.of(context)
                            .textTheme
                            .displayLarge
                            ?.copyWith(color: Theme.of(context).colorScheme.onSecondaryContainer),
                      ),
                    ),
                  )
                : Column(
                    mainAxisSize: MainAxisSize.max,
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Flexible(
                        child: Container(),
                      ),
                      Text("Предмет"),
                      Text(lessons.first.eventName ?? ""),
                      Text("Аудитория"),
                      Text(lessons.first.facility ?? ""),
                      Text("Перподователь"),
                      Text(lessons.first.teacher ?? ""),
                    ],
                  ),
          ),
        ),
      ],
    );
  }
}
