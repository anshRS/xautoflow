import 'package:client/common/entities/message.dart';

class MessageModel extends MessageEntity {
  MessageModel({required super.data, required super.isBot});

  factory MessageModel.fromJson(Map<String, dynamic> map) {
    return MessageModel(
      data: map['data'] as String,
      isBot: map['isBot'] as bool,
    );
  }

  MessageModel copyWith({String? data, bool? isBot}) {
    return MessageModel(data: data ?? this.data, isBot: isBot ?? this.isBot);
  }
}
