import 'package:app/controllers/auth/service.dart';

class AuthConvertor {
  AuthConvertor({required AuthService authService}) : _authService = authService;

  final AuthService _authService;

  Future<AuthResponse> getInfo(String token) async {
    AuthResponse response = AuthResponse();

    try {
      await _authService.getInfo(token);
    } catch (ex) {
      response.status = AuthResponseStatus.newtworkTrouble;

      return response;
    }

    response.status = AuthResponseStatus.sucsess;
    return response;
  }
}

enum AuthResponseStatus {
  sucsess,
  newtworkTrouble,
}

class AuthResponse {
  late final AuthResponseStatus status;
}
