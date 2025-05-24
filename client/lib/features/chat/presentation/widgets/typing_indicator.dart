import 'package:flutter/material.dart';

class TypingIndicator extends StatelessWidget {
  const TypingIndicator({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8, horizontal: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          SizedBox(
            width: 8,
            height: 8,
            child: CircularProgressIndicator(
              strokeWidth: 2,
              valueColor: AlwaysStoppedAnimation<Color>(
                theme.colorScheme.primary,
              ),
            ),
          ),
          SizedBox(width: 8),
          Text(
            "Bot is thinking...",
            style: TextStyle(color: theme.colorScheme.onSurface),
          ),
        ],
      ),
    );
  }
}
