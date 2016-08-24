result_map = {
    'PD': 'Pending',
    'RPD': 'Pending Rejudge',
    'IQ': 'In Queue',
    'DC': 'Decorating',
    'CP': 'Finished Compiling',
    'RN': 'Finished Running',
    'JG': 'Judging',
    'RJ': 'Running & Judging',
    'AE': 'Analysing Errors',
    
    'SE': 'Submission Error',
    'UE': 'Unknown Error',
    'IW': 'Invalid Word',
    'RF': 'Restrained Function',
    'DF': 'Decoration Failed',
    'CLLE': 'Code Length Limit Exceeded',
    'CE': 'Compile Error',
    'RE': 'Runtime Error',
    'TLE': 'Time Limit Exceeded',
    'MLE': 'Memory Limit Exceeded',
    'OLE': 'Output Limit Exceeded',
    'WA': 'Wrong Answer',
    'PE': 'Presentation Error',
    'PTE': 'Punctuation Error',
    'AC': 'Accepted'
}

result_priority = {
    'Accepted': 0,
    'DEFAULT': 5,
    'Presentation Error': 7,
    'Wrong Answer': 10,
    'Time Limit Exceed': 20,
    'Memory Limit Exceed': 30,
    'Output Limit Exceed': 40,
    'Runtime Error': 50,
}
