import 'package:flutter/material.dart';

class Agent extends StatefulWidget {
  final String agentName;
  final Icon icon;
  final String description;
  final VoidCallback onTap;

  const Agent({
    super.key,
    required this.agentName,
    required this.icon,
    required this.description,
    required this.onTap,
  });

  @override
  State<Agent> createState() => _AgentState();
}

class _AgentState extends State<Agent> {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      height: 200,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        border: Border.all(color: theme.colorScheme.outline),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(widget.icon.icon, size: 24, color: theme.colorScheme.onSurface),
          const SizedBox(height: 8),
          Text(
            widget.agentName,
            style: theme.textTheme.bodyLarge?.copyWith(
              color: theme.colorScheme.onSurface,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            widget.description,
            style: theme.textTheme.bodyMedium?.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
          ),
          const Spacer(),
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Icon(
                Icons.arrow_forward,
                size: 24,
                color: theme.colorScheme.onSurface,
              ),
            ],
          ),
        ],
      ),
    );
  }
}
