import pytest
from etl_r_generator.builder import RGenerator
from etl_ir.model import Pipeline, Operation
from etl_ir.types import OpType

def test_full_generation_cycle():
    """
    Scenario: Load -> Aggregate -> Save.
    Goal: Verify the generator produces a complete, valid R script.
    """
    # 1. Construct a mini pipeline
    ops = [
        Operation(
            id="op_1", type=OpType.LOAD_CSV, 
            inputs=[], outputs=["ds_raw"], 
            parameters={"filename": "data.csv"}
        ),
        Operation(
            id="op_2", type=OpType.AGGREGATE, 
            inputs=["ds_raw"], outputs=["ds_agg"], 
            parameters={
                "break": ["category"],
                "aggregations": ["max_val = MAX(val)"]
            }
        ),
        Operation(
            id="op_3", type=OpType.SAVE_BINARY, 
            inputs=["ds_agg"], outputs=["file_out"], 
            parameters={"filename": "output.csv"}
        )
    ]
    
    pipeline = Pipeline(metadata={"generator": "TestBot"}, datasets=[], operations=ops)
    
    # 2. Run the Generator
    generator = RGenerator(pipeline)
    r_script = generator.generate()
    
    print("\n👇 Generated R Script 👇")
    print(r_script)
    
    # 3. Assertions
    assert "library(tidyverse)" in r_script
    assert "ds_raw <- read_csv" in r_script
    
    # Check if the Aggregate block was generated
    assert "ds_agg <- ds_raw %>%" in r_script
    assert "group_by(category)" in r_script
    assert "summarise(max_val = max(val, na.rm = TRUE))" in r_script
    
    # Check if the chain continues to the Save op
    assert 'write_csv(ds_agg, "output.csv")' in r_script