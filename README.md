# 多普勒效應模擬器 - 挑戰模式

## 功能
本程式的核心功能是通過互動式模擬，幫助玩家深入理解多普勒效應的動態特性。通過調整參數，用戶可以觀察多普勒效應在不同速度和頻率下的波形變化，並學習音爆和馬赫波等現象。

### 具體功能
1. **參數調整與模擬觀察**
   - 玩家可以調整聲源頻率、聲源速度和觀察者速度，了解多普勒效應的動態變化。
   - 聲源速度等於音速（340 m/s）時，顯示靜態的音爆波形圖。
   - 聲源速度超過音速（> 340 m/s）時，顯示馬赫波並展示馬赫波夾角的大小。

2. **挑戰模式**
   - 程式會隨機生成一組聲源頻率、聲源速度和觀察者速度的挑戰題目。
   - 玩家通過多普勒效應公式計算觀察頻率，輸入答案並驗證正確性。
   - 玩家有三次機會，成功時顯示靜態波形圖作為獎勵；失敗時公布正確答案並顯示靜態波形圖。

---

## 使用方式
1. **下載**
   -pip intall tkinter
   -pip install numpy
   -pip install matplotlib
   
2. **參數調整：**
   - 使用滑桿或手動輸入方式調整聲源頻率（單位：Hz）、聲源速度和觀察者速度。
   - 滑桿與輸入框結合使用，確保精確控制。

3. **動態波形觀察：**
   - 調整完成後點擊開始鍵，顯示對應參數下的動態波形圖。
     - 聲源速度等於音速時：顯示靜態音爆波形圖。
     - 聲源速度超過音速時：顯示馬赫波並附加馬赫波夾角數據。

4. **挑戰模式：**
   - 點擊開始挑戰按鈕，程式隨機生成一組挑戰參數（聲源頻率、聲源速度和觀察者速度）。
   - 玩家計算觀察頻率，輸入答案後程式判斷正確性：
     - 成功：顯示靜態波形圖作為獎勵。
     - 失敗：顯示正確答案及靜態波形圖。
   - 玩家有三次答題機會。

5. **重置功能：**
   - 按下重置鍵恢復所有參數至默認值，進行新一輪模擬或挑戰。

---

## 程式架構

### 1. 多普勒效應計算模組
- **模擬模式：**
  - 根據輸入的聲源頻率、聲源速度和觀察者速度，計算觀察到的頻率。
  - 判斷音爆狀態（當聲源速度≥音速時）。

- **挑戰模式：**
  - 隨機生成挑戰參數，並計算目標觀察頻率。

### 2. 動態繪圖模組
- 使用 Matplotlib 繪製動態波形，包括音爆和馬赫波的動態顯示。
- 動態更新波形位置，展示聲源與觀察者的相對位置。

### 3. GUI 介面
- 使用 Tkinter 構建用戶介面，包括滑桿、輸入框及按鈕的互動功能。
- 提供直觀的參數調整及結果展示。

---

## 開發過程

### 初始功能開發
- 架構多普勒效應動態波形模擬器，初步實現聲源頻率與速度對波形的動態影響。
- 添加開始鍵，避免參數即時更新導致的不便。

### 優化用戶體驗
- 增加滑桿與輸入框的雙向互動。
- 添加成功挑戰者的靜態波形圖作為獎勵，失敗者顯示正確答案。

### 音爆與馬赫波優化
- 根據聲速閾值判斷條件，加入靜態音爆波形圖與馬赫波夾角計算功能。

### 挑戰模式設計
- 增加隨機生成挑戰題目功能，結合動態顯示進行反饋。
- 提升遊戲教育性及趣味性。

---

## 參考資料來源
1. **物理課本：**
   - 《Fundamentals of Physics》（Halliday, Resnick, Walker）：Chapter 17 - Waves II。
   - 參考多普勒效應公式、音爆與馬赫波的波圖、馬赫波夾角。

2. **ChatGPT：**
   - 提供程式基礎架構與邏輯設計。
   - 協助動態波形繪製、挑戰模式及音爆與馬赫波顯示功能。
   - 提供馬赫波夾角計算實現。
   - 对话内容：https://chatgpt.com/share/676a4176-f9ac-800c-92e3-fb25eb878e6c



---

## 修改與增強內容

### ChatGPT 的貢獻
- 初始架構設計，包括多普勒效應公式的實現及挑戰模式設計。
- 提供音爆與馬赫波的顯示邏輯及動態繪圖方案。

### 個人修改與優化
1. **用戶互動體驗：**
   - 添加開始鍵，避免即時更新問題。
   - 增加滑桿與輸入框的雙向控制功能。

2. **挑戰模式優化：**
   - 成功挑戰者顯示靜態波形圖作為獎勵。
   - 增加錯誤反饋，顯示正確答案與波形圖。

3. **功能穩定性改進：**
   - 修復參數調整引發的功能衝突（按下開始鍵後會把速度頻率值鎖定）。
   - 優化動態波形顯示流暢性。

4. **增強教育性功能：**
   - 增加馬赫波夾角計算，幫助用戶理解相關物理原理。

---
