import os
os.environ['TRANSFORMERS_NO_TF'] = '1'

print("Testing imports...")

try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}")
except Exception as e:
    print(f"❌ PyTorch: {e}")

try:
    import transformers
    print(f"✅ Transformers: {transformers.__version__}")
except Exception as e:
    print(f"❌ Transformers: {e}")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print("✅ Can import transformers classes")
except Exception as e:
    print(f"❌ Transformers classes: {e}")

try:
    import peft
    print(f"✅ PEFT: {peft.__version__}")
except Exception as e:
    print(f"❌ PEFT: {e}")

try:
    import google.protobuf
    print(f"✅ Protobuf: {google.protobuf.__version__}")
except Exception as e:
    print(f"❌ Protobuf: {e}")

print("\n✅ All imports successful!" if all else "⚠️ Some imports failed")
