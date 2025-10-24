import random as rand
import torch

base_quantity_for_all_products = 50
max_expiry_time = 69
min_expiry_time = 2

order_amount = 5

sweet_spot_min = 20
sweet_spot_max = 30

products_by_id = {
    1: {
        "quantity": base_quantity_for_all_products,
        "past_7_days_sales": [0, 0, 0, 0, 0, 0, 0],
        
    },
    2: {
        "id": 2,
        "quantity": base_quantity_for_all_products,
        "past_7_days_sales": [0, 0, 0, 0, 0, 0, 0],
        
    },
    3: {
        "id": 3,
        "quantity": base_quantity_for_all_products,
        "past_7_days_sales": [0, 0, 0, 0, 0, 0, 0],
        
    },
    4: {
        "id": 4,
        "quantity": base_quantity_for_all_products,
        "past_7_days_sales": [0, 0, 0, 0, 0, 0, 0],
        
    },
    5: {
        "id": 5,
        "quantity": base_quantity_for_all_products,
        "past_7_days_sales": [0, 0, 0, 0, 0, 0, 0],
        
    }
}

ids = products_by_id.keys()



def get_random_sales():
    sales = []
    base_quantity = rand.randint(1, base_quantity_for_all_products)
    for _ in range(7):
        sales.append(base_quantity + rand.randint(int(- base_quantity), base_quantity))

    return sales

def get_random_product_size(under: int):
    return rand.randint(0, int(under))

def get_random_expiry_time():
    return rand.randint(min_expiry_time, max_expiry_time)

def make_usable_input_for_batch(sales: list):
    return torch.tensor([sales], dtype=torch.float32)

def make_usable_input_norml(sales: list):
    return torch.tensor(sales, dtype=torch.float32)