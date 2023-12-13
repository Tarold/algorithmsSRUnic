import tkinter as tk
from tkinter import ttk, simpledialog

DEFAULT_COMPANIES = [
    {
        "назва підприємства": "Підприємство А",
        "адреса": "вул. Головна, 1",
        "місяць": 1,
        "рік": 2023,
        "прибуток": 50000
    },
    {
        "назва підприємства": "Підприємство А",
        "адреса": "вул. Головна, 1",
        "місяць": 2,
        "рік": 2023,
        "прибуток": 40000
    },
    {
        "назва підприємства": "Підприємство А",
        "адреса": "вул. Головна, 1",
        "місяць": 3,
        "рік": 2023,
        "прибуток": 20000
    },
    {
        "назва підприємства": "Підприємство А",
        "адреса": "вул. Головна, 1",
        "місяць": 1,
        "рік": 2022,
        "прибуток": 50000
    },
    {
        "назва підприємства": "Підприємство Б",
        "адреса": "вул. Центральна, 10",
        "місяць": 1,
        "рік": 2023,
        "прибуток": 50000
    },
    {
        "назва підприємства": "Підприємство Б",
        "адреса": "вул. Центральна, 10",
        "місяць": 2,
        "рік": 2023,
        "прибуток": 60000
    },
    {
        "назва підприємства": "Підприємство В",
        "адреса": "вул. Паркова, 5",
        "місяць": 1,
        "рік": 2023,
        "прибуток": 51000
    },
    {
        "назва підприємства": "Підприємство Г",
        "адреса": "вул. Паркова, 5",
        "місяць": 1,
        "рік": 2023,
        "прибуток": 5000
    },
    {
        "назва підприємства": "Підприємство Д",
        "адреса": "вул. Паркова, 5",
        "місяць": 1,
        "рік": 2023,
        "прибуток": 40000
    },
    {
        "назва підприємства": "Підприємство Е",
        "адреса": "вул. Паркова, 5",
        "місяць": 1,
        "рік": 2023,
        "прибуток": 50000
    },
    {
        "назва підприємства": "Підприємство Ж",
        "адреса": "вул. Паркова, 5",
        "місяць": 1,
        "рік": 2023,
        "прибуток": 50000
    },
    {
        "назва підприємства": "Підприємство З",
        "адреса": "вул. Паркова, 5",
        "місяць": 1,
        "рік": 2023,
        "прибуток": 50000
    },
    {
        "назва підприємства": "Підприємство К",
        "адреса": "вул. Паркова, 5",
        "місяць": 1,
        "рік": 2023,
        "прибуток": 50000
    },
]

class VisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual App")

        self.companies = list(DEFAULT_COMPANIES)

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)

        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Companies")

        companies_label = ttk.Label(tab1, text="Companies:")
        companies_label.pack()

        display_companies_button = ttk.Button(tab1, text="Display All Companies", command=self.display_all_companies)
        display_companies_button.pack()

        display_top_25_percent_button = ttk.Button(tab1, text="Display Top 25%", command=self.display_top_25_percent)
        display_top_25_percent_button.pack()

        self.display_text_companies = tk.Text(tab1, height=10, width=50)
        self.display_text_companies.pack()

        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="New Companies")

        add_company_button = ttk.Button(tab2, text="Add New Company", command=self.add_new_company)
        add_company_button.pack()

        clear_all_button = ttk.Button(tab2, text="Clear All Companies", command=self.clear_all_companies)
        clear_all_button.pack()

        default_companies_button = ttk.Button(tab2, text="Add Default Companies", command=self.add_default_companies)
        default_companies_button.pack()

        notebook.pack()

    def display_all_companies(self):
        display_text = "All Companies:\n"
        for company in self.companies:
            display_text += f"{company['назва підприємства']}, {company['рік']}, {company['прибуток']}\n"
        self.display_text_companies.delete(1.0, tk.END)
        self.display_text_companies.insert(tk.END, display_text)

    def display_top_25_percent(self):
        profits, max_profits = self.get_by_profits(self.companies)

        profits_list = []

        for company_key, total_profit in profits.items():
            max_profit_key = (company_key[0], company_key[1])
            max_profit = max_profits[max_profit_key]
            company_info = {
                "Company": company_key[0],
                "Year": company_key[1],
                "Total Profit": total_profit,
                "Maximum Profit": max_profit
            }
            profits_list.append(company_info)

        self.sort(profits_list)
        top_25 = self.find_top_25_percent(profits_list)

        display_text = "Top 25% Companies:\n"
        for company_info in top_25:
            display_text += f"Company: {company_info['Company']}, Year: {company_info['Year']}, Total Profit: {company_info['Total Profit']}, Maximum Profit: {company_info['Maximum Profit']}\n"

        self.display_text_companies.delete(1.0, tk.END)
        self.display_text_companies.insert(tk.END, display_text)

    def add_new_company(self):
        company_name = simpledialog.askstring("Company Input", "Enter company name:")
        if company_name:
            year = simpledialog.askinteger("Company Input", "Enter year:")
            if year:
                profit = simpledialog.askinteger("Company Input", "Enter profit:")
                if profit is not None:
                    new_company = {
                        "назва підприємства": company_name,
                        "рік": year,
                        "прибуток": profit
                    }
                    self.companies.append(new_company)
                    self.display_all_companies()

    def clear_all_companies(self):
        self.companies = []
        self.display_all_companies()

    def add_default_companies(self):
        default_companies = list(DEFAULT_COMPANIES)
        self.companies.extend(default_companies)
        self.display_all_companies()

    def get_by_profits(self, companies):
        max_profits = {}
        profits = {}
        for company in companies:
            company_key = (company["назва підприємства"], company["рік"])
            if company_key not in max_profits:
                max_profits[company_key] = company["прибуток"]
                profits[company_key] = company["прибуток"]
            else:
                profits[company_key] += company["прибуток"]
                if company["прибуток"] > max_profits[company_key]:
                    max_profits[company_key] = company["прибуток"]

        return profits, max_profits

    def find_top_25_percent(self, companies):
        sorted_companies = sorted(companies, key=lambda x: (x['Total Profit'], x['Maximum Profit']), reverse=True)
        n = len(sorted_companies)
        return sorted_companies[:int(n * 0.25)]

    def sort(self, companies):
        companies.sort(key=lambda x: (x['Total Profit'], x['Maximum Profit']), reverse=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualApp(root)
    root.mainloop()
