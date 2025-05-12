import 'package:flutter/material.dart';

class ProfileFormField extends StatelessWidget {
  final String label;
  final String hintText;
  final Icon icon;
  final FormFieldValidator<String>? validator;

  final TextEditingController controller;
  final bool enabled;

  const ProfileFormField({
    super.key,
    required this.label,
    required this.hintText,
    required this.icon,
    required this.controller, 
    this.validator,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      enabled: enabled,
      decoration: InputDecoration(
        prefixIcon: icon,
        labelText: label,
        hintText: hintText,
        border: const OutlineInputBorder(),
        floatingLabelBehavior: FloatingLabelBehavior.always,
      ),
      validator: enabled ? validator : null,
    );
  }
}
