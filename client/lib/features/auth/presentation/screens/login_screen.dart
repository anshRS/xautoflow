import 'package:client/common/widgets/custom_button.dart';
import 'package:client/features/auth/presentation/widgets/auth_form_field.dart';
import 'package:flutter/material.dart';

class LogInScreen extends StatefulWidget {
  const LogInScreen({super.key});

  @override
  State<LogInScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<LogInScreen> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  final formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Flex(
            direction: Axis.vertical,
            children: [
              // Image section
              SizedBox(
                height: 460,
                child: Image.asset(
                  'assets/images/login_image.png',
                  fit: BoxFit.cover,
                ),
              ),

              // Form Fields section
              Form(
                key: formKey,
                child: Flex(
                  direction: Axis.vertical,
                  spacing: 24,
                  children: [
                    Column(
                      children: [
                        Text(
                          "Login",
                          style: theme.textTheme.headlineLarge?.copyWith(
                            color: theme.colorScheme.onSurface,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          "Welcome back you've been missed!",
                          style: theme.textTheme.bodyLarge?.copyWith(
                            color: theme.colorScheme.onSurfaceVariant,
                          ),
                        ),
                      ],
                    ),

                    Flex(
                      direction: Axis.vertical,
                      spacing: 16,
                      children: [
                        AuthFormField(
                          label: "Email",
                          hintText: "Enter you email",
                          isHidden: false,
                          icon: Icon(Icons.email_outlined),
                          controller: emailController,
                        ),
                        AuthFormField(
                          label: "Password",
                          hintText: "Enter you password",
                          isHidden: true,
                          icon: Icon(Icons.lock_outline),
                          controller: passwordController,
                        ),
                      ],
                    ),

                    CustomButton(text: "Login", onPressed: () {}),
                  ],
                ),
              ),
              const SizedBox(height: 8),
              Text.rich(
                TextSpan(
                  children: [
                    TextSpan(
                      text: "Don't have account? ",
                      style: theme.textTheme.bodyLarge?.copyWith(
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
                    ),
                    TextSpan(
                      text: "Create now",
                      style: theme.textTheme.bodyLarge?.copyWith(
                        color: theme.colorScheme.onSurfaceVariant,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
