## CUDA
NVIDIA GPUにグラフィック以外の計算処理をさせるライブラリです。  
[こちら](https://developer.nvidia.com/cuda-toolkit-archive)から`CUDA Toolkit 11.8.0`をDL & インストール(12.0.0以降はPyTorchが未対応)


## PyTorch
ディープラーニングをPythonで行うためのライブラリです。  
CPU版もありますがCUDA(GPU)版の方がはるかに高速です。
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---
参考
- https://pytorch.org/get-started/locally/