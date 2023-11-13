import 'dart:convert';

import 'package:chopper/chopper.dart';
import 'package:app/logger.dart';

part '../../gen/controllers/auth/service.chopper.dart';

@ChopperApi()
abstract class AuthService extends ChopperService {
  Future<AuthBackendResponse> getInfo(String token) async {
    Response response = await _getInfo(token, "json");

    return convertResponse(response);
  }

  @Get(path: "/info")
  Future<Response> _getInfo(@Query("oauth_token") String token, @Query("format") String format);

  static AuthService create([ChopperClient? client]) => _$AuthService(client);
}

Future<AuthBackendResponse> convertResponse(Response response) async {
  AuthBackendResponse convertedResponse = AuthBackendResponse();

  convertedResponse.statusCode = response.statusCode;
  convertedResponse.rawResponse = response.body;

  if (response.statusCode != 200) {
    convertedResponse.status = AuthBackendResponseStatus.failed;
    convertedResponse.expectedResponse = null;
    return convertedResponse;
  }

  try {
    String jsonBody = const Utf8Decoder().convert(response.bodyBytes);
    Map<String, dynamic> json = jsonDecode(jsonBody);

    AuthBackendModel authBackendModel = AuthBackendModel();
    authBackendModel.emails = json["emails"];
    authBackendModel.firstName = json["first_name"];
    authBackendModel.lastName = json["last_name"];
  } catch (ex) {
    convertedResponse.expectedResponse = null;
    convertedResponse.status = AuthBackendResponseStatus.cantConvertResponse;
    return convertedResponse;
  }
  convertedResponse.status = AuthBackendResponseStatus.success;
  return convertedResponse;
}

enum AuthBackendResponseStatus {
  success,
  failed,
  cantConvertResponse,
}

class AuthBackendResponse {
  late final AuthBackendResponseStatus status;
  late final int statusCode;

  late final AuthBackendModel? expectedResponse;
  late final dynamic rawResponse;
}

class AuthBackendModel {
  late final String firstName;
  late final String lastName;
  late final List<String> emails;
}
