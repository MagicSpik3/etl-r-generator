import pytest
from src.ir.model import Pipeline, Operation, Dataset
from src.ir.types import OpType
from src.generator.builder import RGenerator

class TestRIO:
    
    def test_generates_load_csv(self):
        """
        Scenario: op outputs=['ds1'] -> ds1 <- read_csv('ds1')
        """
        ops = [
            Operation(
                id="load_op", 
                type=OpType.LOAD_CSV, 
                inputs=[], 
                outputs=["raw_data.csv"],
                parameters={}
            )
        ]
        # We assume the dataset ID is the filename for now
        pipeline = Pipeline(datasets=[], operations=ops)
        
        generator = RGenerator(pipeline)
        code = generator.generate()
        
        # Check for R assignment and read_csv
        # Escape dots for regex or just check string containment
        assert 'raw_data.csv <- read_csv("raw_data.csv")' in code

    def test_generates_save_csv(self):
        """
        Scenario: SAVE_BINARY -> write_csv(dataset, filename)
        """
        ops = [
            Operation(
                id="save_op", 
                type=OpType.SAVE_BINARY, 
                inputs=["final_dataset"], 
                outputs=["output_file.csv"], 
                parameters={}
            )
        ]
        pipeline = Pipeline(datasets=[], operations=ops)
        
        generator = RGenerator(pipeline)
        code = generator.generate()
        
        assert 'write_csv(final_dataset, "output_file.csv")' in code