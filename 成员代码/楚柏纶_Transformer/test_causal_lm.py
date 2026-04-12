# test_causal_lm.py
import numpy as np
from config import CausalLMConfig
from model import CausalLM

def test_zero_input():
    config = CausalLMConfig(
        vocab_size=10, 
        hidden_size=8, 
        num_layers=2, 
        num_heads=2, 
        max_position_embeddings=16
    )
    model = CausalLM(config)
    
    # 按照用户要求：测试输入零tensor的情况
    # 将Embedding权重设为全0，这样无论输入什么ID，进入Block的都是零tensor
    model.embeddings = np.zeros((config.vocab_size, config.hidden_size))
    
    # 输入一组Token IDs
    input_ids = [0, 0, 0, 0]
    
    # 前向传播
    logits = model.forward(input_ids)
    
    print("Input sequence length:", len(input_ids))
    print("Vocab size:", config.vocab_size)
    print("Logits shape:", logits.shape)
    
    # 验证形状是否正确 [seq_len, vocab_size]
    assert logits.shape == (len(input_ids), config.vocab_size), f"Expected shape {(len(input_ids), config.vocab_size)}, but got {logits.shape}"

if __name__ == "__main__":
    try:
        test_zero_input()
    except Exception as e:
        exit(1)
