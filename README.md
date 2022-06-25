# What's this ?
共同利用とクロスチェックを目的としたラマンスペクトル前処理コード群．必要に応じて機能が追加される予定です．ご自由にお使いください．

### **使い慣れていない方へ**
画面内緑色の「Code」から「Download ZIP」でダウンロード可能です．

### **コード共有やクロスチェック,GitHubの使い方に興味がある方へ**
それぞれの公開できる範囲で構いません．お気軽にご相談ください．GitHubの練習を兼ねてのプルリクも大歓迎です．

# 目次
説明は概要のみとなります．関数の仕様や説明などは[ドキュメント](https://lemniscatern.github.io/toraman/document/)をご覧ください．
- [機能](#機能)
   - [読み込み](#読み込み)
   - [バックグラウンドスペクトル除去](#バックグラウンドスペクトル除去)
   - [ベースライン処理](#ベースライン処理)
   - [その他](#その他)
- [利用方法](#利用方法)
- [Reference](#reference)


# 機能

## 読み込み
   load.~
   *  load_ascs : フォルダ内のascファイルをCell,Background,UnknownのDataFrameに分類．

## バックグラウンドスペクトル除去
   * (用意中..)

## ベースライン除去
   correct_baseline.~
   * pureASL : ASL[^1]による除去[^2].
   * arPLS : arPLS[^1]による除去[^2].
   * rolling_ball : ローリングボールによる除去

## その他
   sample_spectra.*
   * n_peaks_spectra : およそn頂点の模擬データをランダム生成
   * polynomial_baseline : n次多項式(風)のデータを生成

# 利用方法
sample.pyをご覧ください．
基本的にはraman_utilと同じ階層にmain.pyを設置して，使用するものをimportしてください．

```
from raman_util.correct_baseline import arPLS
```


# Reference
 
[^1]: [Baseline correction using asymmetrically reweighted penalized least squares smoothing](https://pubs.rsc.org/en/content/articlehtml/2015/an/c4an01061b)(Sung-June Baek a, Aaron Park *a, Young-Jin Ahn a and Jaebum Choo,2014)  
[^2]: [Python baseline correction library(stack over flow)](https://stackoverflow.com/questions/29156532/python-baseline-correction-library?answertab=createdasc#tab-top)  
[^3]: [Asymetrically reweighted penalized least squares](https://www.koreascience.or.kr/article/JAKO201913458198163.pdf)(Aa-Ron Park,Jun-Kyu Park,Dae-Young Ko,Sun-Geum Kim,Sung-June Baek,2019)
