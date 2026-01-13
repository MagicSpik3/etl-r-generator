import pytest
from src.generator.transpiler import RTranspiler

class TestRTranspiler:
    
    def setup_method(self):
        self.transpiler = RTranspiler()

    def test_translates_math_functions(self):
        """
        Scenario: TRUNC -> floor, MOD -> %%
        """
        assert self.transpiler.transpile("TRUNC(age)") == "floor(age)"
        assert self.transpiler.transpile("MOD(x, 10)") == "x %% 10"
        # RND is roughly round, but usually we want standard rounding
        assert self.transpiler.transpile("RND(salary)") == "round(salary)"

    def test_translates_logic_operators(self):
        """
        Scenario: AND/OR -> & / |, = -> ==
        """
        # Note: We need to be careful not to replace '=' inside function calls if possible,
        # but for simple boolean logic:
        assert self.transpiler.transpile("x = 1 AND y = 2") == "x == 1 & y == 2"
        assert self.transpiler.transpile("a <> b") == "a != b"
        assert self.transpiler.transpile("age >= 18 OR status = 'Active'") == "age >= 18 | status == 'Active'"

    def test_translates_missing_values(self):
        """
        Scenario: SYSMIS handling.
        """
        # Function check
        assert self.transpiler.transpile("SYSMIS(x)") == "is.na(x)"
        # Constant check
        assert self.transpiler.transpile("$SYSMIS") == "NA"

    def test_translates_date_constructors(self):
        """
        Scenario: DATE.MDY(m, d, y) -> make_date(year=y, month=m, day=d)
        This requires re-ordering arguments!
        """
        # Input: Month, Day, Year
        expression = "DATE.MDY(12, 31, 2024)"
        # Output: Year, Month, Day (Lubridate standard)
        expected = "make_date(year=2024, month=12, day=31)"
        
        assert self.transpiler.transpile(expression) == expected