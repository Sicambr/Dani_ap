import loop_generator

#delete this def later
def File_from_CATIA(name_of_file):
    CATIA_f = []
    for line in open(name_of_file):CATIA_f.append(line)
    return CATIA_f


def Make_my_loop(original_text):
    all_text = []
    i = 0
    while i < len(original_text):
        if 'G201' in original_text[i] and 'G201' == original_text[i][:4]:
            all_text.append(original_text[i])
            i += 1
            break
        else:
            all_text.append(original_text[i])
            i += 1
    all_text.append('M8M138\n')
    number_b = all_text[0]

    # Extracting unnecessary commands (M8M138 - cooling)
    original_text = (remove_colling(original_text[i:]))

    try_rep = 1
    i = 0
    while try_rep == 1:
        # Create repetition block
        #print('\n',all_text)
        changed_text = loop_generator.Loops_body(original_text)
        number_b = changed_text.make_numbers(number_b)
        changed_text.double_Separation()
        #print('CAST_GXYR: ', changed_text.cast_GXYRF)
        #print('CAST_Z: ', changed_text.cast_Z)
        #print('HEAD_OF_TEXT: ', changed_text.head_ofText)
        changed_text.repetition_searsh()
        #print('HEAD_OF_TEXT: ', changed_text.head_ofText)
        #print('REPETITION BLOCK: ', changed_text.rep_block)
        if len(changed_text.rep_block) == 0:
            try_rep = 0
        #add head of text to origin
        all_text.extend(changed_text.head_ofText)
        changed_text.cut_repetit()
        original_text = changed_text.end_ofText
        if try_rep == 1:
            all_text.extend(changed_text.replace_block())
        i += 1
        if i == 100:
            try_rep = 0
    return all_text


def remove_colling(original_text):
    new_text=[]
    for i in original_text:
        if 'M8M138' not in i:
            new_text.append(i)
    return new_text


def main_creator(my_file):
    My_f = []
    My_f = Make_my_loop(my_file)
    return My_f

"""
open_file = '444.NC'
My_f = []
My_f = File_from_CATIA(open_file)
all_text = main_creator(My_f)
print(all_text)
"""

