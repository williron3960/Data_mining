# DataMining-lab1
## Getting started
### Running Production
* The implementation of aprior_algorithm
'''
python aprior_algorithm.py
'''

* The implementation of fp_growth
'''
python fp_growth.py
'''

# 說明
input 在 input_data 裡面的.csv檔案
output 在 output_data中 output_data_fp_growth為FPgrowth的output 以此類推

# 注意事項
輸入時不有打包參數是因為兩個資料及要看到的min_support 跟 min_confidence不能設定一樣，
因為兩個資料及的頻率相差很遠，會造成data不好看，我以我直接打包在function裡面。

兩者結果看起來不一樣是因為參數不一樣

IBM: fp_growth: min_support = 0.1 min_confidence=0.32
     aprior_algorithm: min_support = 0.5 min_confidence=0.3 max_length=4

Kaggle: fp_growth: min_support = 0.5 min_confidence=0.3
        aprior_algorithm: min_support = 0.5 min_confidence=0.3 max_length=4