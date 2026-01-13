import pytest
from src.ir.model import Pipeline, Operation
from src.ir.types import OpType
from src.generator.builder import RGenerator

class TestFilenameHandling:
    
    def test_uses_filename_parameter_if_present(self):
        """
        Scenario: Parser produces an internal ID (ds_001_inline) but provides
        the real filename in parameters ('demo_data.csv').
        
        The Generator MUST use 'demo_data.csv' for read_csv(), 
        not the internal ID.
        """
        ops = [
            Operation(
                id="op_load", 
                type=OpType.LOAD_CSV, 
                inputs=[], 
                outputs=["ds_001_inline"], # <--- The internal ID
                parameters={
                    "filename": "demo_data.csv", # <--- The real file
                    "format": "TXT"
                }
            )
        ]
        pipeline = Pipeline(datasets=[], operations=ops)
        
        generator = RGenerator(pipeline)
        code = generator.generate()
        
        # FAIL condition: read_csv("ds_001_inline")
        # PASS condition: read_csv("demo_data.csv")
        
        print("\nGenerated Code:", code) # For debugging
        
        assert 'read_csv("demo_data.csv")' in code
        assert 'read_csv("ds_001_inline")' not in code

    def test_fallbacks_to_id_if_parameter_missing(self):
        """
        Scenario: Old behavior. No filename param, so use the ID.
        """
        ops = [
            Operation(
                id="op_load_legacy", 
                type=OpType.LOAD_CSV, 
                inputs=[], 
                outputs=["raw_data.csv"],
                parameters={}
            )
        ]
        pipeline = Pipeline(datasets=[], operations=ops)
        generator = RGenerator(pipeline)
        code = generator.generate()
        
        assert 'read_csv("raw_data.csv")' in code