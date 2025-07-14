import streamlit as st

def app():
    st.title("🥗 PCOS Diet Plan Generator")
    st.markdown("Customize your diet plan based on your health goals and preferences.")

    # --- User Inputs ---
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("👩 Age", min_value=10, max_value=60, value=25)
        weight = st.number_input("⚖️ Weight (kg)", min_value=30, max_value=150, value=60)
    with col2:
        goal = st.selectbox("🎯 Health Goal", ["Weight Loss", "Maintenance", "Weight Gain"])
        preference = st.radio("🥦 Dietary Preference", ["Vegetarian", "Non-Vegetarian"])
    
    allergies = st.text_input("🚫 Any Allergies? (Optional)", placeholder="e.g. lactose, nuts")

    # --- Generate Diet Plan Button ---
    if st.button("📝 Generate Diet Plan"):
        st.subheader("🧾 Your Personalized Diet Plan")
        st.markdown(f"**Age:** {age} years | **Weight:** {weight} kg | **Goal:** {goal} | **Diet:** {preference}")
        if allergies:
            st.markdown(f"**Allergies:** {allergies}")

        # Sample Meal Plan (This logic can be improved later)
        st.markdown("---")
        if goal == "Weight Loss":
            calories = "1200-1500 kcal/day"
            carbs = "Low to Moderate"
        elif goal == "Maintenance":
            calories = "1600-1800 kcal/day"
            carbs = "Moderate"
        else:
            calories = "1900-2200 kcal/day"
            carbs = "Moderate to High"

        st.success(f"Recommended Calories: {calories}")
        st.info(f"Carbohydrate Intake: {carbs}")

        st.markdown("### 🍽️ Sample Daily Meal Plan")

        if preference == "Vegetarian":
            st.markdown("""
- **Breakfast:** Oats with almond milk, chia seeds, and berries  
- **Mid-Morning Snack:** Apple with peanut butter  
- **Lunch:** Quinoa salad with chickpeas and mixed veggies  
- **Evening Snack:** Roasted makhana or nuts  
- **Dinner:** Grilled paneer with steamed broccoli  
""")
        else:
            st.markdown("""
- **Breakfast:** Boiled eggs, whole grain toast, avocado  
- **Mid-Morning Snack:** Greek yogurt with fruit  
- **Lunch:** Grilled chicken with brown rice and veggies  
- **Evening Snack:** Boiled eggs or tuna salad  
- **Dinner:** Fish curry with steamed spinach  
""")

        st.markdown("---")
        st.success("💡 Tip: Stay hydrated and exercise regularly to manage PCOS better.")

