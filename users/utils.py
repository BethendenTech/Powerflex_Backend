import requests
from decimal import Decimal
from product.models import Product, Appliance
from setting.models import Settings
from users.models import Quote
from django.forms.models import model_to_dict


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

    for value in appliances:
        appliance_id = value.get("appliance_id")
        usage = value.get("usage")
        quantity = value.get("quantity")

        if appliance_id:
            # Retrieve appliance data from the database
            applianceData = Appliance.objects.filter(id=appliance_id).first()
            if applianceData:  # Check if the appliance exists
                # Calculate the consumption and add it to the total
                total_appliance_consumption_kwh += (
                    applianceData.power_w * usage * quantity
                ) / 1000
            else:
                print(f"Appliance with ID {appliance_id} not found.")

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
    is_finance,
):

    if coverage_percentage and coverage_percentage is not None:
        load_covered_by_solar = total_load_kwh * (coverage_percentage / 100)
        solar_energy_required = load_covered_by_solar / (1 - 0.20)  # 20% system losses
    else:
        load_covered_by_solar = 0.0
        solar_energy_required = 0.0

    # Selecting best solar panel
    panel_required_output_kwh = (
        solar_energy_required / 6
    )  # Assuming 6 sun hours per day

    best_panel = select_best_component(1, panel_required_output_kwh * 1000)

    # Check if the capacity_w value is not null or empty
    if best_panel and best_panel.capacity_w is not None:
        panel_output_per_day_kwh = (float(best_panel.capacity_w) * 6) / 1000
    else:
        panel_output_per_day_kwh = 0.0  # or another default value

    # Check if solar_energy_required and panel_output_per_day_kwh are valid
    if solar_energy_required and panel_output_per_day_kwh:
        number_of_panels = solar_energy_required / panel_output_per_day_kwh
    else:
        number_of_panels = 0  # or another default value

    # Selecting best inverter
    inverter_input_w = load_covered_by_solar * 1000
    inverter_size_w = inverter_input_w * 1.2
    best_inverter = select_best_component(2, inverter_size_w)

    # Check if the capacity_w value is not null or zero
    if best_inverter and best_inverter.capacity_w is not None:
        number_of_inverters = inverter_size_w / float(best_inverter.capacity_w)
    else:
        number_of_inverters = 0  # or another default value

    # Selecting best battery
    battery_capacity_kwh = load_covered_by_solar * (battery_autonomy_hours / 24)

    best_battery = select_best_component(3, battery_capacity_kwh)

    effective_battery_capacity_kwh = battery_capacity_kwh / (
        float(best_battery.dod) / 100 * float(best_battery.efficiency) / 100
    )

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

    # Total cost calculations
    total_panel_cost_usd = number_of_panels * panel_price_usd
    total_inverter_cost_usd = number_of_inverters * inverter_price_usd
    total_battery_cost_usd = number_of_batteries * battery_price_usd

    products = {
        "best_panel": model_to_dict(best_panel),
        "best_inverter": model_to_dict(best_inverter),
        "best_battery": model_to_dict(best_battery),
        "battery_capacity_kwh": (battery_capacity_kwh),
        "effective_battery_capacity_kwh": (effective_battery_capacity_kwh),
        "number_of_panels": round(number_of_panels),
        "number_of_inverters": round(number_of_inverters),
        "number_of_batteries": round(number_of_batteries),
        "panel_price_usd": round(panel_price_usd, 2),
        "inverter_price_usd": round(inverter_price_usd, 2),
        "battery_price_usd": round(battery_price_usd, 2),
        "total_panel_cost_usd": round(total_panel_cost_usd, 2),
        "total_inverter_cost_usd": round(total_inverter_cost_usd, 2),
        "total_battery_cost_usd": round(total_battery_cost_usd, 2),
        "total_panel_cost_naira": round(total_panel_cost_usd * exchange_rate),
        "total_inverter_cost_naira": round(total_inverter_cost_usd * exchange_rate),
        "total_battery_cost_naira": round(total_battery_cost_usd * exchange_rate),
    }

    print("products", products)

    total_cost_usd = (
        total_panel_cost_usd + total_inverter_cost_usd + total_battery_cost_usd
    )

    total_cost_naira = total_cost_usd * exchange_rate

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

    if is_finance:
        profit_margin_amount = total_cost_naira * profit_margin_financing / 100
    else:
        profit_margin_amount = total_cost_naira * profit_margin_outright / 100

    # 20% profit margin calculate from back office
    total_cost_with_profit = (
        total_cost_naira
        + installation_and_cabling
        + installer_commission_amount
        + profit_margin_amount
    )

    if systemSetting and systemSetting.vat is not None:
        vat = float(systemSetting.vat)
    else:
        vat = 7.5  # Default VAT rate if not found in settings

    total_vat = total_cost_with_profit * vat / 100

    return {
        "total_load_kwh": total_load_kwh,
        "load_covered_by_solar": load_covered_by_solar,
        "total_equipments": round(
            number_of_panels + number_of_inverters + number_of_batteries
        ),
        "total_cost_usd": round(total_cost_usd, 2),
        "total_cost_naira": round(total_cost_naira),
        "installation_and_cabling": round(installation_and_cabling),
        "total_cost_with_profit": round(total_cost_with_profit),
        "electricity_spend": round(electricity_spend, 2),
        "installer_commission": round(installer_commission),
        "installer_commission_amount": round(installer_commission_amount),
        "price_band": price_band,
        "vat": vat,
        "total_vat": total_vat,
        "products": products,
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
    is_finance=False,
):
    coverage_percentage = float(coverage_percentage or 0)
    battery_autonomy_hours = float(battery_autonomy_hours or 8)

    # Load exchange rate (USD to NGN)
    # api_key = "8bd4f7fa32220748df03958d"  # ExchangeRate API key
    # exchange_rate = get_exchange_rate(api_key, "USD", "NGN")

    systemSetting = Settings.objects.first()

    if systemSetting and systemSetting.exchange_rate is not None:
        exchange_rate = float(systemSetting.exchange_rate)
    else:
        exchange_rate = 1800

    # Base consumption calculation
    base_consumption_kwh_per_day = calculate_base_consumption(monthly_spend, band_group)

    breakdowns = breakdowns or {}

    # Calculate appliance-based consumption if provided
    appliance_consumption_kwh_per_day = calculate_appliance_based_consumption(
        breakdowns
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
        is_finance,
    )

    print("system_details", system_details)

    # Financing calculations based on total cost without profit margin
    financing_details = calculate_financing(system_details["total_cost_naira"])

    # Calculate monthly savings and ROI
    loan_term_months = 4 * 12  # 4 years
    savings_and_roi = calculate_savings_and_roi(
        monthly_spend,
        financing_details["monthly_payment"],
        loan_term_months,
        system_details["total_cost_with_profit"],
    )

    system_details["savings_and_roi"] = savings_and_roi

    return system_details


def generate_quote_number():
    last_quote = Quote.objects.order_by("id").last()
    if last_quote:
        new_id = int(last_quote.quote_number[3:]) + 1
        return f"PFX{str(new_id).zfill(10)}"
    else:
        return "PFX0000000001"
