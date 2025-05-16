import 'package:flutter/material.dart';

class MessageBubble extends StatelessWidget {
  final String text;
  final bool isBot;

  const MessageBubble({super.key, required this.text, required this.isBot});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    // final alignment = isBot ? CrossAxisAlignment.start : CrossAxisAlignment.end;
    final bgColor =
        isBot
            ? theme.colorScheme.surfaceContainerHighest
            : theme.colorScheme.secondary;
    final fgColor =
        isBot
            ? theme.colorScheme.onSurfaceVariant
            : theme.colorScheme.onSecondary;
    final radius =
        isBot
            ? const BorderRadius.only(
              topLeft: Radius.circular(20),
              topRight: Radius.circular(20),
              bottomLeft: Radius.circular(8),
              bottomRight: Radius.circular(20),
            )
            : const BorderRadius.only(
              topLeft: Radius.circular(20),
              topRight: Radius.circular(20),
              bottomLeft: Radius.circular(20),
              bottomRight: Radius.circular(8),
            );

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 4),
      child: SingleChildScrollView(
        child: Column(
          // crossAxisAlignment: alignment,
          children: [
            Row(
              mainAxisAlignment:
                  isBot ? MainAxisAlignment.start : MainAxisAlignment.end,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (isBot)
                  CircleAvatar(
                    backgroundColor: theme.colorScheme.secondary,
                    child: Icon(
                      Icons.smart_toy,
                      color: theme.colorScheme.onSecondary,
                    ),
                  ),
                const SizedBox(width: 8),
                Flexible(
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 16,
                    ),
                    decoration: BoxDecoration(
                      color: bgColor,
                      borderRadius: radius,
                    ),
                    child: Text(text, style: TextStyle(color: fgColor)),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
