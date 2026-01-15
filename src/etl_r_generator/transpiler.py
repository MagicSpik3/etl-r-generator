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
            
            # Math Functions
            (r"TRUNC\(", "floor("),
            (r"RND\(", "round("),
            (r"ABS\(", "abs("),
        ]

    def transpile(self, expression: str) -> str:
        """
        Main entry point. Applies all translation rules.
        """
        if not expression:
            return "NA"

        result = expression

        # 1. Apply Regex Replacements
        for pattern, replacement in self.replacements:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        # 2. Handle Special Functions (Argument Reordering)
        result = self._handle_mod(result)
        result = self._handle_dates(result)
        result = self._handle_sysmis(result)

        return result.strip()

    def _handle_mod(self, expr: str) -> str:
        """
        SPSS: MOD(a, b) -> R: a %% b
        """
        # Pattern: MOD(arg1, arg2)
        pattern = r"MOD\(([^,]+),\s*([^)]+)\)"
        
        def replace_mod(match):
            a = match.group(1).strip()
            b = match.group(2).strip()
            return f"{a} %% {b}"
            
        return re.sub(pattern, replace_mod, expr, flags=re.IGNORECASE)

    def _handle_dates(self, expr: str) -> str:
        """
        SPSS: DATE.MDY(m, d, y) -> R: make_date(year=y, month=m, day=d)
        """
        pattern = r"DATE\.MDY\(([^,]+),\s*([^,]+),\s*([^)]+)\)"
        
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
        return re.sub(r"SYSMIS\(", "is.na(", expr, flags=re.IGNORECASE)