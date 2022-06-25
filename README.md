# What's this ?
共同利用とクロスチェックを目的としたラマンスペクトル前処理コード群．必要に応じて機能が追加される予定です．ご自由にお使いください．

### **使い慣れていない方へ**
画面内緑色の「Code」から「Download ZIP」でダウンロード可能です．

### **コード共有やクロスチェック,GitHubの使い方に興味がある方へ**
それぞれの公開できる範囲で構いません．お気軽にご相談ください．GitHubの練習を兼ねてのプルリクも大歓迎です．

# 目次
- [機能](#機能)
   - [読み込み](#読み込み)
   - [バックグラウンドスペクトル除去](#バックグラウンドスペクトル除去)(用意中..)
   - [ベースライン処理](#ベースライン処理)
- [利用方法](#利用方法)
- [Reference](#reference)


# 機能

## 読み込み
| 関数名 | 機能 | 補足 | 
| - |- | - | 
| loadascs | 指定フォルダ内のascファイルの一括読み込み+サンプル/バックグラウンド/不明データの分類 | 「\* quartz\* .asc」,「\* water\* .asc」，「\* _(数字).asc」の3種類で分割 | 

## バックグラウンドスペクトル除去
| 関数名 | 機能 | 補足 | 
| - |- | - | 

## ベースライン処理
| 関数名 | 機能 | 補足 | 
| - |- | - | 
| pureASL  | ASL法[^1],[^2]によるベースライン補正|| 
| arPLS    | arPLS法[^1],[^2]によるベースライン補正|最適化オプション[^3]を利用する場合,形状から推定されるベースラインの次数をguess_baseline_orderに渡す| 


# 利用方法
1. 利用したい.pyファイル(main.py)と同じディレクトリ内にraman_utilフォルダを設置

```
.
├──  sample.py
└─── raman_util
   └── (省略)
```

2. main.pyにて必要なモジュールをimport,実行

```python:sample.py
#from raman_util import *
#from raman_util import loadascs,pureASL

from raman_util.arPLS import arPLS
from raman_util.sample_spectra import n_peaks_spectra,polynomial_baseline

#generate simulated data
x = np.arange(0,1000)
y = n_peaks_spectra(x,n=3,seed=0) + polynomial_baseline(x,degree=3)

#correct and show process
correct = arPLS(y,show_process=True,guess_baseline_order=3)
```

# Reference
[^1]: [Python baseline correction library(stack over flow)](https://stackoverflow.com/questions/29156532/python-baseline-correction-library?answertab=createdasc#tab-top)  
[^2]: [Baseline correction using asymmetrically reweighted penalized least squares smoothing](https://pubs.rsc.org/en/content/articlehtml/2015/an/c4an01061b)(Sung-June Baek a, Aaron Park *a, Young-Jin Ahn a and Jaebum Choo,2014)  
[^3]: [Asymetrically reweighted penalized least squares](https://www.koreascience.or.kr/article/JAKO201913458198163.pdf)(Aa-Ron Park,Jun-Kyu Park,Dae-Young Ko,Sun-Geum Kim,Sung-June Baek,2019)