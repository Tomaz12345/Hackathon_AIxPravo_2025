import json
from .data import combine_files


def get_prompt_1(database_example):
    message = '''
    I want to register a trademark.
    The brand name is Nike.
    here is data from the database: \n{}
    Can I register it?'''.format(database_example)

    return message

def get_prompt_main(brand, goods_services):
    database_example = combine_files(brand, goods_services)
    return get_prompt_1(database_example)

def get_prompt_evaluation(result):
    message = '''
    Can you determine the status of the trademark registration?
    Response: {}
    Give me short answer in 1 word, must be one of the following options: "rejected", "caution", "approved"'''.format(result)
    
    return message


if __name__ == "__main__":
    brand = "Nike"
    goods_services = None
    print(get_prompt_main(brand, goods_services))