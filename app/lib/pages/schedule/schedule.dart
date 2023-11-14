import 'package:app/pages/schedule/widgets/shedule_page.dart';
import 'package:app/pages/schedule/widgets/week_data.dart';
import 'package:app/pages/schedule/widgets/week_day_indicator.dart';
import 'package:flutter/material.dart';

import 'widgets/date_picker.dart';

class Schedule extends StatelessWidget {
  const Schedule({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.secondaryContainer,
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: WeekData(),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.only(left: 8.0, right: 8.0),
                child: ShedulePage(),
              ),
            ),
          ],
        ),
      ),
      // floatingActionButton: FloatingActionButton(
      //   onPressed: () {},
      //   child: const Icon(Icons.filter_alt),
      // ),
    );
  }
}
