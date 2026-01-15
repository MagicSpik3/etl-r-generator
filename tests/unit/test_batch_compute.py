import pytest
from etl_ir.model import Pipeline, Operation
from etl_ir.types import OpType
from src.generator.builder import RGenerator

class TestRBatchCompute:
    
    def test_generates_single_mutate_for_batch(self):
        """
        Scenario: A BATCH_COMPUTE op with 2 calculations.
        IR: 
          params={
            'computes': [
               {'target': 'age_years', 'expression': 'TRUNC(age)'},
               {'target': 'is_adult', 'expression': 'age >= 18'}
            ]
          }
        
        Expected R:
          ds2 <- ds1 %>%
            mutate(
              age_years = floor(age),
              is_adult = age >= 18
            )
        """
        ops = [
            Operation(
                id="batch_op", 
                type=OpType.BATCH_COMPUTE, 
                inputs=["ds1"], 
                outputs=["ds2"], 
                parameters={
                    "computes": [
                        {"target": "age_years", "expression": "TRUNC(age)"},
                        {"target": "is_adult", "expression": "age >= 18"}
                    ]
                }
            )
        ]
        pipeline = Pipeline(datasets=[], operations=ops)
        generator = RGenerator(pipeline)
        code = generator.generate()
        
        # We verify the structure. 
        # Note: Whitespace matching in tests can be tricky, so we check for key phrases
        assert "ds2 <- ds1 %>%" in code
        assert "mutate(" in code
        assert "age_years = floor(age)" in code
        assert "is_adult = age >= 18" in code