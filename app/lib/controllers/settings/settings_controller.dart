import 'package:app/controllers/theme/theme_controller.dart';
import 'package:app/utils.dart';
import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:mobx/mobx.dart';

part '../../gen/controllers/settings/settings_controller.g.dart';

class SettingsController = SettingsControllerStorage with _$SettingsController;

abstract class SettingsControllerStorage with Store {
  final ThemeContoller _themeContoller;

  SettingsControllerStorage({required ThemeContoller themeContoller}) : _themeContoller = themeContoller;

  @action
  Future<void> init() async {
    selectedThemeMode = _themeContoller.theme;
    selectedColor = _themeContoller.themeColor;
  }

  @action
  void changeTheme(ThemeMode newTheme) {
    selectedThemeMode = newTheme;
    _themeContoller.changeTheme(newTheme);
  }

  @action
  void changeColor(Color newColor) {
    selectedColor = newColor;
    _themeContoller.changeThemeColor(newColor);
  }

  @observable
  ThemeMode selectedThemeMode = ThemeMode.system;

  @observable
  Color selectedColor = HexColor.fromHex("#0967b0");

  List<Color> themeColorsList = [
    const Color.fromRGBO(9, 103, 176, 1),
    Colors.amber,
    Colors.purple,
    Colors.green,
    Colors.indigo,
  ];
}
