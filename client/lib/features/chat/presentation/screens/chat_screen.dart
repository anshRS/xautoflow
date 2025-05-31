import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/common/widgets/message_bubble.dart';
import 'package:client/common/widgets/prompt_input_field.dart';
import 'package:client/common/widgets/typing_indicator.dart';
import 'package:client/features/chat/presentation/bloc/chat_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class ChatScreen extends StatefulWidget {
  static route() => MaterialPageRoute(builder: (context) => const ChatScreen());

  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  late ChatBloc _chatBloc;

  @override
  void initState() {
    super.initState();

    final user = (context.read<AppUserCubit>().state as AppUserLoggedIn).user;    
    context.read<ChatBloc>().add(ConnectChatEvent(user.id));
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _chatBloc = context.read<ChatBloc>();
  }

  @override
  void dispose() {
    _chatBloc.add(DisconnectChatEvent());
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Realtime Chat')),
      body: BlocBuilder<ChatBloc, ChatState>(
        builder: (context, state) {
          return Column(
            children: [
              Expanded(
                child: ListView.builder(
                  reverse: true,
                  itemCount: state.messages.length,
                  padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  itemBuilder: (context, index) {
                    final message = state.messages[index];
                    return MessageBubble(text: message.data, isBot: message.isBot!);
                  },
                ),
              ),
              if (state.isTyping) TypingIndicator(),
              PromptInputField(
                isTyping: state.isTyping,
                onSend: (text) {
                  context.read<ChatBloc>().add(SendMessageEvent(text));
                },
              ),
            ],
          );
        },
      ),
    );
  }
}
