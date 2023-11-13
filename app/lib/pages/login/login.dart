import 'package:balanced_text/balanced_text.dart';
import 'package:chopper/chopper.dart';
import 'package:app/controllers/auth/controller.dart';
import 'package:flutter/material.dart';
import 'package:flutter_login_yandex/flutter_login_yandex.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:get_it/get_it.dart';
import 'package:loading_animation_widget/loading_animation_widget.dart';

class Login extends StatelessWidget {
  Login({super.key});

  final AuthController authController = GetIt.I<AuthController>();

  final _loginYandexPlugin = FlutterLoginYandex();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.secondaryContainer,
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const BalancedText(
              "Нам необходимо удостовериться что вы явялетесь студентом ДВФУ, войдите через корпоративный Яндекс ID",
              textAlign: TextAlign.center,
            ),
            Divider(
              color: Theme.of(context).colorScheme.onSecondaryContainer,
            ),
            ElevatedButton(
              onPressed: signIn,
              child: Observer(builder: (_) {
                if (authController.isLoading)
                  return LoadingAnimationWidget.prograssiveDots(
                    color: Theme.of(context).colorScheme.secondaryContainer,
                    size: 60,
                  );

                return Text("Войти с помошью Яндекс ID");
              }),
            )
          ],
        ),
      ),
    );
  }

  void signIn() async {
    Map<Object?, Object?>? response;
    try {
      response = await _loginYandexPlugin.signIn();
    } catch (ex) {}

    if (response == null) return;

    String _token;
    if (response['token'] != null) {
      _token = response['token'] as String;
    } else {
      _token = response['error'] as String;
    }

    authController.getInfo(_token);
  }
}
