import 'dart:convert';
import 'package:http/http.dart' as http;

String extractError(http.Response response) {
  try {
    final decoded = json.decode(response.body);
    if (decoded is Map<String, dynamic>) {
      return decoded['detail'] ??
          decoded['message'] ??
          decoded['error'] ??
          decoded['hint'] ??
          json.encode(decoded);
    }
    return json.encode(decoded);
  } catch (_) {
    return response.body.isNotEmpty ? response.body : 'Unexpected error';
  }
}
