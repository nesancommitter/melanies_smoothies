# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the Fruits you want in your custome Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be :', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session() 
# Instead of hardcoded choices bring data from table

# option = st.selectbox ('What is your Fav Fruit?',('Banana', 'Strawberries', 'Peaches') )
# st.write('Your Fav Fruit is : ', option)

# Fetch only the Fruit_name column from table
# my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Add a Multiselect instead of table display
#st.dataframe(data=my_dataframe,use_container_width=True)

ingredients_list = st.multiselect (
    'Choose upto 5 ingredients:',
    my_dataframe,
    max_selections = 5
)
# Display the choices by customer only when atleast one fruit is selected
# Take all the choices as string in ingredients_string
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+ name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button("Submit Order")
    
    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

#st.write(my_dataframe.queries)
