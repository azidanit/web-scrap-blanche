import json

def get_slug_from_href(href):
    return href.split("/")[-1]

def json_to_sql(json_file):

    with open(json_file) as f:
        data = json.load(f)

        with open("categories_with_id.sql", "w") as fsql:
            for level_1_cat in data:
                level_1_name = level_1_cat["level_1_name"]
                level_1_href = get_slug_from_href(level_1_cat["level_1_href"])
                level_1_cat_id = level_1_cat["cat_id"]
                fsql.write("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', NULL, NULL);\n".format(
                    level_1_cat_id, level_1_name, level_1_href, ""
                ))
                print("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', NULL, NULL);".format(
                    level_1_cat_id, level_1_name, level_1_href, ""))

                for level_2_cat in level_1_cat["level_2"]:
                    level_2_name = level_2_cat["level_2_name"]
                    level_2_href = get_slug_from_href(level_2_cat["level_2_href"])
                    if level_2_href == "lain-lain" or level_2_href == "lainnya":
                        level_2_href += "-" + level_1_href
                    level_2_cat_id = level_2_cat["cat_id"]
                    fsql.write("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', {}, NULL);\n".format(
                        level_2_cat_id, level_2_name, level_2_href, "", level_2_cat["cat_id_parent"] ))
                    print("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', {}, NULL);".format(
                        level_2_cat_id, level_2_name, level_2_href, "", level_2_cat["cat_id_parent"] ))
                    
                    for level_3_cat in level_2_cat["level_3"]:
                        level_3_name = level_3_cat["level_3_name"]
                        level_3_href = level_2_href + "-" + get_slug_from_href(level_3_cat["level_3_href"])
                        level_3_cat_id = level_3_cat["cat_id"]
                        fsql.write("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', {}, {});\n".format(
                            level_3_cat_id, level_3_name, level_3_href, "", level_3_cat["cat_id_parent"], level_3_cat["cat_id_grandparent"]))
                        print("INSERT INTO categories (id, name, slug, image_url, parent_id, grandparent_id) VALUES ({}, '{}', '{}', '{}', {}, {});".format(
                            level_3_cat_id, level_3_name, level_3_href, "", level_3_cat["cat_id_parent"], level_3_cat["cat_id_grandparent"]))
                   

json_to_sql("categories_new_with_id.json")