import 'package:flutter/material.dart';

class CustomDrawerItem extends StatelessWidget {
  final String label;
  final IconData icon;
  final VoidCallback onTap;
  const CustomDrawerItem({
    super.key,
    required this.label,
    required this.icon,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 12),
      height: 56,
      child: ListTile(
        leading: Icon(icon),
        title: Text(label, style: TextStyle(fontWeight: FontWeight.normal)),
        onTap: onTap,
      ),
    );
  }
}
