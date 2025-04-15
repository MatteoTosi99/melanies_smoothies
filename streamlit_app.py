import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

name_on_oder = st.text_input("Name on smoothie:")
if name_on_oder:
    st.write("The name on your order will be", name_on_oder)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
fruit_list = my_dataframe.to_pandas()["FRUIT_NAME"].tolist()

st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect("Choose up to 5 ingredients", fruit_list)

if len(ingredients_list) > 5:
    st.warning("Please choose up to 5 ingredients only.")
else:
    if ingredients_list and name_on_oder:
        ingredients_string = ", ".join(ingredients_list)
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, name_on_order, order_filled) 
            VALUES ('{ingredients_string}', '{name_on_oder}', FALSE)
        """
        if st.button("Submit order"):
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
