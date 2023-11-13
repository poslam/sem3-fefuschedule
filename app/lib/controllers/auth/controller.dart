import 'package:app/controllers/auth/convertor.dart';
import 'package:mobx/mobx.dart';

part '../../gen/controllers/auth/controller.g.dart';

class AuthController = AuthControllerStore with _$AuthController;

abstract class AuthControllerStore with Store {
  AuthControllerStore({required AuthConvertor authConvertor}) : _authConvertor = authConvertor;

  final AuthConvertor _authConvertor;

  @observable
  bool isLoading = false;

  @action
  Future<void> getInfo(String token) async {
    isLoading = true;

    await _authConvertor.getInfo(token);

    isLoading = false;
  }
}
