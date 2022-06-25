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
   - [その他](#その他)
- [利用方法](#利用方法)
- [Reference](#reference)


# 機能

## 読み込み
| 関数名 | 機能 | 引数 | 戻り値 |補足 | 
| - | - | - | - | - |
| load_ascs.load_ascs | 指定フォルダ内のascファイルの一括読み込み+サンプル/バックグラウンド/不明データの分類 | dirname:str=None,filepath:str=None,noreturn_unknown_data :bool=True,sep="\t" | cell_df,background_df,(unknown_df) |「\* quartz\* .asc」,「\* water\* .asc」，「\* _(数字).asc」の3種類で分割 | 



## バックグラウンドスペクトル除去
| 関数名 | 機能 | 補足 | 
| - |- | - | 



## ベースライン処理
| 関数名 | 機能 | 引数 | 戻り値 |補足 | 
| - | - | - | - | - |
| pureASL.pureASL| ASL法[^1],[^2]によるベースライン補正|Data:list,lam:int=10**3.5,p:float =0.00005,repeat_max:int=10,show_process    :bool=False|corrected_baseline| 
| arPLS.arPLS    | arPLS法[^1],[^2]によるベースライン補正|Data:list,lam:int=1e4,ratio:float=1e-6,loop_max:int=10, show_process:bool=False,full_output:bool=False,guess_baseline_order:int=None|corrected_baseline,(estimate_baseline,info)|最適化オプション[^3]を利用する場合,形状から推定されるベースラインの次数をguess_baseline_orderに渡す| 



## その他
| 関数名 | 機能 | 引数 | 戻り値 |補足 | 
| - | - | - | - | - |
|sample_spectra.n_peaks_spectra| n頂点のピークがランダムな場所にあるデータを生成|x,n=3,seed=0|spectra|
|sample_spectra.polynomial_baseline| degree多項式の曲線を生成|x,degree=3|generated_baseline|degreeに応じて形状は固定|




# 利用方法
sample.pyをご覧ください．

基本的にはraman_utilと同じ階層にmain.pyを設置して，使用するものをimportしてください．
* from raman_util.pureASL import pureASL
* from raman_util.sample_spectra import n_peaks_spectra,polynomial_baseline
* from raman_util.arPLS import arPLS

# Reference
[^1]: [Python baseline correction library(stack over flow)](https://stackoverflow.com/questions/29156532/python-baseline-correction-library?answertab=createdasc#tab-top)  
[^2]: [Baseline correction using asymmetrically reweighted penalized least squares smoothing](https://pubs.rsc.org/en/content/articlehtml/2015/an/c4an01061b)(Sung-June Baek a, Aaron Park *a, Young-Jin Ahn a and Jaebum Choo,2014)  
[^3]: [Asymetrically reweighted penalized least squares](https://www.koreascience.or.kr/article/JAKO201913458198163.pdf)(Aa-Ron Park,Jun-Kyu Park,Dae-Young Ko,Sun-Geum Kim,Sung-June Baek,2019)