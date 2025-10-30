#taylorsamarel/qwen2-5-32b-arc-local-score-32-solved-script
import zipfile, json, os, copy, json
from code_golf_utils import *
from tqdm import tqdm

def check(solution, task_num, valall=False):
    if task_num == 157: return True # this one just takes a while to run
    task_data = load_examples(task_num)
    #print(task_num, max(1, 2500 - len(solution.encode('utf-8'))))
    try:
        namespace = {}
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=SyntaxWarning)
            exec(solution, namespace)
        if 'p' not in namespace: return False
        all_examples = task_data['train'] + task_data['test'] + task_data['arc-gen']
        examples_to_check = all_examples if valall else all_examples[:3]
        for example in examples_to_check:
            input_grid = copy.deepcopy(example['input'])
            expected = example['output']
            try:
                actual = namespace['p'](input_grid)
                actual = [[int(x) if int(x) == x else x for x in row] for row in actual]
                if json.dumps(actual) != json.dumps(expected):
                    return False
            except:
                return False
        return True
    except Exception as e:
        print(e)
        return False
    
import pandas as pd
#https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQ7RUqwrtwRD2EJbgMRrccAHkwUQZgFe2fsROCR1WV5LA1naxL0pU2grjQpcWC2HU3chdGwIOUpeuoK/pubhtml#gid=1427788625
top=[58, 90, 58, 80, 206, 51, 62, 84, 109, 68, 121, 127, 140, 70, 93, 43, 99, 323, 105, 146, 57, 91, 195, 62, 131, 52, 103, 63, 108, 94, 45, 39, 73, 125, 83, 75, 105, 51, 60, 69, 49, 139, 56, 255, 45, 170, 55, 92, 81, 85, 115, 40, 21, 280, 83, 40, 48, 103, 156, 48, 63, 143, 74, 152, 91, 268, 33, 116, 151, 78, 119, 54, 46, 79, 86, 276, 126, 60, 123, 253, 91, 50, 40, 62, 50, 172, 36, 101, 236, 159, 63, 86, 99, 102, 73, 325, 108, 88, 115, 85, 281, 150, 29, 84, 148, 67, 162, 56, 81, 85, 60, 109, 25, 64, 54, 20, 148, 271, 106, 97, 89, 82, 75, 96, 126, 54, 65, 61, 47, 65, 125, 86, 298, 168, 32, 105, 141, 104, 94, 36, 94, 40, 135, 53, 191, 58, 83, 141, 75, 30, 108, 40, 133, 99, 18, 146, 248, 269, 109, 105, 82, 96, 131, 32, 136, 61, 71, 111, 129, 196, 51, 20, 218, 97, 75, 64, 51, 47, 21, 79, 67, 169, 93, 100, 143, 60, 92, 61, 111, 109, 241, 110, 81, 67, 105, 112, 54, 122, 84, 84, 208, 102, 64, 93, 166, 144, 81, 215, 289, 20, 48, 105, 92, 62, 42, 114, 95, 56, 257, 87, 87, 103, 51, 171, 132, 139, 52, 119, 73, 114, 43, 58, 297, 118, 61, 54, 67, 223, 99, 99, 21, 54, 79, 64, 106, 105, 95, 72, 26, 118, 89, 57, 129, 84, 242, 95, 74, 61, 85, 135, 47, 39, 122, 216, 104, 102, 46, 239, 63, 117, 86, 89, 116, 71, 136, 38, 194, 118, 107, 179, 145, 83, 82, 220, 288, 109, 56, 89, 63, 67, 61, 56, 59, 70, 54, 63, 43, 55, 54, 87, 31, 89, 62, 92, 57, 71, 50, 226, 38, 78, 32, 44, 63, 96, 63, 71, 59, 54, 194, 68, 55, 48, 102, 259, 160, 30, 67, 163, 54, 134, 83, 58, 89, 66, 107, 93, 46, 64, 37, 119, 132, 111, 65, 78, 90, 58, 50, 94, 214, 91, 67, 84, 92, 96, 98, 105, 86, 97, 64, 45, 193, 69, 213, 155, 111, 365, 129, 138, 113, 260, 109, 48, 39, 112, 53, 30, 55, 143, 141, 27, 79, 134, 121, 62, 25, 52, 218, 61, 57, 99, 63, 149, 63, 91, 53, 179, 121, 77, 64, 67]

score = 0
rows = []
for task_num in tqdm(range(1,401), desc="Processing tasks"):
    solution = open('Best-Updated-2/task' + str(task_num).zfill(3) + '.py','rb').read()
    if check(solution, task_num, valall=True):
        s = max([0.1,2500-len(solution)])
        # print(task_num, 2500-s, top[task_num-1], top[task_num-1]-(2500-s))
        rows.append([task_num, len(solution), top[task_num-1], len(solution)-top[task_num-1]])
        score += s
        #print(task_num, '*'* 40)
    else: 
        rows.append([task_num, 'WRONG', 'WRONG', 'WRONG'])
        print(task_num, ": WRONG!!")
print('Score:', score)

df = pd.DataFrame(rows, columns=['Task', 'Our Bytes', 'Lowest Reported Bytes', 'Difference'])
# Convert 'WRONG' to a large negative number for sorting purposes
df['Difference_Sort'] = df['Difference'].apply(lambda x: float('-inf') if x == 'WRONG' else x)
sorted_df = df.sort_values(by='Difference_Sort', ascending=False).drop('Difference_Sort', axis=1)
sorted_df.to_csv('prioritize.csv', index=False)