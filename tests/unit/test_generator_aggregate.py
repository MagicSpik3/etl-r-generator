import pytest
from etl_r_generator.builder import RGenerator
from etl_ir.model import Pipeline, Operation
from etl_ir.types import OpType

class TestGeneratorAggregate:
    
    def setup_method(self):
        # Create a dummy pipeline to initialize the generator
        self.pipeline = Pipeline(metadata={}, datasets=[], operations=[])
        self.generator = RGenerator(self.pipeline)

    def test_standard_aggregation(self):
        """
        Scenario: Group by 'region' and calculate mean of 'sales'.
        """
        op = Operation(
            id="op_agg",
            type=OpType.AGGREGATE,
            inputs=["ds_input"],
            outputs=["ds_output"],
            parameters={
                "break": ["region"],
                "aggregations": ["mean_sales = MEAN(sales)"]
            }
        )
        
        # Call the private handler directly for unit testing
        self.generator._gen_aggregate(op)
        
        code = "\n".join(self.generator.lines)
        
        assert "ds_output <- ds_input %>%" in code
        assert "group_by(region) %>%" in code
        # Check if our naive robustifier worked (MEAN -> mean, added na.rm)
        assert "summarise(mean_sales = mean(sales, na.rm = TRUE))" in code

    def test_multi_key_aggregation(self):
        """
        Scenario: Group by multiple keys (region, year).
        """
        op = Operation(
            id="op_agg_multi",
            type=OpType.AGGREGATE,
            inputs=["ds_in"],
            outputs=["ds_out"],
            parameters={
                "break": ["region", "year"],
                "aggregations": ["total = SUM(amt)"]
            }
        )
        
        self.generator._gen_aggregate(op)
        code = "\n".join(self.generator.lines)
        
        assert "group_by(region, year) %>%" in code
        assert "summarise(total = sum(amt, na.rm = TRUE))" in code

    def test_distinct_aggregation(self):
        """
        Scenario: Aggregation with NO aggregation functions acts as 'DISTINCT'.
        """
        op = Operation(
            id="op_distinct",
            type=OpType.AGGREGATE,
            inputs=["ds_in"],
            outputs=["ds_out"],
            parameters={
                "break": ["id"],
                "aggregations": [] # Empty list
            }
        )
        
        self.generator._gen_aggregate(op)
        code = "\n".join(self.generator.lines)
        
        # Should use distinct() instead of summarise()
        assert "group_by" in code or "distinct(id)" in code
        assert "summarise" not in code