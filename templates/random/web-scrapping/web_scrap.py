import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

# Executable path for Mac users
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
driver = webdriver.Chrome(executable_path=r"C:\Chrome\chromedriver.exe")

# Function to grab ingredients, instructions and image from half-baked harvest inner-page
def grab_details_hbh(url):

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    recipe_ingredients_detail = soup.find_all('li', attrs={'class': 'wprm-recipe-ingredient'})
    ingredients_list = []

    for ingredients in recipe_ingredients_detail:
        ingredients_list.append(ingredients.text)

    recipe_instructions_detail = soup.find_all('li', attrs={'class': 'wprm-recipe-instruction'})
    instructions_list = []

    for instruction in recipe_instructions_detail:
        instructions_list.append(instruction.text)

    # Extract Image
    post_content = soup.find("div", attrs={"class": "post-content"}).find_all_next("img")
    image_list = []
    for img in post_content:
        try:
            if img['alt']:
                string = str(img['alt'])
                if "horizontal photo" in string:
                    image = img['data-src']
                    image_list.append(image)

        except Exception as e:
            pass

    return ingredients_list, instructions_list, image_list

# Function to grab link and recipe name from half baked harvest main page
def halfbakedharvest():

    my_dict = {}

    url = 'https://www.halfbakedharvest.com/category/recipes/'
    browser.visit(url)

    for x in range(1, 10):

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        recipes = soup.find_all('a', class_='recipe-block')

        for recipe in recipes:

            recipe_link = recipe['href']
            my_dict[recipe.img['title']] = [recipe_link]

        # Iterate through to the next page
        browser.visit(f"{url}page/{x}/")

    for recipe_name in my_dict:

        link = my_dict[recipe_name]
        details = grab_details_hbh(link[0])
        ingredients, instructions, image = details

        my_dict[recipe_name].append(ingredients)
        my_dict[recipe_name].append(instructions)
        if image:
            my_dict[recipe_name].append(image[0])
        else:
            print("Image not found!")

        print(my_dict)

    return my_dict

# Save the dictionary to a local variable
hbh_dict = halfbakedharvest()

# Save the dictionary as a dataframe
df = pd.DataFrame(hbh_dict.values(), index=hbh_dict.keys(), columns=['Link', 'Ingredients', 'Instructions', "Image"])

print(df)
