## CUDA
NVIDIA GPUにグラフィック以外の計算処理をさせるライブラリです。  
[こちら](https://developer.nvidia.com/cuda-toolkit-archive)から`CUDA Toolkit 11.8.0`をDL & インストール(12.0.0以降はPyTorchが未対応)


## PyTorch
ディープラーニングをPythonで行うためのライブラリです。  
CPU版もありますが今回はCUDA(GPU)版が必要です。
```
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### トラブルシューティング
```
AssertionError: Torch not compiled with CUDA enabled
```
このケースではCPU版のPyTorchが認識されております。  
CPU版を削除してGPU版をインストールする必要があります
```
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---
参考
- https://pytorch.org/get-started/locally/