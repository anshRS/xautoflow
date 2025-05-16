import 'package:client/features/chat/presentation/widgets/message_bubble.dart';
import 'package:client/features/chat/presentation/widgets/prompt_input_field.dart';
import 'package:client/features/chat/presentation/widgets/typing_indicator.dart';
import 'package:flutter/material.dart';

class ChatScreen extends StatefulWidget {
  static route() => MaterialPageRoute(builder: (context) => const ChatScreen());

  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<Map<String, dynamic>> _messages = [
    {'text': 'Hello!', 'isBot': false},
    {'text': 'Hi there, how can I help you today?', 'isBot': true},
    {'text': 'Tell me a joke.', 'isBot': false},
    {'text': 'Why don’t scientists trust atoms? Because they make up everything.', 'isBot': true},
  ];

  bool _isBotTyping = false;

  void _handleSend(String text) {
    setState(() {
      _messages.insert(0, {'text': text, 'isBot': false});
      _isBotTyping = true;
    });

    Future.delayed(const Duration(seconds: 2), () {
      setState(() {
        _messages.insert(0, {'text': 'Mock bot reply to "$text"', 'isBot': true});
        _isBotTyping = false;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Realtime Chat'),
        
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              reverse: true,
              itemCount: _messages.length + (_isBotTyping ? 1 : 0),
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              itemBuilder: (context, index) {
                if (_isBotTyping && index == 0) {
                  return const TypingIndicator();
                }

                final message = _messages[_isBotTyping ? index - 1 : index];                
                return MessageBubble(
                  text: message['text'],
                  isBot: message['isBot'],
                );
              },
            ),
          ),
          PromptInputField(onSend: _handleSend),
        ],
      ),
    );
  }
}
