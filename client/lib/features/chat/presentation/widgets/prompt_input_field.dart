import 'package:flutter/material.dart';

class PromptInputField extends StatefulWidget {
  final void Function(String) onSend;
  final bool isTyping;

  const PromptInputField({
    super.key,
    required this.onSend,
    required this.isTyping,
  });

  @override
  State<PromptInputField> createState() => _PromptInputFieldState();
}

class _PromptInputFieldState extends State<PromptInputField> {
  final _controller = TextEditingController();

  void _submit() {
    final text = _controller.text.trim();
    if (text.isNotEmpty) {
      widget.onSend(text);
      _controller.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return SafeArea(
      child: Container(
        decoration: BoxDecoration(color: theme.colorScheme.surfaceContainer),
        padding: const EdgeInsets.fromLTRB(0, 16, 16, 16),
        child: Row(
          children: [
            IconButton(
              icon: const Icon(Icons.emoji_emotions_outlined),
              onPressed: () {}, // Emoji picker placeholder
            ),
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 4),
                decoration: BoxDecoration(
                  color: theme.colorScheme.surfaceContainerHigh,
                  borderRadius: BorderRadius.circular(28),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(
                      width: 48,
                      height: 48,
                      child: Icon(
                        Icons.text_fields,
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
                    ),
                    Expanded(
                      child: TextField(
                        controller: _controller,
                        enabled: !widget.isTyping,
                        decoration: const InputDecoration(
                          hintText: 'Type something here...',
                          border: InputBorder.none,
                        ),
                        onSubmitted: (_) => _submit(),
                      ),
                    ),
                    SizedBox(
                      width: 48,
                      height: 48,
                      child: IconButton(
                        icon: const Icon(Icons.send),
                        onPressed: widget.isTyping ? null : _submit,
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
