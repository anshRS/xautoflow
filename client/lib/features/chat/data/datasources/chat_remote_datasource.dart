import 'dart:async';
import 'dart:convert';

import 'package:client/features/chat/data/models/message_model.dart';
import 'package:client/common/entities/message.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:web_socket_client/web_socket_client.dart';

final _baseUrl = dotenv.env['BACKEND_WS_URL'];

class ChatRemoteDatasource {
  WebSocket? _socket;

  ChatRemoteDatasource();

  Future<void> connect(String userId) async {
    _socket ??= WebSocket(Uri.parse('$_baseUrl/code/$userId'));
  }

  void sendMessage(String query) {
    _socket!.send(json.encode({"query": query}));
  }

  Stream<MessageEntity> get messageStream {
    return _socket!.messages.map((data) {
      return MessageModel.fromJson(json.decode(data));
    });
  }

  void dispose() {
    _socket?.close();
    _socket = null;
  }
}
