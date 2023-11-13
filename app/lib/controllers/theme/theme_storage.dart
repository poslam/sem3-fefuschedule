import 'package:app/utils.dart';
import 'package:get_storage/get_storage.dart';
import 'package:flutter/material.dart';

class ThemeStorage {
  late GetStorage _box;

  static const String _boxName = "themeBox";

  ThemeMode get theme => convertThemeFromString(_theme);
  String _theme = "system";
  static const String _themeName = "theme";

  Color get themeColor => HexColor.fromHex(_themeColor);
  String _themeColor = "#0967b0";
  static const String _themeColorName = "themeColor";

  Future<void> init() async {
    await GetStorage.init(_boxName);
    _box = GetStorage(_boxName);

    _theme = _box.read(_themeName) ?? _theme;
    _themeColor = _box.read(_themeColorName) ?? _themeColor;
  }

  Future<void> writeNewTheme(ThemeMode newTheme) async {
    _theme = convertThemeTotring(newTheme);
    _box.write(_themeName, _theme);
  }

  Future<void> writeNewThemeColor(Color newColor) async {
    _themeColor = newColor.toHex();
    _box.write(_themeColorName, _themeColor);
  }

  ThemeMode convertThemeFromString(String theme) {
    switch (theme) {
      case "system":
        return ThemeMode.system;
      case "dark":
        return ThemeMode.dark;
      case "light":
        return ThemeMode.light;
    }
    return ThemeMode.system;
  }

  String convertThemeTotring(ThemeMode theme) {
    switch (theme) {
      case ThemeMode.system:
        return "system";
      case ThemeMode.light:
        return "light";
      case ThemeMode.dark:
        return "dark";
    }
  }
}
