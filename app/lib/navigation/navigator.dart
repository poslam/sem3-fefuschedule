import 'package:app/i18n/strings.g.dart';
import 'package:app/router.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AppNavigator {
  static String _previousRoute = "/schedule";

  static void goToSchedule() {
    // rootNavigatorKey.currentContext!.go("/dashboard");
    Router.neglect(
      rootNavigatorKey.currentContext!,
      () => rootNavigatorKey.currentContext!.goNamed(t.schedule.label, extra: {"previousRoute": _previousRoute}),
    );
    _previousRoute = "/schedule";
  }

  static void goToSearch() {
    // rootNavigatorKey.currentContext!.go("/dashboard");
    Router.neglect(
      rootNavigatorKey.currentContext!,
      () => rootNavigatorKey.currentContext!.goNamed(t.search.label, extra: {"previousRoute": _previousRoute}),
    );
    _previousRoute = "/search";
  }

  static void goToProfile() {
    // rootNavigatorKey.currentContext!.go("/dashboard");
    Router.neglect(
      rootNavigatorKey.currentContext!,
      () => rootNavigatorKey.currentContext!.goNamed(t.profile.label, extra: {"previousRoute": _previousRoute}),
    );
    _previousRoute = "/profile";
  }

  static void goToSettings() {
    rootNavigatorKey.currentContext!.goNamed(t.settings.label);
  }
}
