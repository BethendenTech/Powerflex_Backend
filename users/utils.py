import os
import json
import requests
from decimal import Decimal

# Load the components table from the external JSON file
def load_components_table():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'components.json')
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON: {e}")

# Load exchange rate using ExchangeRate API
def get_exchange_rate(api_key, base_currency, target_currency):
    """Fetch the current exchange rate from an external API."""
    try:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()

        if 'conversion_rates' in data and target_currency in data['conversion_rates']:
            return data['conversion_rates'][target_currency]
        else:
            print("Error: Unable to fetch exchange rate.")
            return 450  # Default exchange rate
    except requests.RequestException as e:
        print(f"Error: Network problem occurred: {e}")
        return 450  # Default exchange rate if a network error occurs

# Function to calculate the base consumption based on the monthly spend and band group
def calculate_base_consumption(monthly_spend, band_group):
    band_prices = {'A': 209.5, 'B': 67.96, 'C': 53.49}  # Price per kWh for each band
    hours_supply = {'A': 20, 'B': 16, 'C': 12}  # Hours of electricity supply per day

    # Validate band group
    if band_group not in band_prices:
        raise ValueError("Error: Please specify a valid band group (A, B, or C)")

    # Select price per kWh and hours of supply based on band group
    price_per_kwh = band_prices[band_group]
    hours_per_day = hours_supply[band_group]

    # Calculate base consumption considering the hours of electricity supply
    base_consumption_kwh_per_month = float(monthly_spend) / price_per_kwh

    base_daily_consumption_kwh = float(base_consumption_kwh_per_month) / 30

    # Adjust base consumption to the actual number of hours supply for the band group
    adjusted_daily_consumption_kwh = base_daily_consumption_kwh * (24 / hours_per_day)
    return adjusted_daily_consumption_kwh

# Function to calculate appliance-based consumption (optional)
def calculate_appliance_based_consumption(appliances):
    total_appliance_consumption_kwh = 0
    for appliance in appliances:
        power = appliance['power_w']
        hours_per_day = appliance['hours_per_day']
        quantity = appliance['quantity']
        total_appliance_consumption_kwh += (power * hours_per_day * quantity) / 1000
    return total_appliance_consumption_kwh

# Function to compare and adjust the base consumption based on appliance consumption
def compare_and_adjust_base_consumption(base_consumption, appliance_consumption):
    # Calculate the difference
    difference = abs(base_consumption - appliance_consumption)

    # Determine the adjustment factor based on the difference
    if difference / base_consumption <= 0.10:  # Small difference, within 10%
        adjustment_factor = 0.1  # 90% trust in base consumption
    elif difference / base_consumption > 0.25:  # Large difference, more than 25%
        adjustment_factor = 0.5  # 50% trust in each
    else:
        adjustment_factor = 0.3  # Medium difference, balance the trust

    # Blend base and appliance-based consumption using the adjustment factor
    refined_daily_load_kwh = (base_consumption * (1 - adjustment_factor)) + (appliance_consumption * adjustment_factor)
    return refined_daily_load_kwh

# Function to calculate the refined total load
def refine_total_load(base_consumption_kwh_per_day, appliance_consumption_kwh_per_day):
    if appliance_consumption_kwh_per_day is None or appliance_consumption_kwh_per_day == 0:
        return base_consumption_kwh_per_day  # No appliance data provided; use base consumption
    else:
        # Compare and refine the base consumption
        refined_daily_load_kwh = compare_and_adjust_base_consumption(base_consumption_kwh_per_day, appliance_consumption_kwh_per_day)
        return refined_daily_load_kwh

# Function to calculate the system's components
def calculate_system_components(total_load_kwh, coverage_percentage, components_table, exchange_rate, battery_autonomy_hours, electricity_spend, price_band):
    load_covered_by_solar = total_load_kwh * (coverage_percentage / 100)

    # Solar panel calculations
    solar_energy_required = load_covered_by_solar / (1 - 0.20)  # 20% system losses
    panel_capacity_w = components_table['solar_panels'][0]['capacity_w']
    panel_output_per_day_kwh = (panel_capacity_w * 5) / 1000  # Assuming 5 sun hours per day
    number_of_panels = solar_energy_required / panel_output_per_day_kwh

    # Inverter calculations
    inverter_input_w = load_covered_by_solar * 1000
    inverter_size_w = inverter_input_w * 1.2  # Adding 20% safety margin
    inverter_capacity_w = components_table['inverters'][0]['capacity_w']
    number_of_inverters = inverter_size_w / inverter_capacity_w

    # Battery calculations based on customer input for battery autonomy in hours
    battery_capacity_kwh = load_covered_by_solar * (battery_autonomy_hours / 24)  # Adjust for hours of autonomy
    battery_efficiency = components_table['batteries'][0]['battery_efficiency'] / 100
    battery_dod = components_table['batteries'][0]['dod'] / 100
    effective_battery_capacity_kwh = battery_capacity_kwh / (battery_dod * battery_efficiency)
    battery_capacity_per_unit_kwh = components_table['batteries'][0]['capacity_kwh']
    number_of_batteries = effective_battery_capacity_kwh / battery_capacity_per_unit_kwh

    # Prices in USD from the components table
    panel_price_usd = components_table['solar_panels'][0]['price_usd']
    inverter_price_usd = components_table['inverters'][0]['price_usd']
    battery_price_usd = components_table['batteries'][0]['price_usd']

    # Convert prices to Naira
    panel_price_naira = panel_price_usd * exchange_rate
    inverter_price_naira = inverter_price_usd * exchange_rate
    battery_price_naira = battery_price_usd * exchange_rate

    # Total cost calculations
    total_panel_cost_usd = number_of_panels * panel_price_usd
    total_inverter_cost_usd = number_of_inverters * inverter_price_usd
    total_battery_cost_usd = number_of_batteries * battery_price_usd

    total_panel_cost_naira = number_of_panels * panel_price_naira
    total_inverter_cost_naira = number_of_inverters * inverter_price_naira
    total_battery_cost_naira = number_of_batteries * battery_price_naira

    total_cost_usd = total_panel_cost_usd + total_inverter_cost_usd + total_battery_cost_usd
    total_cost_naira = total_panel_cost_naira + total_inverter_cost_naira + total_battery_cost_naira

    # Miscellaneous and profit margin
    miscellaneous_cost = total_cost_naira * 0.20
    total_cost_with_profit = total_cost_naira + miscellaneous_cost + (total_cost_naira * 0.20)

    return {
        "total_load_kwh": total_load_kwh,
        "load_covered_by_solar": load_covered_by_solar,
        "total_equipments": round(number_of_panels+number_of_inverters+number_of_batteries),
        "number_of_panels": round(number_of_panels),
        "number_of_inverters": round(number_of_inverters),
        "number_of_batteries": round(number_of_batteries),
        "total_panel_cost_usd": round(total_panel_cost_usd, 2),
        "total_inverter_cost_usd": round(total_inverter_cost_usd, 2),
        "total_battery_cost_usd": round(total_battery_cost_usd, 2),
        "total_panel_cost_naira": round(total_panel_cost_naira),
        "total_inverter_cost_naira": round(total_inverter_cost_naira),
        "total_battery_cost_naira": round(total_battery_cost_naira),
        "total_cost_usd": round(total_cost_usd, 2),
        "total_cost_naira": round(total_cost_naira),
        "miscellaneous_cost": round(miscellaneous_cost),
        "total_cost_with_profit": round(total_cost_with_profit),
        "user_id": 1,
        "electricity_spend": round(electricity_spend, 2),
        "price_band": price_band
    }

# Function to calculate the financing details
def calculate_financing(total_cost_naira):
    down_payment = total_cost_naira * 0.30
    loan_amount = total_cost_naira - down_payment
    monthly_interest_rate = 0.075
    loan_term_months = 4 * 12  # 4 years

    # Calculate monthly payment using the formula
    monthly_payment = (loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months)) / (((1 + monthly_interest_rate) ** loan_term_months) - 1)

    return {
        "down_payment": round(down_payment, 2),
        "monthly_payment": round(monthly_payment, 2),
        "loan_amount": round(loan_amount, 2)
    }

# Function to calculate monthly savings and ROI
def calculate_savings_and_roi(monthly_spend, monthly_payment, loan_term_months, total_cost_with_profit):
    monthly_savings = monthly_spend - Decimal(monthly_payment)
    total_savings = monthly_savings * loan_term_months
    roi = (total_savings / total_cost_with_profit) * 100  # ROI in percentage

    return {
        "monthly_savings": round(monthly_savings, 2),
        "roi": round(roi, 2)
    }

def calculate_quote(monthly_spend, band_group, coverage_percentage=None, battery_autonomy_hours=None, breakdowns=None):
    # Load components from the JSON file
    components_table = load_components_table()

    if components_table is None:
        raise ValueError("components_table cannot be None")

    if 'solar_panels' not in components_table or not components_table['solar_panels']:
        raise ValueError("components_table must contain a non-empty 'solar_panels' list")


    # # Example customer inputs
    # monthly_spend = float(input("Enter your monthly spend on electricity (in Naira): "))
    # band_group = input("Enter your band group (A, B, or C): ").upper()

    # Validate band group before proceeding
    # if band_group not in ['A', 'B', 'C']:
    #     print("Error: Please specify a valid band group (A, B, or C).")
    #     exit()

    coverage_percentage = float(coverage_percentage or 50)
    battery_autonomy_hours = float(battery_autonomy_hours or 10)

    # Load exchange rate (USD to NGN)
    api_key = '8bd4f7fa32220748df03958d'  # ExchangeRate API key
    exchange_rate = get_exchange_rate(api_key, 'USD', 'NGN')

    # Base consumption calculation
    base_consumption_kwh_per_day = calculate_base_consumption(monthly_spend, band_group)

    breakdowns = breakdowns or {}

    # Optional appliance data input
    appliances = [
        {"name": "Lighting (LED bulb)", "power_w": 8, "hours_per_day": float(breakdowns.get('lighting_usage') or 0), "quantity": int(breakdowns.get('lighting_quantity') or 0)},
        {"name": "Fridge", "power_w": 150, "hours_per_day": float(breakdowns.get('fridge_usage') or 0), "quantity": int(breakdowns.get('fridge_quantity') or 0)},
        {"name": "Freezer", "power_w": 250, "hours_per_day": float(breakdowns.get('freezer_usage') or 0), "quantity": int(breakdowns.get('freezer_quantity') or 0)},
        {"name": "Microwave", "power_w": 1200, "hours_per_day": float(breakdowns.get('microwave_usage') or 0), "quantity": int(breakdowns.get('microwave_quantity') or 0)},
        {"name": "Oven", "power_w": 2000, "hours_per_day": float(breakdowns.get('oven_usage') or 0), "quantity": int(breakdowns.get('oven_quantity') or 0)},
        {"name": "Toaster", "power_w": 800, "hours_per_day": float(breakdowns.get('toaster_usage') or 0), "quantity": int(breakdowns.get('toaster_quantity') or 0)},
        {"name": "Blender", "power_w": 500, "hours_per_day": float(breakdowns.get('blender_usage') or 0), "quantity": int(breakdowns.get('blender_quantity') or 0)},
        {"name": "Coffee Maker", "power_w": 600, "hours_per_day": float(breakdowns.get('coffee_maker_usage') or 0), "quantity": int(breakdowns.get('coffee_maker_quantity') or 0)},
        {"name": "Kettle", "power_w": 3000, "hours_per_day": float(breakdowns.get('kettle_usage') or 0), "quantity": int(breakdowns.get('kettle_quantity') or 0)},
        {"name": "Laptop", "power_w": 75, "hours_per_day": float(breakdowns.get('laptop_usage') or 0), "quantity": int(breakdowns.get('laptop_quantity') or 0)},
        {"name": "Desktop Computer", "power_w": 200, "hours_per_day": float(breakdowns.get('desktop_usage') or 0), "quantity": int(breakdowns.get('desktop_quantity') or 0)},
        {"name": "Television", "power_w": 300, "hours_per_day": float(breakdowns.get('television_usage') or 0), "quantity": int(breakdowns.get('television_quantity') or 0)},
        {"name": "Water Heater", "power_w": 1200, "hours_per_day": float(breakdowns.get('water_heater_usage') or 0), "quantity": int(breakdowns.get('water_heater_quantity') or 0)},
        {"name": "Washing Machine", "power_w": 500, "hours_per_day": float(breakdowns.get('washing_machine_usage') or 0), "quantity": int(breakdowns.get('washing_machine_quantity') or 0)},
        {"name": "Dryer", "power_w": 2160, "hours_per_day": float(breakdowns.get('dryer_usage') or 0), "quantity": int(breakdowns.get('dryer_quantity') or 0)},
        {"name": "Electric Car", "power_w": 6500, "hours_per_day": float(breakdowns.get('electric_car_usage') or 0), "quantity": int(breakdowns.get('electric_car_quantity') or 0)},
        {"name": "Other Appliances", "power_w": 500, "hours_per_day": float(breakdowns.get('other_appliances_usage') or 0), "quantity": int(breakdowns.get('other_appliances_quantity') or 0)}
    ]

    # Calculate appliance-based consumption if provided
    appliance_consumption_kwh_per_day = calculate_appliance_based_consumption(appliances)

    # Refine the total load
    total_load_kwh_per_day = refine_total_load(base_consumption_kwh_per_day, appliance_consumption_kwh_per_day)

    # System component calculations
    system_details = calculate_system_components(total_load_kwh_per_day, coverage_percentage, components_table, exchange_rate, battery_autonomy_hours, monthly_spend, band_group)

    # Financing calculations based on total cost without profit margin
    financing_details = calculate_financing(system_details['total_cost_naira'])

    # Calculate monthly savings and ROI
    loan_term_months = 4 * 12  # 4 years
    savings_and_roi = calculate_savings_and_roi(monthly_spend, financing_details['monthly_payment'], loan_term_months, system_details['total_cost_with_profit'])

    # Output the results
    print(f"\nTotal Daily Load: {total_load_kwh_per_day:.2f} kWh/day")
    print(f"Load Covered by Solar: {system_details['load_covered_by_solar']:.2f} kWh/day")
    print(f"Number of Solar Panels: {system_details['number_of_panels']}")
    print(f"Number of Inverters: {system_details['number_of_inverters']}")
    print(f"Number of Batteries: {system_details['number_of_batteries']}")
    print(f"Total Panel Cost: {system_details['total_panel_cost_usd']} USD ({system_details['total_panel_cost_naira']} Naira)")
    print(f"Total Inverter Cost: {system_details['total_inverter_cost_usd']} USD ({system_details['total_inverter_cost_naira']} Naira)")
    print(f"Total Battery Cost: {system_details['total_battery_cost_usd']} USD ({system_details['total_battery_cost_naira']} Naira)")
    print(f"Total System Cost (without profit): {system_details['total_cost_usd']} USD ({system_details['total_cost_naira']} Naira)")
    print(f"Total System Cost with Profit: {system_details['total_cost_with_profit']} Naira")

    # Financing information
    print("\nFinancing Information:")
    print(f"Downpayment (30%): {financing_details['down_payment']} Naira")
    print(f"Monthly Payment: {financing_details['monthly_payment']} Naira")
    print(f"Loan Amount: {financing_details['loan_amount']} Naira")

    # Savings and ROI information
    print("\nSavings and ROI Information:")
    print(f"Monthly Savings Compared to Grid: {savings_and_roi['monthly_savings']} Naira")
    print(f"Customer ROI: {savings_and_roi['roi']} %")
    return system_details
