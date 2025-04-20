import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final bool isLoading;
  final bool isOutlined;
  final bool isText;
  final Color? backgroundColor;
  final Color? textColor;
  final double? width;
  final double? height;
  final double borderRadius;
  final IconData? icon;
  final double? iconSize;

  const CustomButton({
    Key? key,
    required this.text,
    required this.onPressed,
    this.isLoading = false,
    this.isOutlined = false,
    this.isText = false,
    this.backgroundColor,
    this.textColor,
    this.width,
    this.height,
    this.borderRadius = 12,
    this.icon,
    this.iconSize,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    if (isText) {
      return TextButton(
        onPressed: isLoading ? null : onPressed,
        style: TextButton.styleFrom(
          foregroundColor: textColor ?? theme.colorScheme.primary,
          padding: EdgeInsets.symmetric(
            horizontal: width != null ? width! / 4 : 16,
            vertical: height != null ? height! / 3 : 8,
          ),
        ),
        child: _buildChild(theme),
      );
    }
    
    if (isOutlined) {
      return OutlinedButton(
        onPressed: isLoading ? null : onPressed,
        style: OutlinedButton.styleFrom(
          foregroundColor: textColor ?? theme.colorScheme.primary,
          side: BorderSide(color: textColor ?? theme.colorScheme.primary),
          padding: EdgeInsets.symmetric(
            horizontal: width != null ? width! / 4 : 24,
            vertical: height != null ? height! / 3 : 12,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(borderRadius),
          ),
        ),
        child: _buildChild(theme),
      );
    }
    
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: backgroundColor ?? theme.colorScheme.primary,
        foregroundColor: textColor ?? Colors.white,
        padding: EdgeInsets.symmetric(
          horizontal: width != null ? width! / 4 : 24,
          vertical: height != null ? height! / 3 : 12,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(borderRadius),
        ),
      ),
      child: _buildChild(theme),
    );
  }
  
  Widget _buildChild(ThemeData theme) {
    if (isLoading) {
      return SizedBox(
        width: 24,
        height: 24,
        child: SpinKitDoubleBounce(
          color: isOutlined || isText
              ? (textColor ?? theme.colorScheme.primary)
              : Colors.white,
          size: 24,
        ),
      );
    }
    
    if (icon != null) {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: iconSize ?? 20,
            color: isOutlined || isText
                ? (textColor ?? theme.colorScheme.primary)
                : Colors.white,
          ),
          const SizedBox(width: 8),
          Text(text),
        ],
      );
    }
    
    return Text(text);
  }
}
