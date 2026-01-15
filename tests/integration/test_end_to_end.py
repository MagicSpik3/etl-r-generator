import pytest
from etl_ir.model import Pipeline, Operation
from etl_ir.types import OpType
from src.generator.builder import RGenerator

class TestEndToEnd:
    
    def test_generates_complex_pipeline(self):
        """
        Scenario: A realistic chain containing Load -> Filter -> BatchCompute -> Join -> Save.
        """
        ops = [
            # 1. Load
            Operation(id="op1", type=OpType.LOAD_CSV, inputs=[], outputs=["raw.csv"]),
            
            # 2. Batch Compute (The heavy lifting)
            Operation(
                id="op2", 
                type=OpType.BATCH_COMPUTE, 
                inputs=["raw.csv"], 
                outputs=["derived"],
                parameters={
                    "computes": [
                        {"target": "age_years", "expression": "TRUNC(age)"},
                        {"target": "is_valid", "expression": "SYSMIS(status)"}
                    ]
                }
            ),
            
            # 3. Filter
            Operation(
                id="op3",
                type=OpType.FILTER_ROWS,
                inputs=["derived"],
                outputs=["filtered"],
                parameters={"condition": "is_valid = 0"} # 0 = False in old system
            ),
            
            # 4. Save
            Operation(id="op4", type=OpType.SAVE_BINARY, inputs=["filtered"], outputs=["clean.csv"])
        ]
        
        pipeline = Pipeline(
            metadata={"generator": "Integration Test"},
            datasets=[],
            operations=ops
        )
        
        generator = RGenerator(pipeline)
        r_script = generator.generate()
        
        print("\n--- Generated R Script ---")
        print(r_script)
        print("--------------------------")
        
        # Assertions
        assert "derived <- raw.csv %>%" in r_script
        assert "mutate(" in r_script
        assert "floor(age)" in r_script      # Transpiler check
        assert "is.na(status)" in r_script   # Transpiler check
        assert "filter(" in r_script
        assert "write_csv" in r_script