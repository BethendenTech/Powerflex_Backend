import requests
from decimal import Decimal
from product.models import Product, Appliance, Band
from setting.models import Settings
from users.models import Quote
from django.forms.models import model_to_dict
from django.db.models import Min


def safe_model_to_dict(instance):
    return model_to_dict(instance) if instance else None


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

    # Retrieve band data from the database
    band_data = Band.objects.get(id=band_group)

    if band_data:
        price_per_kwh = band_data.price
        hours_per_day = band_data.hours_supply
    else:
        raise ValueError("Error: Band data not found for the specified group")

    # Calculate base consumption considering the hours of electricity supply
    base_consumption_kwh_per_month = float(monthly_spend) / price_per_kwh

    base_daily_consumption_kwh = float(base_consumption_kwh_per_month) / 30

    return base_daily_consumption_kwh
    # Adjust base consumption to the actual number of hours supply for the band group
    # adjusted_daily_consumption_kwh = base_daily_consumption_kwh * (24 / hours_per_day)
    # return adjusted_daily_consumption_kwh


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


# # Function to select the best component or multiple identical components
def select_best_component(category_id, required_capacity, system_voltage=None):
    """
    Selects the best single component or multiple identical components
    to efficiently meet or exceed the required capacity.

    Parameters:
        category_id (int): Component category (1=Solar Panel, 2=Inverter, 3=Battery).
        required_capacity (float): The total required power in watts (W).
        system_voltage (int, optional): Required voltage (for inverters & batteries).

    Returns:
        dict: Selected component and the number of identical units required.
    """
    query = Product.objects.filter(category_id=category_id)

    if system_voltage is not None and category_id in [
        2,
        3,
    ]:  # Inverters & Batteries only
        query = query.filter(voltage__gte=system_voltage)

    available_components = list(
        query.order_by("-capacity_w")
    )  # Sort by highest capacity first

    print("available_components", category_id, available_components)

    if not available_components:
        raise ValueError(
            f"No suitable component found for category {category_id} and voltage {system_voltage}"
        )

    best_component = None
    num_units_required = 0

    for component in available_components:
        component_wattage = component.capacity_w

        # If a single unit is enough, select it
        if component_wattage >= required_capacity:
            return {"component": component, "quantity": 1}

        # If not, calculate how many of this component type are required
        num_units_required = -(
            -required_capacity // component_wattage
        )  # Equivalent to ceil(required_capacity / component_wattage)
        best_component = component
        break  # Stop at the first valid component

    if best_component:
        return {"component": best_component, "quantity": num_units_required}

    raise ValueError(
        f"Unable to meet {required_capacity}W requirement with available components."
    )


# Function to determine the best system voltage based on daily energy consumption
def determine_system_voltage(daily_energy_Wh):
    print("daily_energy_Wh", daily_energy_Wh)
    if daily_energy_Wh <= 2000:  # <2kWh
        return 12
    elif daily_energy_Wh <= 5000:  # 2-5kWh
        return 24
    else:  # >5kWh
        return 48


# Function to calculate the system's components
def calculate_system_components(
    total_load_kwh,
    coverage_percentage,
    exchange_rate,
    battery_autonomy_hours,
    monthly_spend,
    band_group,
    is_finance,
):
    """
    Calculates the best system components (inverter, battery, and solar panel)
    based on the refined total energy load and available products.
    """
    print("coverage_percentage", coverage_percentage)
    # **Step 1: Determine the Energy Covered by Solar**
    load_covered_by_solar = total_load_kwh * (coverage_percentage / 100)
    solar_energy_required = load_covered_by_solar

    print("solar_energy_required", solar_energy_required)

    # **Step 2: Select System Voltage**
    system_voltage = determine_system_voltage(solar_energy_required * 1000)

    print("system_voltage", system_voltage)

    # **Step 3: Solar Panel Selection**
    solar_efficiency = 0.8
    peak_sun_hours = 4
    solar_losses = 1.05
    future_growth_factor = 1.2

    solar_power_required_kW = (solar_energy_required * future_growth_factor) / (
        peak_sun_hours * solar_efficiency
    )

    print("solar_power_required_kW", solar_power_required_kW)

    solar_power_required_losses_adj_W = solar_power_required_kW * solar_losses * 1000

    print("solar_power_required_losses_adj_W", solar_power_required_losses_adj_W)

    best_panel = select_best_component(1, solar_power_required_losses_adj_W)
    print("best_panel", best_panel)
    print('best_panel["component"].capacity_w', best_panel["component"].capacity_w)
    number_of_panels = (
        solar_power_required_losses_adj_W / best_panel["component"].capacity_w
        if best_panel and best_panel["component"].capacity_w > 0
        else 0
    )

    print("number_of_panels", number_of_panels)

    # **Step 4: Inverter Selection**
    best_inverter = select_best_component(
        2, solar_power_required_losses_adj_W, system_voltage
    )

    print("best_inverter", best_inverter)

    if best_inverter:
        efficiency_inverter = (
            best_inverter["component"].efficiency
            if best_inverter["component"].efficiency
            else 0.9
        )
        print("efficiency_inverter", efficiency_inverter)
        power_factor = 0.8
        safety_margin = 1.2

        inverter_size_VA = (solar_power_required_losses_adj_W * safety_margin) / (
            efficiency_inverter * power_factor
        )
        number_of_inverters = best_inverter["quantity"]
    else:
        efficiency_inverter = 0.9
        inverter_size_VA = 0
        number_of_inverters = 0

    print("inverter_size_VA", inverter_size_VA)

    # *Step 5: Battery Selection (Using Ah instead of W)*

    battery_energy_required_Wh = solar_energy_required * 1000 * future_growth_factor

    # Convert required energy to Ah (instead of W)
    battery_capacity_Ah_required = battery_energy_required_Wh / (
        system_voltage * battery_autonomy_hours
    )
    print("battery_capacity_Ah_required", battery_capacity_Ah_required)
    # Select best battery using Ah directly from the database

    best_battery = select_best_component(
        3, battery_capacity_Ah_required, system_voltage
    )

    print("best_battery", best_battery)
    if best_battery:
        battery_efficiency = best_battery["component"].efficiency or 0.9
        battery_voltage = best_battery["component"].voltage or system_voltage
        battery_charge_ah = best_battery["component"].capacity_ah or 200

        depth_of_discharge = 0.6
        temperature_factor = 0.95

        daily_system_charge_required_Ah = battery_energy_required_Wh / battery_voltage
        battery_capacity_Ah = daily_system_charge_required_Ah / (
            depth_of_discharge * battery_efficiency * temperature_factor
        )

        batteries_in_series = system_voltage / battery_voltage
        batteries_in_parallel = battery_capacity_Ah / battery_charge_ah
        total_batteries_needed = batteries_in_series * batteries_in_parallel
    else:
        battery_efficiency = 0.9
        battery_voltage = system_voltage
        battery_charge_ah = 200
        total_batteries_needed = 0
        battery_energy_required_Wh = 0
        daily_system_charge_required_Ah = 0
        battery_capacity_Ah = 0
        batteries_in_series = 0
        batteries_in_parallel = 0

    print("battery_capacity_Ah", battery_capacity_Ah)

    print("total_batteries_needed", total_batteries_needed)

    # **Step 6: Retrieve Prices & Calculate Costs**
    panel_price_usd = float(best_panel["component"].price_usd or 0) if best_panel else 0
    inverter_price_usd = (
        float(best_inverter["component"].price_usd or 0) if best_inverter else 0
    )
    battery_price_usd = (
        float(best_battery["component"].price_usd or 0) if best_battery else 0
    )

    total_cost_usd = (
        (number_of_panels * panel_price_usd)
        + (number_of_inverters * inverter_price_usd)
        + (total_batteries_needed * battery_price_usd)
    )
    total_cost_naira = total_cost_usd * exchange_rate

    return {
        "system_voltage": system_voltage,
        "battery_voltage": battery_voltage,
        "battery_charge_ah": battery_charge_ah,
        "efficiency_inverter": efficiency_inverter,
        "battery_efficiency": battery_efficiency,
        "battery_energy_required_Wh": round(battery_energy_required_Wh, 2),
        "daily_system_charge_required_Ah": round(daily_system_charge_required_Ah, 2),
        "battery_capacity_Ah": round(battery_capacity_Ah, 2),
        "batteries_in_series": round(batteries_in_series, 2),
        "batteries_in_parallel": round(batteries_in_parallel, 2),
        "total_batteries_needed": round(total_batteries_needed, 2),
        "solar_power_required_kW": round(solar_power_required_kW, 2),
        "load_covered_by_solar": round(load_covered_by_solar, 2),
        "solar_power_required_losses_adj_W": round(
            solar_power_required_losses_adj_W, 2
        ),
        "number_of_panels": round(number_of_panels, 2),
        "inverter_size_VA": round(inverter_size_VA, 2),
        "number_of_inverters": round(number_of_inverters, 2),
        "total_cost_usd": round(total_cost_usd, 2),
        "total_cost_naira": round(total_cost_naira, 2),
        "products": {
            "best_panel": safe_model_to_dict(best_panel["component"]),
            "best_inverter": safe_model_to_dict(best_inverter["component"]),
            "best_battery": safe_model_to_dict(best_battery["component"]),
        },
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

    bandObject = Band.objects.get(id=band_group)

    if bandObject:
        tariff = float(bandObject.tariff or 0)
        hourPerDay = float(bandObject.hours_supply or 0)
    else:
        raise ValueError("Error: Band data not found for the specified group")

    monthlyEnergyConsumption = float(monthly_spend) / tariff

    print("monthlyEnergyConsumption =", monthlyEnergyConsumption)
    dailyEnergyConsumption = monthlyEnergyConsumption * 1000 / 30
    print("dailyEnergyConsumption =", dailyEnergyConsumption)
    totalWatts = dailyEnergyConsumption / hourPerDay
    print("totalWatts =", totalWatts)

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
