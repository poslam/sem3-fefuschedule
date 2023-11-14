import 'package:flutter/material.dart';

class DatePicker extends StatelessWidget {
  const DatePicker({super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Theme.of(context).colorScheme.secondaryContainer,
      elevation: 5,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(13),
        child: SizedBox(
          height: 60,
          child: PageView.builder(
            itemBuilder: (BuildContext context, int index) {
              return Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Expanded(child: DateButton()),
                  Expanded(child: DateButton()),
                  Expanded(child: DateButton()),
                  Expanded(child: DateButton()),
                  Expanded(child: DateButton()),
                  Expanded(child: DateButton()),
                  Expanded(child: DateButton()),
                ],
              );
            },
          ),
        ),
      ),
    );
  }
}

class DateButton extends StatelessWidget {
  const DateButton({super.key});

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 1,
      child: Padding(
        padding: const EdgeInsets.all(2.0),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(13),
            color: Theme.of(context).colorScheme.onSecondaryContainer,
          ),
          child: Center(
            child: Text(
              "23",
              style: Theme.of(context)
                  .textTheme
                  .bodyMedium!
                  .copyWith(color: Theme.of(context).colorScheme.secondaryContainer),
            ),
          ),
        ),
      ),
    );
  }
}
