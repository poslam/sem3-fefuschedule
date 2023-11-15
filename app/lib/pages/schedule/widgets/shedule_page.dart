import 'package:app/controllers/schedule/controller.dart';
import 'package:app/pages/schedule/widgets/date_picker.dart';
import 'package:app/pages/schedule/widgets/week_day_indicator.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:get_it/get_it.dart';

class ShedulePage extends StatelessWidget {
  ShedulePage({super.key});

  final ScheduleWidgetController controller = GetIt.I<ScheduleWidgetController>();

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
        Observer(builder: (context) {
          return Flexible(
            child: PageView.builder(
                controller: controller.datePageScrollController,
                onPageChanged: (index) => controller.setDayOffSet(index),
                itemBuilder: (context, index) {
                  return ListView(
                    children: [
                      Text(index.toString()),
                      Divider(
                        color: Theme.of(context).colorScheme.secondary,
                      ),
                      EventCard(),
                      Divider(
                        color: Theme.of(context).colorScheme.secondary,
                      ),
                      EventCard(),
                      Divider(
                        color: Theme.of(context).colorScheme.secondary,
                      ),
                      EventCard(),
                      Divider(
                        color: Theme.of(context).colorScheme.secondary,
                      ),
                      EventCard(),
                      Divider(
                        color: Theme.of(context).colorScheme.secondary,
                      ),
                      EventCard(),
                      Divider(
                        color: Theme.of(context).colorScheme.secondary,
                      ),
                      EventCard(),
                      Divider(
                        color: Theme.of(context).colorScheme.secondary,
                      ),
                      EventCard(),
                      Divider(
                        color: Theme.of(context).colorScheme.secondary,
                      ),
                      EventCard()
                    ],
                  );
                }),
          );
        }),
      ],
    );
  }
}

class EventCard extends StatelessWidget {
  const EventCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Chip(
              color: MaterialStatePropertyAll<Color>(Theme.of(context).colorScheme.primaryContainer),
              label: Text(
                "1",
                style: Theme.of(context)
                    .textTheme
                    .titleSmall!
                    .copyWith(color: Theme.of(context).colorScheme.onPrimaryContainer),
              ),
            ),
            Chip(
              color: MaterialStatePropertyAll<Color>(Theme.of(context).colorScheme.secondaryContainer),
              label: Text(
                "08:30 - 10:00",
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
            child: Container(),
          ),
        ),
      ],
    );
  }
}
