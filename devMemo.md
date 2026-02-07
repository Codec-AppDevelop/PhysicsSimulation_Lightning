# 稲妻シミュレーション

## 方法

### 手法比較

雷のシミュレーションに関する手法の違いは[参考サイト](https://qiita.com/chromia/items/7bda3dd4338bee964f97)を参照。
今回は理論に基づくDBM(Dielectric Breakdown Model)をベースとした高速手法を採用する。

### 文献要約

ここでは[参考文献](laplacian_large.pdf)（Theodore Kim et al., "Fast Simulation of Laplacian Growth", IEEE Computer Graphics and Applications, Vol. 27, No. 2, 2007）の内容を要約する。

#### Dielectric Breakdown Model

- DBMの計算プロセスは以下の３ステップ

  1. 電位ポテンシャルを計算
  2. ポテンシャルに従い進行するグリッドを選択
  3. 進行されたグリッドを境界条件に追加

- 境界条件として負電位（$ \phi = 0 $）と正電位（$ \phi = 1 $）を定義する
- 各グリッドの電位ポテンシャルを下記ラプラス方程式を解くことで計算する
  $$ \nabla^2\phi = 0 $$
- 進行グリッドを電位ポテンシャルに基づく確率分布から計算する
  $$ p_i = \frac{ (\phi_i)^\eta }{ \Sigma^n_{j=1} (\phi_j)^\eta } $$
  $ p_i $ は $ i $ 番目の進行候補地点の確率、 $ n $ は進行候補地点の個数、$ \eta $ は図形の広がりやすさを表す変数（ $ 0 \leq \eta \leq 4 $ ）

#### Fast Simulation for DBM

- 従来のDBMは電位ポテンシャルの計算にメモリ・時間を要する
- 本文献で提案するアルゴリズムは以下の通り

  1. スタートポイントを設定
  2. 候補ポイントを設定（隣接グリッド）
  3. 各候補ポイントの電位ポテンシャルを下式で計算
     $$ \phi_i = \sum^n_{j=0} \left( c_1 - \frac{c_2}{r_{i,j}} \right) $$
     $$ c_1 = - \left( \frac{R_1}{R_2} - 1 \right)^{-1}, c_2 = \left( \frac{1}{R_2} - \frac{1}{R_1} \right)^{-1} $$
     $ R_1 $ はグリッドに配置される電荷を球とした時の半径で、グリッド高さの半分。
     $ r_{i,j} $ はグリッド $ i $ から電荷 $ j $ までの距離であり、$ n $ は電荷の合計数
  4. 下式で表される確立に基づき進行グリッドを決定
     $$ p_i = \frac{ (\Phi_i)^\eta }{ \Sigma^n_{j=1} (\Phi_j)^\eta } $$
     $$ \Phi_i = \frac{\phi_i - \phi_{min}}{\phi_{max} - √} $$
     $ p_i $ は $ i $ 番目の進行候補地点の確率、 $ n $ は進行候補地点の個数、$ \eta $ は図形の広がりやすさを表す変数（ $ 0 \leq \eta \leq 4 $ ）
  5. 下式により全ての候補点の電位ポテンシャルを更新する
     $$ \phi^{t+1}_i = \phi^t_i + \left( c_1 - \frac{c_2}{r_{i,t+1}} \right) $$
     $ \phi^t_i $ はグリッド $ i $ の、時間ステップ $ t $ における電位ポテンシャル。
     この式は、電位ポテンシャルの更新は１ステップ前の電位ポテンシャルに追加した電位分のポテンシャルを足し合わせることで行うことを表している。
  6. 候補ポイントを更新
  7. 追加した候補ポイントの電位ポテンシャルを 3. と同じ方法で計算する
  8. 4~7 を繰り返す

## 環境構築

### Python仮想環境

仮想環境を以下のコマンドで作成

```terminal
python3 -m venv .PhysSim_Lightning
```

以下のコマンドでアクティベート

```terminal
. ./.PhysSim_Lightning/bin/activate
```

ディアクティベートする場合は以下のコマンド

```terminal
deactivate
```

### ライブラリ
