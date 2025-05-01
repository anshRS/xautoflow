import 'package:client/common/widgets/custom_button.dart';
import 'package:client/features/auth/presentation/screens/login_screen.dart';
import 'package:flutter/material.dart';

class VerifyEmailScreen extends StatelessWidget {
  final String email;

  static route(String email) =>
      MaterialPageRoute(builder: (context) => VerifyEmailScreen(email: email));

  const VerifyEmailScreen({super.key, required this.email});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        actions: [
          IconButton(
            onPressed: () => Navigator.pushAndRemoveUntil(context, LogInScreen.route(), (route) => false),
            icon: Icon(Icons.clear),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              "Verify your email address!",
              style: theme.textTheme.headlineSmall?.copyWith(
                color: theme.colorScheme.onSurface,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              email,
              style: theme.textTheme.bodyLarge?.copyWith(
                color: theme.colorScheme.onSurface,
                fontWeight: FontWeight.w500,
              ),
            ),

            const SizedBox(height: 16),

            Text(
              "We've sent a link to your email. Click it to verify your account.",
              textAlign: TextAlign.center,
              style: theme.textTheme.bodyLarge?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
            ),

            const SizedBox(height: 32),

            CustomButton(
              text: "Continue",
              onPressed: () {
                Navigator.pushAndRemoveUntil(
                  context,
                  LogInScreen.route(),
                  (route) => false,
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
