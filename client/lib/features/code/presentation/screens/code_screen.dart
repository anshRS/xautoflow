
import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/common/widgets/message_bubble.dart';
import 'package:client/common/widgets/prompt_input_field.dart';
import 'package:client/common/widgets/typing_indicator.dart';
import 'package:client/features/code/presentation/bloc/code_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class CodeScreen extends StatefulWidget {
  static route() => MaterialPageRoute(builder: (context) => const CodeScreen());

  const CodeScreen({super.key});

  @override
  State<CodeScreen> createState() => _CodeScreenState();
}

class _CodeScreenState extends State<CodeScreen> {
  late CodeBloc _chatBloc;

  @override
  void initState() {
    super.initState();

    final user = (context.read<AppUserCubit>().state as AppUserLoggedIn).user;    
    context.read<CodeBloc>().add(ConnectCodeEvent(user.id));
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _chatBloc = context.read<CodeBloc>();
  }

  @override
  void dispose() {
    _chatBloc.add(DisconnectCodeEvent());
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Coding')),
      body: BlocBuilder<CodeBloc, CodeState>(
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
                  context.read<CodeBloc>().add(SendMessageEvent(text));
                },
              ),
            ],
          );
        },
      ),
    );
  }
}
