import os
import json
import requests
from decimal import Decimal
from product.models import Product
from setting.models import Settings
from django.db.models import Max


# Load exchange rate using ExchangeRate API
def get_exchange_rate(api_key, base_currency, target_currency):
    """Fetch the current exchange rate from an external API."""
    try:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()

        if "conversion_rates" in data and target_currency in data["conversion_rates"]:
            return data["conversion_rates"][target_currency]
        else:
            print("Error: Unable to fetch exchange rate.")
            return 450  # Default exchange rate
    except requests.RequestException as e:
        print(f"Error: Network problem occurred: {e}")
        return 450  # Default exchange rate if a network error occurs


# Function to calculate the base consumption based on the monthly spend and band group
def calculate_base_consumption(monthly_spend, band_group):
    band_prices = {"A": 209.5, "B": 67.96, "C": 53.49}  # Price per kWh for each band
    hours_supply = {"A": 20, "B": 16, "C": 12}  # Hours of electricity supply per day

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
        power = appliance["power_w"]
        hours_per_day = appliance["hours_per_day"]
        quantity = appliance["quantity"]
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
    refined_daily_load_kwh = (base_consumption * (1 - adjustment_factor)) + (
        appliance_consumption * adjustment_factor
    )
    return refined_daily_load_kwh


# Function to calculate the refined total load
def refine_total_load(base_consumption_kwh_per_day, appliance_consumption_kwh_per_day):
    if (
        appliance_consumption_kwh_per_day is None
        or appliance_consumption_kwh_per_day == 0
    ):
        return base_consumption_kwh_per_day  # No appliance data provided; use base consumption
    else:
        # Compare and refine the base consumption
        refined_daily_load_kwh = compare_and_adjust_base_consumption(
            base_consumption_kwh_per_day, appliance_consumption_kwh_per_day
        )
        return refined_daily_load_kwh


# Function to select the best component based on minimum requirements
def select_best_component(category_id, required_capacity):
    # Try to find a suitable component with capacity >= required_capacity
    suitable_component = Product.objects.filter(
        category_id=category_id, capacity_w__gte=required_capacity
    ).first()

    if suitable_component:
        return suitable_component

    # If no suitable component found, get the product with the maximum capacity
    suitable_component = (
        Product.objects.filter(category_id=category_id).order_by("-capacity_w").first()
    )

    return suitable_component


# Function to calculate the system's components
def calculate_system_components(
    total_load_kwh,
    coverage_percentage,
    exchange_rate,
    battery_autonomy_hours,
    electricity_spend,
    price_band,
):
    print("\ncoverage_percentage:", coverage_percentage)
    if coverage_percentage and coverage_percentage is not None:
        load_covered_by_solar = total_load_kwh * (coverage_percentage / 100)
        print("\load_covered_by_solar:", load_covered_by_solar)
        solar_energy_required = load_covered_by_solar / (1 - 0.20)  # 20% system losses
        print("\solar_energy_required:", solar_energy_required)
    else:
        load_covered_by_solar = 0.0
        solar_energy_required = 0.0

    # Selecting best solar panel
    panel_required_output_kwh = (
        solar_energy_required / 5
    )  # Assuming 5 sun hours per day

    print("\n panel_required_output_kwh:", panel_required_output_kwh * 1000)
    best_panel = select_best_component(1, panel_required_output_kwh * 1000)

    print("\n best_panel:", best_panel)

    # Check if the capacity_w value is not null or empty
    if best_panel and best_panel.capacity_w is not None:
        print("\n best_panel.capacity_w:", best_panel.capacity_w)
        panel_output_per_day_kwh = (float(best_panel.capacity_w) * 5) / 1000
    else:
        panel_output_per_day_kwh = 0.0  # or another default value

    # Check if solar_energy_required and panel_output_per_day_kwh are valid
    print("\n solar_energy_required:", solar_energy_required)
    print("\n panel_output_per_day_kwh:", panel_output_per_day_kwh)

    if solar_energy_required and panel_output_per_day_kwh:
        number_of_panels = solar_energy_required / panel_output_per_day_kwh
    else:
        number_of_panels = 0  # or another default value

    print("\n number_of_panels:", number_of_panels)

    # Selecting best inverter
    print("\n load_covered_by_solar:", load_covered_by_solar)
    inverter_input_w = load_covered_by_solar * 1000
    print("\n inverter_input_w:", inverter_input_w)
    inverter_size_w = inverter_input_w * 1.2
    best_inverter = select_best_component(2, inverter_size_w)
    print("\n inverter_size_w", inverter_size_w)
    print("\n best_inverter", best_inverter)

    # Check if the capacity_w value is not null or zero
    if best_inverter and best_inverter.capacity_w is not None:
        print("\n best_inverter.capacity_w:", best_inverter.capacity_w)
        number_of_inverters = inverter_size_w / float(best_inverter.capacity_w)
    else:
        number_of_inverters = 0  # or another default value

    # Selecting best battery
    battery_capacity_kwh = load_covered_by_solar * (battery_autonomy_hours / 24)

    print("\n battery_capacity_kwh:", battery_capacity_kwh)

    best_battery = select_best_component(3, battery_capacity_kwh)

    print("\n best_battery", best_battery)

    effective_battery_capacity_kwh = battery_capacity_kwh / (
        float(best_battery.dod) / 100 * float(best_battery.efficiency) / 100
    )

    print("\n effective_battery_capacity_kwh:", effective_battery_capacity_kwh)

    if best_battery and best_battery.capacity_w is not None:
        number_of_batteries = effective_battery_capacity_kwh / float(
            best_battery.capacity_w
        )
    else:
        number_of_batteries = 0

    # Check if the prices are not null or empty

    if best_panel and best_panel.price_usd is not None:
        panel_price_usd = float(best_panel.price_usd)
    else:
        panel_price_usd = 0

    if best_inverter and best_inverter.price_usd is not None:
        inverter_price_usd = float(best_inverter.price_usd)
    else:
        inverter_price_usd = 0

    if best_battery and best_battery.price_usd is not None:
        battery_price_usd = float(best_battery.price_usd)
    else:
        battery_price_usd = 0

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

    total_cost_usd = (
        total_panel_cost_usd + total_inverter_cost_usd + total_battery_cost_usd
    )
    total_cost_naira = (
        total_panel_cost_naira + total_inverter_cost_naira + total_battery_cost_naira
    )

    systemSetting = Settings.objects.first()

    if systemSetting and systemSetting.profit_margin_outright is not None:
        profit_margin_outright = float(systemSetting.profit_margin_outright)
    else:
        profit_margin_outright = 30
    if systemSetting and systemSetting.profit_margin_financing is not None:
        profit_margin_financing = float(systemSetting.profit_margin_financing)
    else:
        profit_margin_financing = 20

    if systemSetting and systemSetting.installation_margin is not None:
        installation_margin = float(systemSetting.installation_margin)
    else:
        installation_margin = 15

    if systemSetting and systemSetting.installer_commission is not None:
        installer_commission = float(systemSetting.installer_commission)
    else:
        installer_commission = 2

    # Miscellaneous and profit margin
    installation_and_cabling = total_cost_naira * installation_margin / 100
    installer_commission_amount = total_cost_naira * installer_commission / 100
    profit_margin_outright_amount = total_cost_naira * profit_margin_outright / 100
    profit_margin_financing_amount = total_cost_naira * profit_margin_financing / 100

    # 20% profit margin calculate from back office
    total_cost_with_profit_outright = (
        total_cost_naira
        + installation_and_cabling
        + installer_commission_amount
        + profit_margin_outright_amount
    )

    total_cost_with_profit_financing = (
        total_cost_naira
        + installation_and_cabling
        + installer_commission_amount
        + profit_margin_financing_amount
    )

    if systemSetting and systemSetting.vat is not None:
        vat = float(systemSetting.vat)
    else:
        vat = 7.5  # Default VAT rate if not found in settings

    total_vat_outright = total_cost_with_profit_outright * vat / 100
    total_vat_financing = total_cost_with_profit_financing * vat / 100

    return {
        "total_load_kwh": total_load_kwh,
        "load_covered_by_solar": load_covered_by_solar,
        "total_equipments": round(
            number_of_panels + number_of_inverters + number_of_batteries
        ),
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
        "installation_and_cabling": round(installation_and_cabling),
        "total_cost_with_profit_outright": round(total_cost_with_profit_outright),
        "total_cost_with_profit_financing": round(total_cost_with_profit_financing),
        "user_id": 1,
        "electricity_spend": round(electricity_spend, 2),
        "installer_commission": round(installer_commission),
        "installer_commission_amount": round(installer_commission_amount),
        "price_band": price_band,
        "vat": vat,
        "total_vat_outright": total_vat_outright,
        "total_vat_financing": total_vat_financing,
    }


# Function to calculate the financing details
def calculate_financing(total_cost_naira):
    down_payment = total_cost_naira * 0.30
    loan_amount = total_cost_naira - down_payment
    monthly_interest_rate = 0.075
    loan_term_months = 4 * 12  # 4 years

    # Calculate monthly payment using the formula
    monthly_payment = (
        loan_amount
        * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months)
    ) / (((1 + monthly_interest_rate) ** loan_term_months) - 1)

    return {
        "down_payment": round(down_payment, 2),
        "monthly_payment": round(monthly_payment, 2),
        "loan_amount": round(loan_amount, 2),
    }


# Function to calculate monthly savings and ROI
def calculate_savings_and_roi(
    monthly_spend, monthly_payment, loan_term_months, total_cost_with_profit
):
    monthly_savings = monthly_spend - Decimal(monthly_payment)
    total_savings = monthly_savings * loan_term_months

    if total_cost_with_profit != 0:
        roi = (total_savings / total_cost_with_profit) * 100  # ROI in percentage
    else:
        roi = 0

    return {"monthly_savings": round(monthly_savings, 2), "roi": round(roi, 2)}


def calculate_quote(
    monthly_spend,
    band_group,
    coverage_percentage=None,
    battery_autonomy_hours=None,
    breakdowns=None,
):

    coverage_percentage = float(coverage_percentage or 0)
    battery_autonomy_hours = float(battery_autonomy_hours or 8)

    # Load exchange rate (USD to NGN)
    api_key = "8bd4f7fa32220748df03958d"  # ExchangeRate API key
    exchange_rate = get_exchange_rate(api_key, "USD", "NGN")

    print(f"\n Monthly Spend: {monthly_spend}")
    print(f"\n Band Group: {band_group}")
    print(f"\n coverage_percentage: {coverage_percentage}")
    print(f"\n battery_autonomy_hours: {battery_autonomy_hours}")

    # Base consumption calculation
    base_consumption_kwh_per_day = calculate_base_consumption(monthly_spend, band_group)

    breakdowns = breakdowns or {}

    # Optional appliance data input
    appliances = [
        {
            "name": "Lighting (LED bulb)",
            "power_w": 8,
            "hours_per_day": float(breakdowns.get("lighting_usage") or 0),
            "quantity": int(breakdowns.get("lighting_quantity") or 0),
        },
        {
            "name": "Fridge",
            "power_w": 150,
            "hours_per_day": float(breakdowns.get("fridge_usage") or 0),
            "quantity": int(breakdowns.get("fridge_quantity") or 0),
        },
        {
            "name": "Freezer",
            "power_w": 250,
            "hours_per_day": float(breakdowns.get("freezer_usage") or 0),
            "quantity": int(breakdowns.get("freezer_quantity") or 0),
        },
        {
            "name": "Microwave",
            "power_w": 1200,
            "hours_per_day": float(breakdowns.get("microwave_usage") or 0),
            "quantity": int(breakdowns.get("microwave_quantity") or 0),
        },
        {
            "name": "Oven",
            "power_w": 2000,
            "hours_per_day": float(breakdowns.get("oven_usage") or 0),
            "quantity": int(breakdowns.get("oven_quantity") or 0),
        },
        {
            "name": "Toaster",
            "power_w": 800,
            "hours_per_day": float(breakdowns.get("toaster_usage") or 0),
            "quantity": int(breakdowns.get("toaster_quantity") or 0),
        },
        {
            "name": "Blender",
            "power_w": 500,
            "hours_per_day": float(breakdowns.get("blender_usage") or 0),
            "quantity": int(breakdowns.get("blender_quantity") or 0),
        },
        {
            "name": "Coffee Maker",
            "power_w": 600,
            "hours_per_day": float(breakdowns.get("coffee_maker_usage") or 0),
            "quantity": int(breakdowns.get("coffee_maker_quantity") or 0),
        },
        {
            "name": "Kettle",
            "power_w": 3000,
            "hours_per_day": float(breakdowns.get("kettle_usage") or 0),
            "quantity": int(breakdowns.get("kettle_quantity") or 0),
        },
        {
            "name": "Laptop",
            "power_w": 75,
            "hours_per_day": float(breakdowns.get("laptop_usage") or 0),
            "quantity": int(breakdowns.get("laptop_quantity") or 0),
        },
        {
            "name": "Desktop Computer",
            "power_w": 200,
            "hours_per_day": float(breakdowns.get("desktop_usage") or 0),
            "quantity": int(breakdowns.get("desktop_quantity") or 0),
        },
        {
            "name": "Television",
            "power_w": 300,
            "hours_per_day": float(breakdowns.get("television_usage") or 0),
            "quantity": int(breakdowns.get("television_quantity") or 0),
        },
        {
            "name": "Water Heater",
            "power_w": 1200,
            "hours_per_day": float(breakdowns.get("water_heater_usage") or 0),
            "quantity": int(breakdowns.get("water_heater_quantity") or 0),
        },
        {
            "name": "Washing Machine",
            "power_w": 500,
            "hours_per_day": float(breakdowns.get("washing_machine_usage") or 0),
            "quantity": int(breakdowns.get("washing_machine_quantity") or 0),
        },
        {
            "name": "Dryer",
            "power_w": 2160,
            "hours_per_day": float(breakdowns.get("dryer_usage") or 0),
            "quantity": int(breakdowns.get("dryer_quantity") or 0),
        },
        {
            "name": "Electric Car",
            "power_w": 6500,
            "hours_per_day": float(breakdowns.get("electric_car_usage") or 0),
            "quantity": int(breakdowns.get("electric_car_quantity") or 0),
        },
        {
            "name": "Other Appliances",
            "power_w": 500,
            "hours_per_day": float(breakdowns.get("other_appliances_usage") or 0),
            "quantity": int(breakdowns.get("other_appliances_quantity") or 0),
        },
    ]

    # Calculate appliance-based consumption if provided
    appliance_consumption_kwh_per_day = calculate_appliance_based_consumption(
        appliances
    )

    # Refine the total load
    total_load_kwh_per_day = refine_total_load(
        base_consumption_kwh_per_day, appliance_consumption_kwh_per_day
    )

    # System component calculations
    system_details = calculate_system_components(
        total_load_kwh_per_day,
        coverage_percentage,
        exchange_rate,
        battery_autonomy_hours,
        monthly_spend,
        band_group,
    )

    # Financing calculations based on total cost without profit margin
    financing_details = calculate_financing(system_details["total_cost_naira"])

    # Calculate monthly savings and ROI
    loan_term_months = 4 * 12  # 4 years
    savings_and_roi = calculate_savings_and_roi(
        monthly_spend,
        financing_details["monthly_payment"],
        loan_term_months,
        system_details["total_cost_with_profit_outright"],
    )

    # Output the results
    print(f"\nTotal Daily Load: {total_load_kwh_per_day:.2f} kWh/day")
    print(
        f"Load Covered by Solar: {system_details['load_covered_by_solar']:.2f} kWh/day"
    )
    print(f"Number of Solar Panels: {system_details['number_of_panels']}")
    print(f"Number of Inverters: {system_details['number_of_inverters']}")
    print(f"Number of Batteries: {system_details['number_of_batteries']}")
    print(
        f"Total Panel Cost: {system_details['total_panel_cost_usd']} USD ({system_details['total_panel_cost_naira']} Naira)"
    )
    print(
        f"Total Inverter Cost: {system_details['total_inverter_cost_usd']} USD ({system_details['total_inverter_cost_naira']} Naira)"
    )
    print(
        f"Total Battery Cost: {system_details['total_battery_cost_usd']} USD ({system_details['total_battery_cost_naira']} Naira)"
    )
    print(
        f"Total System Cost (without profit): {system_details['total_cost_usd']} USD ({system_details['total_cost_naira']} Naira)"
    )
    print(
        f"Total System Cost with Profit: {system_details['total_cost_with_profit_outright']} Naira"
    )

    # Financing information
    print("\nFinancing Information:")
    print(f"Downpayment (30%): {financing_details['down_payment']} Naira")
    print(f"Monthly Payment: {financing_details['monthly_payment']} Naira")
    print(f"Loan Amount: {financing_details['loan_amount']} Naira")

    # Savings and ROI information
    print("\nSavings and ROI Information:")
    print(
        f"Monthly Savings Compared to Grid: {savings_and_roi['monthly_savings']} Naira"
    )
    print(f"Customer ROI: {savings_and_roi['roi']} %")
    return system_details
