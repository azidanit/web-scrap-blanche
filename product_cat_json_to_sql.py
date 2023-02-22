import json
import random
import re
import os

product_id = 999
variant_item_id = 999
variation_group_id = 1000
variant_spec_id = 1000
product_analytic_id = 999

def replace_quote_postgres(str):
    return str.replace("'", "''")

def get_price(pricestr):
    return re.sub("[^0-9]", "", pricestr)

def get_group_name(name):
    return name.split(' ')[1][:-1]


def slug_generator(title):
    # add random string
    # title = title + ' ' + random_string(5)   
    # remove special character
    # title = re.sub(r'[^\w\s]', '', title)
    # remove space
    # title = title.replace(' ', '-')
    # lowercase
    title = title + str(random.randint(0,9999))
    title = re.sub(r'[^\w\s]', '', title)
    title = title.replace(' ', '-')
    title = title.lower()

    return title

def json_to_sql(json_data, cat_id_product):
    # with open(json_file) as f:
        data = json_data
        sql_products = "INSERT INTO public.products (id, product_analytic_id, merchant_id, category_id, slug, title, min_real_price, max_real_price, min_discount_price, max_discount_price, description, weight) VALUES\n"
        sql_images = "INSERT INTO public.product_images (product_id, image_url) VALUES\n"
        sql_analytics = "INSERT INTO public.product_analytics (id, avg_rating, num_of_review, num_of_sale, num_of_favorite, total_stock, score) VALUES\n"
        sql_variant_items = "INSERT INTO public.variant_items (id, product_id, price, image_url, stock, discount_price) VALUES\n"
        sql_variant_specs = "INSERT INTO public.variant_specs (id, variant_item_id, variation_group_id, variation_name) VALUES\n"
        sql_variant_groups = "INSERT INTO public.variation_groups (id, name) VALUES\n"
        
        sql_products_final = ""
        sql_images_final = ""
        sql_analytics_final = ""
        sql_variant_items_final = ""
        sql_variant_specs_final = ""
        sql_variant_groups_final = ""

        global product_id
        global variant_item_id
        global variation_group_id
        global variant_spec_id
        global product_analytic_id


        for i in data:
            price = int(get_price(i["price"]))
            min_price = price
            max_price = price
            total_stock = 0

            product_id += 1

            # variant groups
            variant_groups_ids = []
            if i["variants"] != None:
                sql_variant_groups_final += sql_variant_groups + "({id}, '{name}');\n".format(
                    id= variation_group_id,
                    name= get_group_name(i["variants"]["group_name1"])
                )
                variant_groups_ids.append(variation_group_id)
                variation_group_id += 1
                
                if i["variants"]["group_name2"] != None:
                    sql_variant_groups_final += sql_variant_groups + "({id}, '{name}');\n".format(
                        id= variation_group_id,
                        name= get_group_name(i["variants"]["group_name2"])
                    )
                    variant_groups_ids.append(variation_group_id)
                    variation_group_id += 1

                # variant items
                variant_items_ids = []
                for variant_item in i["variants"]["options"]:
                    variant_item_id += 1
                    sql_variant_items_final += sql_variant_items + "({id}, {product_id}, {price}, '{image_url}', {stock}, {discount_price});\n".format(
                        id= variant_item_id,
                        product_id= product_id,
                        price= get_price(variant_item["price"]),
                        image_url= "",
                        stock= 10,
                        discount_price= get_price(variant_item["price"])
                    )
                    min_price = min(min_price, int(get_price(variant_item["price"])))
                    max_price = max(max_price, int(get_price(variant_item["price"])))
                    total_stock += 10
                    variant_items_ids.append(variant_item_id)
                
                # variant specs
                for variant_item_id in variant_items_ids:
                    for variant_group_id in variant_groups_ids:
                        item_option_data = i["variants"]["options"][variant_items_ids.index(variant_item_id)]
                        if variant_group_id == variant_groups_ids[0]:
                            sql_variant_specs_final += sql_variant_specs + "({id}, {variant_item_id}, {variation_group_id}, '{variation_name}');\n".format(
                                id= variant_spec_id,
                                variant_item_id= variant_item_id,
                                variation_group_id= variant_group_id,
                                variation_name= item_option_data["option_name1"]
                            )
                        else:
                            sql_variant_specs_final += sql_variant_specs + "({id}, {variant_item_id}, {variation_group_id}, '{variation_name}');\n".format(
                                id= variant_spec_id,
                                variant_item_id= variant_item_id,
                                variation_group_id= variant_group_id,
                                variation_name= item_option_data["option_name2"]
                            )
                        variant_spec_id += 1
            else:
                #inset dummy variant item
                variant_item_id += 1
                sql_variant_items_final += sql_variant_items + "({id}, {product_id}, {price}, '{image_url}', {stock}, {discount_price});\n".format(
                    id= variant_item_id,
                    product_id= product_id,
                    price= price,
                    image_url= "",
                    stock= 10,
                    discount_price= price
                )
                total_stock += 10

            # analytics
            product_analytic_id += 1
            sql_analytics_final += sql_analytics + "({id}, {avg_rating}, {num_of_review}, {num_of_sale}, {num_of_favorite}, {total_stock}, {score});\n".format(
                id= product_analytic_id,
                avg_rating= 0,
                num_of_review= 0,
                num_of_sale= 0,
                num_of_favorite= 0,
                total_stock= total_stock,
                score= 0
            )

            # temp_sql_prod = len(sql_products)
            # sql += "(" + 1 + ", '" + i["name"] + "', " + slug_generator(str(i["name"])) +  "', " + "), "
            sql_products_final += sql_products + "({id}, {product_analytic_id}, {merchant_id}, {cat_id}, '{slug}', '{title}', {min_real_price}, {max_real_price}, {min_discount_price}, {max_discount_price}, '{description}', {weight});\n".format(
                id= product_id,
                product_analytic_id= product_analytic_id,
                merchant_id=1, 
                cat_id=cat_id_product, 
                slug= "penakjaya/" + slug_generator(str(i["name"])), 
                title= replace_quote_postgres(i["name"]), 
                min_real_price= min_price,
                max_real_price= max_price,
                min_discount_price= min_price,
                max_discount_price= max_price,
                description= replace_quote_postgres(i["desc"]),
                weight= 1500
                )

            # images
            for image in i["imgs"]:
                sql_images_final += sql_images + "({product_id}, '{image_url}');\n".format(
                    product_id= product_id,
                    image_url= image
                )            
        
        # sql_products = sql_products[:-2] + ";\n"
        # sql_images = sql_images[:-2] + ";\n"
        # sql_analytics = sql_analytics[:-2] + ";\n"
        # sql_variant_items = sql_variant_items[:-2] + ";\n"
        # sql_variant_specs = sql_variant_specs[:-2] + ";\n"
        # sql_variant_groups = sql_variant_groups[:-2] + ";\n"
        return sql_products_final, sql_images_final, sql_analytics_final, sql_variant_items_final, sql_variant_specs_final, sql_variant_groups_final


# print(json_to_sql('product_laptop.json'))

sql_prod, sql_img, sql_analytic, sql_variant_item, sql_variant_spec, sql_variant_group = "", "", "", "", "", ""
for file in sorted(os.listdir('product_cat')):
    if file.endswith(".json"):
        print(file)

    fjson = os.path.join('product_cat', file)
    with open(fjson) as f:
        json_data = json.load(f)
        print(json_data["cat_id"])
        print(len(json_data["products"]))
        sql_prod_tmp, sql_img_tmp, sql_analytic_tmp, sql_variant_item_tmp, sql_variant_spec_tmp, sql_variant_group_tmp = json_to_sql(json_data["products"], json_data["cat_id"])
        
        sql_prod += sql_prod_tmp
        sql_img += sql_img_tmp
        sql_analytic += sql_analytic_tmp
        sql_variant_item += sql_variant_item_tmp
        sql_variant_spec += sql_variant_spec_tmp
        sql_variant_group += sql_variant_group_tmp


# write to file
# with open('product_sql/' + 'product_cat_11.sql', 'w') as f:
#     f.write(sql_analytic)
#     f.write(sql_prod)
#     f.write(sql_img)
#     f.write(sql_variant_group)
#     f.write(sql_variant_item)
#     f.write(sql_variant_spec)

with open('product_sql2/' + 'product_cat_11.sql', 'w') as f:
    f.write(sql_prod)

with open('product_sql2/' + 'product_images_cat_11.sql', 'w') as f:
    f.write(sql_img)

with open('product_sql2/' + 'product_analytics_cat_11.sql', 'w') as f:
    f.write(sql_analytic)

with open('product_sql2/' + 'variant_items_cat_11.sql', 'w') as f:
    f.write(sql_variant_item)

with open('product_sql2/' + 'variant_specs_cat_11.sql', 'w') as f:
    f.write(sql_variant_spec)

with open('product_sql2/' + 'variant_groups_cat_11.sql', 'w') as f:
    f.write(sql_variant_group)
    
