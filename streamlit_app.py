import streamlit
streamlit.title('My Mom'"'"'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeel')
streamlit.text(' 🥗 kale , Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑 🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
streamlit.text(fruityvice_response.json())

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

#New section to display fruityvice api data
streamlit.header("Fruityvice Fruit Advice!")
try:    fruit_choice = streamlit.text_input('What fruit would you like information about?')    if not fruit_choice:        streamlit.error("Please select a fruit to get information.")    else:        back_from_function = get_fruityvice_data(fruit_choice)        streamlit.dataframe(back_from_function)

except URLError as e:    streamlit.error()

streamlit.header("View Our Fruit List - Add Your Favorites!")
#Sowflake-related fuction
def get_fruit_load_list():    with my_cnx.cursor() as my_cur:        my_cur.execute("select * from fruit_load_list")        return my_cur.fetchall()
 like 1


#Add a button to load the fruit
if streamlit.button('Get Fruit List'):    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])    my_data_rows = get_fruit_load_list()    my_cnx.close()    streamlit.dataframe(my_data_rows)

#dont run anything past here while we troublshoot
#streamlit.stop()

#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):    with my_cnx.cursor() as my_cur:        my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])    back_from_function = insert_row_snowflake(add_my_fruit)    my_cnx.close()    streamlit.text(back_from_function)





