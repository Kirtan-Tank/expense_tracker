import streamlit as st
import pandas as pd
from datetime import datetime

# Create a function to load or create the expense data
def load_expenses():
    try:
        expenses = pd.read_csv("expenses.csv")
    except FileNotFoundError:
        expenses = pd.DataFrame(columns=["Date", "Amount", "Tags"])
    return expenses

# Create a function to save the expense data
def save_expenses(expenses):
    expenses.to_csv("expenses.csv", index=False)

# Create the main function to run the Streamlit app
def main():
    st.title("Expense Tracker App")

    # Load or create expense data
    expenses = load_expenses()

    # Add expense form
    st.subheader("Add New Expense")
    date = st.date_input("Date", datetime.today())
    amount = st.number_input("Amount")
    tags = st.text_input("Tags (comma-separated)")

    if st.button("Add Expense"):
        tags_list = [tag.strip() for tag in tags.split(",")]
        new_expense = {"Date": date, "Amount": amount, "Tags": tags_list}
        expenses = expenses.append(new_expense, ignore_index=True)
        save_expenses(expenses)
        st.success("Expense added successfully!")

    # Review expenses
    st.subheader("Review Expenses")

    # Display expenses based on selected timeframe
    timeframe = st.selectbox("Select Timeframe", ["Daily", "Weekly", "Monthly", "Yearly"])

    if timeframe == "Daily":
        today = datetime.today().date()
        daily_expenses = expenses[expenses["Date"] == today]
        st.write(daily_expenses)

    elif timeframe == "Weekly":
        this_week = datetime.today().isocalendar()[1]
        weekly_expenses = expenses[(expenses["Date"] >= today - pd.Timedelta(days=today.weekday())) & (expenses["Date"].dt.isocalendar().week == this_week)]
        st.write(weekly_expenses)

    elif timeframe == "Monthly":
        this_month = datetime.today().month
        monthly_expenses = expenses[expenses["Date"].dt.month == this_month]
        st.write(monthly_expenses)

    elif timeframe == "Yearly":
        this_year = datetime.today().year
        yearly_expenses = expenses[expenses["Date"].dt.year == this_year]
        st.write(yearly_expenses)

if __name__ == "__main__":
    main()
