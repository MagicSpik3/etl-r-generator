import argparse
import yaml
import sys
from pathlib import Path

# Ensure src is in python path
sys.path.append('src')

from src.ir.model import Pipeline
from src.generator.builder import RGenerator

def main():
    parser = argparse.ArgumentParser(description="ETL R Generator: YAML -> Tidyverse")
    parser.add_argument("input_file", type=str, help="Path to Optimized Logical IR (YAML)")
    parser.add_argument("--output", "-o", type=str, help="Output path for .R script", required=True)
    
    args = parser.parse_args()
    
    # 1. Load YAML
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}")
        sys.exit(1)
        
    print(f"🔄 Loading Logical IR from {input_path}...")
    with open(input_path, "r") as f:
        data = yaml.safe_load(f)
    
    # 2. Hydrate Model
    try:
        pipeline = Pipeline(**data)
    except Exception as e:
        print(f"❌ Error: Invalid IR format. {e}")
        sys.exit(1)

    # 3. Generate R
    print("🧠 Transpiling to R (Tidyverse)...")
    generator = RGenerator(pipeline)
    r_code = generator.generate()
    
    # 4. Write Output
    output_path = Path(args.output)
    with open(output_path, "w") as f:
        f.write(r_code)
        
    print(f"✅ Success! Generated R script at: {output_path}")
    print(f"   Lines of code: {len(r_code.splitlines())}")

if __name__ == "__main__":
    main()