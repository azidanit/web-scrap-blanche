import json
import random
import re
import os

# INSERT INTO public.products
# (merchant_id, category_id, slug, title, min_real_price, max_real_price, min_discount_price, max_discount_price, created_at, updated_at, deleted_at, is_archived, description, weight, width, height, length, is_used, sku)
# VALUES(0, 0, '', '', 0, 0, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '', false, '', '', '', '', '', false, '');

# INSERT INTO public.product_images
# (product_id, image_url)
# VALUES(0, '');

# INSERT INTO public.product_analytics
# (product_id, avg_rating, num_of_review, num_of_sale, num_of_favorite, total_stock, created_at, updated_at, deleted_at, score)
# VALUES(0, 0, 0, 0, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '', 0);

# INSERT INTO public.variant_items
# (product_id, price, image_url, stock, created_at, updated_at, deleted_at, discount_price)
# VALUES(0, 0, '', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '', 0);

# INSERT INTO public.variant_specs
# (variant_item_id, variation_group_id, variation_name, created_at, updated_at, deleted_at)
# VALUES(0, 0, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '');

# INSERT INTO public.variation_groups
# ("name", created_at, updated_at, deleted_at)
# VALUES('', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '');

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
    title = title.replace("'", "''")
    title = title.replace(' ', '-')
    title = title.replace('--', '-')
    title = title.replace(' ', '')
    title = title.lower()
    print(title)

    return title

def random_number_between(start, end):
    return random.randint(start, end)

def get_merchant_domain_and_id():
    start_id = 100
    list_domain = ["browsecat","meevee","edgepulse","talanenew","topicware","eamia","roomm","centidel","talane","mybuzz","zooveo","podcat","meejo","thoughtblab","realblab","ooba","bluezoom","brainlounge","oyondu","buzzbean","mycat","agivu","oyonder","tavu","gabcube","voonyx","jatri","trunyx","aimbu","meetz"]
    random_number = random_number_between(0, len(list_domain)-1)
    return list_domain[random_number], start_id + random_number

def json_to_sql(json_file, product_id, variant_item_id, variation_group_id, variant_spec_id, product_analytic_id):
    with open(json_file) as f:
        data = json.load(f)
        sql_products = "INSERT INTO public.products (id, product_analytic_id, merchant_id, merchant_domain, category_id, slug, title, min_real_price, max_real_price, min_discount_price, max_discount_price, description, weight) VALUES"
        sql_images = "INSERT INTO public.product_images (product_id, image_url) VALUES"
        sql_analytics = "INSERT INTO public.product_analytics (id, avg_rating, num_of_review, num_of_sale, num_of_favorite, total_stock, score) VALUES"
        sql_variant_items = "INSERT INTO public.variant_items (id, product_id, price, image_url, stock) VALUES"
        sql_variant_specs = "INSERT INTO public.variant_specs (id, variant_item_id, variation_group_id, variation_name) VALUES"
        sql_variant_groups = "INSERT INTO public.variation_groups (id, name) VALUES"
        
        # product_id = 9999
        # variant_item_id = 9999
        # variation_group_id = 10000
        # variant_spec_id = 10000
        # product_analytic_id = 9999

        for i in data["products"]:
            # print(i)
            # print(i["price"])
            price = int(get_price(i["price"]))
            min_price = price
            max_price = price
            total_stock = 0
            product_cat_id = data["cat_id"]
            prod_merchant_domain, prod_merchant_id = get_merchant_domain_and_id()

            product_id += 1

            # variant groups
            variant_groups_ids = []
            if i["variants"] != None:
                sql_variant_groups += "({id}, '{name}'),".format(
                    id= variation_group_id,
                    name= get_group_name(i["variants"]["group_name1"])
                )
                variant_groups_ids.append(variation_group_id)
                variation_group_id += 1
                
                if i["variants"]["group_name2"] != None:
                    sql_variant_groups += "({id}, '{name}'),".format(
                        id= variation_group_id,
                        name= get_group_name(i["variants"]["group_name2"])
                    )
                    variant_groups_ids.append(variation_group_id)
                    variation_group_id += 1

                # variant items
                variant_items_ids = []
                for variant_item in i["variants"]["options"]:
                    variant_item_id += 1
                    sql_variant_items += "({id}, {product_id}, {price}, '{image_url}', {stock}),".format(
                        id= variant_item_id,
                        product_id= product_id,
                        price= get_price(variant_item["price"]),
                        image_url= "",
                        stock= 10,
                        # discount_price= get_price(variant_item["price"])
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
                            sql_variant_specs += "({id}, {variant_item_id}, {variation_group_id}, '{variation_name}'),".format(
                                id= variant_spec_id,
                                variant_item_id= variant_item_id,
                                variation_group_id= variant_group_id,
                                variation_name= item_option_data["option_name1"]
                            )
                        else:
                            sql_variant_specs += "({id}, {variant_item_id}, {variation_group_id}, '{variation_name}'),".format(
                                id= variant_spec_id,
                                variant_item_id= variant_item_id,
                                variation_group_id= variant_group_id,
                                variation_name= item_option_data["option_name2"]
                            )
                        variant_spec_id += 1
            else:
                #inset dummy variant item
                variant_item_id += 1
                sql_variant_items += "({id}, {product_id}, {price}, '{image_url}', {stock}),".format(
                    id= variant_item_id,
                    product_id= product_id,
                    price= price,
                    image_url= "",
                    stock= 10,
                    # discount_price= price
                )
                total_stock += 10

            # analytics
            product_analytic_id += 1
            sql_analytics += "({id}, {avg_rating}, {num_of_review}, {num_of_sale}, {num_of_favorite}, {total_stock}, {score}),".format(
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
            sql_products += "({id}, {product_analytic_id}, {merchant_id}, '{merchant_domain}', {cat_id}, '{slug}', '{title}', {min_real_price}, {max_real_price}, {min_discount_price}, {max_discount_price}, '{description}', {weight}),".format(
                id= product_id,
                product_analytic_id= product_analytic_id,
                merchant_id=prod_merchant_id, 
                merchant_domain=prod_merchant_domain,
                cat_id=product_cat_id, 
                slug= prod_merchant_domain + "/" + slug_generator(str(i["name"])), 
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
                sql_images += "({product_id}, '{image_url}'),".format(
                    product_id= product_id,
                    image_url= image
                )            
        
        sql_products = sql_products[:-1] + ";"
        sql_images = sql_images[:-1] + ";"
        sql_analytics = sql_analytics[:-1] + ";"
        sql_variant_items = sql_variant_items[:-1] + ";"
        sql_variant_specs = sql_variant_specs[:-1] + ";"
        sql_variant_groups = sql_variant_groups[:-1] + ";"
        return sql_products, sql_images, sql_analytics, sql_variant_items, sql_variant_specs, sql_variant_groups, product_id, variant_item_id, variant_spec_id, variation_group_id, product_analytic_id


folder_chunk = "product_cat_chunk"

json_files = []
for path in os.listdir(folder_chunk):
    # check if current path is a file
    if os.path.isfile(os.path.join(folder_chunk, path)):
        json_files.append(os.path.join(folder_chunk, path))
print(json_files)


product_id = 9999
variant_item_id = 9999
variation_group_id = 10000
variant_spec_id = 10000
product_analytic_id = 9999

for json_file in json_files:
    sql_prod, sql_img, sql_analytic, sql_variant_item, sql_variant_spec, sql_variant_group, product_id, variant_item_id, variant_spec_id, variation_group_id, product_analytic_id = json_to_sql(json_file, product_id, variant_item_id, variation_group_id, variant_spec_id, product_analytic_id)
    # product_id += 1
    # variant_item_id += 1
    # variation_group_id += 1
    # variant_spec_id += 1
    # product_analytic_id += 1

    # write to file
    with open('product_sql_2202/' + 'product_cat.sql', 'a') as f:
        f.write(sql_prod)

    with open('product_sql_2202/' + 'product_images_cat.sql', 'a') as f:
        f.write(sql_img)

    with open('product_sql_2202/' + 'product_analytics_cat.sql', 'a') as f:
        f.write(sql_analytic)

    with open('product_sql_2202/' + 'variant_items_cat.sql', 'a') as f:
        f.write(sql_variant_item)

    with open('product_sql_2202/' + 'variant_specs_cat.sql', 'a') as f:
        f.write(sql_variant_spec)

    with open('product_sql_2202/' + 'variant_groups_cat.sql', 'a') as f:
        f.write(sql_variant_group)
        