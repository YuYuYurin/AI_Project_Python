
case_01 = "The analysis result is a diary or journal."
case_02 = "The analysis result is related to money expenses."
case_03 = "The analysis result does not fall into Case 1 or Case 2."

prompt_system = f"""
Our role as the system is to analyze the input content. An input content can be categorized into the following cases:

1. **Case 01**: {case_01} - In this case, return "Case 01 and the input text".
2. **Case 02**: {case_02} - In this case, return "Case 02" and the input image or input text.
3. **Case 03**: {case_03} - In this case, categorize the result as 'others' and return "Case 03".

"""


