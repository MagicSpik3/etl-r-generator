import pytest
from src.ir.model import Pipeline, Operation
from src.ir.types import OpType
from src.generator.builder import RGenerator

class TestRStructuralOps:
    
    def test_generates_filter(self):
        """
        Scenario: Filter rows based on a condition.
        IR: inputs=['ds1'], outputs=['ds2'], params={'condition': 'age > 18'}
        R: ds2 <- ds1 %>% filter(age > 18)
        """
        ops = [
            Operation(
                id="filter_op", 
                type=OpType.FILTER, 
                inputs=["ds1"], 
                outputs=["ds2"], 
                parameters={"condition": "age > 18"}
            )
        ]
        pipeline = Pipeline(datasets=[], operations=ops)
        generator = RGenerator(pipeline)
        code = generator.generate()
        
        expected = "ds2 <- ds1 %>% filter(age > 18)"
        assert expected in code

    def test_generates_sort(self):
        """
        Scenario: Sort rows.
        IR: inputs=['ds1'], outputs=['ds2'], params={'keys': 'age, date'}
        R: ds2 <- ds1 %>% arrange(age, date)
        """
        ops = [
            Operation(
                id="sort_op", 
                type=OpType.SORT, 
                inputs=["ds1"], 
                outputs=["ds2"], 
                parameters={"keys": "age, date"}
            )
        ]
        pipeline = Pipeline(datasets=[], operations=ops)
        generator = RGenerator(pipeline)
        code = generator.generate()
        
        expected = "ds2 <- ds1 %>% arrange(age, date)"
        assert expected in code

    def test_generates_join(self):
        """
        Scenario: Join two datasets.
        IR: inputs=['left', 'right'], outputs=['joined']
        R: joined <- left %>% inner_join(right)
        """
        ops = [
            Operation(
                id="join_op", 
                type=OpType.JOIN, 
                inputs=["ds_left", "ds_right"], 
                outputs=["ds_joined"], 
                parameters={} 
            )
        ]
        pipeline = Pipeline(datasets=[], operations=ops)
        generator = RGenerator(pipeline)
        code = generator.generate()
        
        expected = "ds_joined <- ds_left %>% inner_join(ds_right)"
        assert expected in code