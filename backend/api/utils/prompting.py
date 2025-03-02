import json
from .data import combine_files


def get_prompt_1(brand_name, goods_services, database_example):
    message = "I want to register a trademark."
    if brand_name is not None and goods_services is not None:
        message += '''The brand name is {}, and the goods/services are {}.'''.format(brand_name, goods_services)
    elif brand_name is not None:
        message += '''The brand name is {}.'''.format(brand_name, database_example)
    else:
        message += '''The goods/services are {}.'''.format(goods_services)
    message += '''Here is data from the database: \n{}
    If there is no entries in the database(s), you can register it.
    No need for caution.
    Remember that.
    This is important.
    Can I register the brand?'''.format(database_example)

    return message

def get_prompt_main(brand, goods_services):
    database_example = combine_files(brand, goods_services)
    return get_prompt_1(brand, goods_services, database_example)

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