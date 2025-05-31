import 'package:client/common/entities/message.dart';

class CodeMessageModel extends MessageEntity {
  CodeMessageModel({required super.data, required super.isBot});

  factory CodeMessageModel.fromJson(Map<String, dynamic> map) {
    return CodeMessageModel(
      data: map['data'] as String,
      isBot: map['isBot'] as bool,
    );
  }

  CodeMessageModel copyWith({String? data, bool? isBot}) {
    return CodeMessageModel(data: data ?? this.data, isBot: isBot ?? this.isBot);
  }
}
