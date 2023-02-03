import json

def get_slug_from_href(href):
    return href.split("/")[-1]

def json_to_sql(json_file):
    cat_id_global = 99

    with open(json_file) as f:
        data = json.load(f)

        with open("categories.sql", "w") as fsql:
            for level_1_cat in data:
                cat_id_global += 1
                level_1_name = level_1_cat["level_1_name"]
                level_1_href = get_slug_from_href(level_1_cat["level_1_href"])
                level_1_cat_id = cat_id_global
                fsql.write("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', NULL, NULL);\n".format(
                    level_1_cat_id, level_1_name, level_1_href, ""
                ))
                print("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', NULL, NULL);".format(
                    level_1_cat_id, level_1_name, level_1_href, ""))

                for level_2_cat in level_1_cat["level_2"]:
                    cat_id_global += 1
                    level_2_name = level_2_cat["level_2_name"]
                    level_2_href = get_slug_from_href(level_2_cat["level_2_href"])
                    level_2_cat_id = cat_id_global
                    fsql.write("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', {}, NULL);\n".format(
                        level_2_cat_id, level_2_name, level_2_href, "", level_1_cat_id ))
                    print("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', {}, NULL);".format(
                        level_2_cat_id, level_2_name, level_2_href, "", level_1_cat_id))
                    for level_3_cat in level_2_cat["level_3"]:
                        cat_id_global += 1
                        level_3_name = level_3_cat["level_3_name"]
                        level_3_href = get_slug_from_href(level_3_cat["level_3_href"])
                        level_3_cat_id = cat_id_global
                        fsql.write("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', {}, {});\n".format(
                            level_3_cat_id, level_3_name, level_3_href, "", level_2_cat_id, level_1_cat_id))
                        print("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', {}, {});".format(
                            level_3_cat_id, level_3_name, level_3_href, "", level_2_cat_id, level_1_cat_id))
                   

json_to_sql("categories_new.json")