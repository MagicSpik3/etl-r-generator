import re

class RTranspiler:
    """
    Responsible for translating individual formula expressions into R/Tidyverse syntax.
    Handles semantic differences between SPSS/Legacy and R.
    """
    
    def __init__(self):
        # 1. Simple Replacements (Direct mapping)
        self.replacements = [
            # Operators
            (r"\s+AND\s+", " & "),
            (r"\s+OR\s+", " | "),
            (r"\s+<>\s+", " != "),
            # We must be careful with '='. In logic it's '=='. 
            # We assume assignments happen elsewhere (in mutate params), 
            # so '=' in an expression is likely equality.
            (r"(?<![<>!=])=(?![=])", "=="), 
            
            # Constants
            (r"\$SYSMIS", "NA"),
            
            # Math Functions (with optional spaces around parens)
            (r"TRUNC\s*\(", "floor("),
            (r"RND\s*\(", "round("),
            (r"ABS\s*\(", "abs("),
            (r"LAG\s*\(", "lag("),
            # String concatenation
            (r"CONCAT\s*\(", "paste0("),
        ]

    def transpile(self, expression: str) -> str:
        """
        Main entry point. Applies all translation rules.
        """
        if not expression:
            return "NA"

        result = expression

        # 0. Normalize spaces around parentheses in function arguments
        # This handles cases like "lag ( val )" -> "lag (val)" to make regex matching work
        result = self._normalize_function_calls(result)

        # 1. Apply Regex Replacements
        for pattern, replacement in self.replacements:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        # 2. Handle Special Functions (Argument Reordering)
        result = self._handle_mod(result)
        result = self._handle_dates(result)
        result = self._handle_sysmis(result)

        return result.strip()

    def _normalize_function_calls(self, expr: str) -> str:
        """
        Normalize spacing around function call parentheses.
        Converts "func ( arg )" to "func(arg)" for cleaner processing.
        Also normalizes spaces inside parentheses for consistency.
        """
        # Remove spaces between function name and opening paren
        expr = re.sub(r'(\w+)\s+\(', r'\1(', expr)
        # Remove spaces immediately after opening paren
        expr = re.sub(r'\(\s+', '(', expr)
        # Remove spaces immediately before closing paren (but preserve space before operators)
        expr = re.sub(r'\s+\)', ')', expr)
        # Normalize spaces around commas in arguments: multiple spaces -> single space after comma
        expr = re.sub(r'\s*,\s*', ', ', expr)
        return expr

    def _handle_mod(self, expr: str) -> str:
        """
        SPSS: MOD(a, b) -> R: a %% b
        """
        # Pattern: MOD(arg1, arg2) - handles spaces
        pattern = r"mod\s*\(([^,]+),\s*([^)]+)\)"
        
        def replace_mod(match):
            a = match.group(1).strip()
            b = match.group(2).strip()
            return f"{a} %% {b}"
            
        return re.sub(pattern, replace_mod, expr, flags=re.IGNORECASE)

    def _handle_dates(self, expr: str) -> str:
        """
        SPSS: DATE.MDY(m, d, y) -> R: make_date(year=y, month=m, day=d)
        """
        pattern = r"date\.mdy\s*\(([^,]+),\s*([^,]+),\s*([^)]+)\)"
        
        def replace_date(match):
            m = match.group(1).strip()
            d = match.group(2).strip()
            y = match.group(3).strip()
            return f"make_date(year={y}, month={m}, day={d})"
            
        return re.sub(pattern, replace_date, expr, flags=re.IGNORECASE)

    def _handle_sysmis(self, expr: str) -> str:
        """
        SPSS: SYSMIS(x) -> R: is.na(x)
        """
        return re.sub(r"sysmis\s*\(", "is.na(", expr, flags=re.IGNORECASE)