import 'package:app/pages/login/login.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

final GlobalKey<NavigatorState> rootNavigatorKey = GlobalKey<NavigatorState>();
final GlobalKey<NavigatorState> _shellNavigationKey = GlobalKey<NavigatorState>();

final Map<String, int> routeIndex = {
  "/schedule": 0,
  "/search": 1,
  "/profile": 2,
};

final GoRouter router = GoRouter(
  routerNeglect: true,
  navigatorKey: rootNavigatorKey,
  initialLocation: "/login",
  routes: [
    GoRoute(
      path: "/login",
      builder: (context, state) => Login(),
    ),
  ],
);
