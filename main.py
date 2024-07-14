import try_openAI_vision_02
import excel_data_processing

# Test the funktion     
#user_input = "Project/img/jpg/IMG_9985.jpg" # Case 03 MEMO: Wenn die Endung .jpeg ist, bekommt man error: "UnboundLocalError: cannot access local variable 'base64_image' where it is not associated with a value"  
#user_input = "Project/img/jpg/IMG_9984.jpg" # Case 03 MEMO: Wenn die Endung .jpeg ist, bekommt man error
user_input = "Today I've been busy learning Python again. It's fun to work in a team." # Expected "Case 01", result "Case 01"
user_input = "Project/img/jpg/IMG_9991.HEIC" # excpected "Case 02", result "Case 03"
#user_input = "Project/img/jpg/IMG_9991.jpeg" # expected Case 02, result Case 03. MEMO: Wenn die Endung .jpg ist, bekommt man error: "UnboundLocalError: cannot access local variable 'base64_image' where it is not associated with a value"  


# Test the excel function
#df = excel_data_processing.add_expense(df, "Rewe", "Lebensmittel", 66.77)
#excel_data_processing.write_to_excel(df, file_path, receipt_issue_month=2, receipt_issue_year=2024)



answer_category = try_openAI_vision_02.determine_and_ask_openAI(user_input) 
print("answer_category:", answer_category)
if answer_category:
    if "Case 01" in answer_category:
        print("Processing Case 01...")
        positiv_feedback = try_openAI_vision_02.second_API_request_case_01(user_input)
        print(positiv_feedback)
    elif "Case 02" in answer_category:
        print("Processing Case 02...")
        get_expense_info = try_openAI_vision_02.second_API_request_case_02(user_input)
        print(get_expense_info) 
        #expense_input = excel_data_processing.add_expense(get_expense_info) # TODO Anpassung im Funktionskopf notwendig
    else:
        print("the user input was neither a journal nor money expense")
else:
    print("Failed to determine the category from the response.")


#try_openAI_vision_02.determine_and_ask_openAI(user_input)