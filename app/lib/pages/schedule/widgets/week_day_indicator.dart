import 'package:app/utils.dart';
import 'package:flutter/material.dart';

class WeekDayIndicator extends StatelessWidget {
  const WeekDayIndicator({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 30,
      child: Row(
        children: ["пн", "вт", "cр", "чт", "пт", "сб", "вс"]
            .map((day) => Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(2.0),
                    child: Center(
                      child: Text(
                        day,
                        style: Theme.of(context).textTheme.bodyLarge!.copyWith(
                              color: Theme.of(context).colorScheme.onSecondaryContainer,
                            ),
                      ),
                    ),
                  ),
                ))
            .toList(),
      ),
    );
  }
}
