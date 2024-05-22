import streamlit as st
import pandas as pd


# Define the rate schedules for Merced
merced_rates = {
    "summer": {
        "customer_charge": 350.00,
        "demand_charge_per_kw": 28.00,
        "energy_charge_per_kwh": 0.06780
    },
    "winter": {
        "customer_charge": 350.00,
        "demand_charge_per_kw": 10.00,
        "energy_charge_per_kwh": 0.06780
    }
}
# Function to calculate total monthly cost for Merced
def calculate_merced_costs(num_charging_sessions, num_kwh_per_session, rate_session_dist, actual_max_num_simultaneous_charging,
                           season="summer", mandated_charge_percent=5.35, worst_case=False):
    """
    Calculate the total monthly electricity cost for EV charging stations in Merced based on the season and scenarios.

    Parameters:
    - num_charging_sessions (int): The number of EV charging sessions per month.
    - num_kwh_per_session (int): The number of kWh consumed per charging session.
    - rate_session_dist (dict): Distribution of sessions across on-peak periods.
    - actual_max_num_simultaneous_charging (int): Actual maximum number of cars charging simultaneously.
    - season (str): The season, either "summer" or "winter".
    - mandated_charge_percent (float): Mandated charge percentage.
    - worst_case (bool): If True, calculates costs assuming all chargers are used simultaneously; if False, calculates costs based on the provided actual maximum simultaneous charging.

    Returns:
    - breakdown (dict): A dictionary containing the input parameters, cost breakdown, and total cost.
    """

    # Calculate total kWh
    total_kwh = num_charging_sessions * num_kwh_per_session

    # Calculate total kWh for each time-of-use period
    total_kwh_distribution = {key: rate_session_dist[key] * total_kwh for key in rate_session_dist}

    if season in merced_rates:
        customer_charge = merced_rates[season]["customer_charge"]
        demand_charge_per_kw = merced_rates[season]["demand_charge_per_kw"]
        energy_charge_per_kwh = merced_rates[season]["energy_charge_per_kwh"]

        if worst_case:
            # Calculate actual maximum demand assuming all chargers are in use simultaneously
            actual_max_demand = num_150kw_chargers * 150  # in kW
        else:
            # Calculate actual maximum demand based on provided input
            actual_max_demand = actual_max_num_simultaneous_charging * 150  # in kW

        # Calculate energy cost
        energy_cost = sum(total_kwh_distribution[key] * energy_charge_per_kwh for key in total_kwh_distribution if key in rate_session_dist)

        # Calculate demand charge
        demand_charge = actual_max_demand * demand_charge_per_kw

        # Calculate mandated charge
        mandated_charge = (customer_charge + energy_cost + demand_charge) * (mandated_charge_percent / 100)

        # Total cost
        total_cost = customer_charge + energy_cost + demand_charge + mandated_charge

        breakdown = {
            "num_charging_sessions": num_charging_sessions,
            "num_kwh_per_session": num_kwh_per_session,
            "rate_session_dist": rate_session_dist,
            "actual_max_num_simultaneous_charging": actual_max_num_simultaneous_charging,
            "season": season,
            "mandated_charge_percent": mandated_charge_percent,
            "worst_case": worst_case,
            "customer_charge": customer_charge,
            "energy_cost": energy_cost,
            "demand_charge": demand_charge,
            "mandated_charge": mandated_charge,
            "total_cost": total_cost
        }

        return breakdown

    else:
        raise ValueError("Unsupported season")





# Define the rate schedules for Modesto
modesto_rates = {
    "summer": {
        "fixed_monthly_charge": 192.00,
        "demand_charge_per_kw": 19.37,
        "energy_charge": {
            "on_peak": 0.14252,
            "partial_peak": 0.11169,
            "off_peak": 0.07572
        }
    },
    "winter": {
        "fixed_monthly_charge": 192.00,
        "demand_charge_per_kw": 19.37,
        "energy_charge": {
            "on_peak": 0.09851,
            "off_peak": 0.07572
        }
    }
}

# Function to calculate total monthly cost for Modesto
def calculate_modesto_costs(num_charging_sessions, num_kwh_per_session, rate_session_dist,
                            actual_max_num_simultaneous_charging, season="summer", worst_case=False):
    """
    Calculate the total monthly electricity cost for EV charging stations in Modesto based on the season and scenarios.

    Parameters:
    - num_charging_sessions (int): The number of EV charging sessions per month.
    - num_kwh_per_session (int): The number of kWh consumed per charging session.
    - rate_session_dist (dict): Distribution of sessions across on-peak, partial-peak (for summer), and off-peak periods.
    - actual_max_num_simultaneous_charging (int): Actual maximum number of cars charging simultaneously.
    - season (str): The season, either "summer" or "winter".
    - worst_case (bool): If True, calculates costs assuming all chargers are used simultaneously; if False, calculates costs based on the provided actual maximum simultaneous charging.

    Returns:
    - breakdown (dict): A dictionary containing the input parameters, cost breakdown, and total cost.
    """

    # Calculate total kWh
    total_kwh = num_charging_sessions * num_kwh_per_session

    # Calculate total kWh for each time-of-use period
    total_kwh_distribution = {key: rate_session_dist[key] * total_kwh for key in rate_session_dist}

    if season in modesto_rates:
        fixed_monthly_charge = modesto_rates[season]["fixed_monthly_charge"]
        demand_charge_per_kw = modesto_rates[season]["demand_charge_per_kw"]
        energy_charge = modesto_rates[season]["energy_charge"]

        if worst_case:
            # Calculate actual maximum demand assuming all chargers are in use simultaneously
            actual_max_demand = num_150kw_chargers * 150  # in kW
        else:
            # Calculate actual maximum demand based on provided input
            actual_max_demand = actual_max_num_simultaneous_charging * 150  # in kW

        # Calculate energy cost
        energy_cost = sum(total_kwh_distribution[key] * energy_charge[key] for key in total_kwh_distribution if key in energy_charge)

        # Calculate demand charge
        demand_charge = actual_max_demand * demand_charge_per_kw

        # Total cost
        total_cost = fixed_monthly_charge + energy_cost + demand_charge

        breakdown = {
            "num_charging_sessions": num_charging_sessions,
            "num_kwh_per_session": num_kwh_per_session,
            "rate_session_dist": rate_session_dist,
            "actual_max_num_simultaneous_charging": actual_max_num_simultaneous_charging,
            "season": season,
            "worst_case": worst_case,
            "fixed_monthly_charge": fixed_monthly_charge,
            "energy_cost": energy_cost,
            "demand_charge": demand_charge,
            "total_cost": total_cost
        }

        return breakdown

    else:
        raise ValueError("Unsupported season")









# Define the rate schedules for PG&E BEV-2-S, BEV-1, and BEV-2-P
rates = {
    "BEV-2-S": {
        "subscription_charge_per_block": 95.56,
        "block_size": 50,  # in kW
        "energy_charge": {
            "peak": 0.41522,
            "off_peak": 0.20199,
            "super_off_peak": 0.17872
        },
        "overage_fee_per_kw": 3.82  # per kW
    },
    "BEV-1": {
        "subscription_charge_per_block": 12.41,
        "block_size": 10,  # in kW
        "energy_charge": {
            "peak": 0.40040,
            "off_peak": 0.20839,
            "super_off_peak": 0.18173
        },
        "overage_fee_per_kw": 2.48  # per kW
    },
    "BEV-2-P": {
        "subscription_charge_per_block": 85.98,
        "block_size": 50,  # in kW
        "energy_charge": {
            "peak": 0.40635,
            "off_peak": 0.19747,
            "super_off_peak": 0.17481
        },
        "overage_fee_per_kw": 3.44  # per kW
    }
}
# Function to calculate total monthly cost for PG&E BEV-2-S, BEV-1, and BEV-2-P
def calculate_pge_costs(num_charging_sessions, num_kwh_per_session, rate_session_dist,
                        predefine_max_num_simultaneous_charging, actual_max_num_simultaneous_charging,
                        subscription_type="BEV-2-S", worst_case=False):
    """
    Computes PG&E total monthly electricity cost given subscription types (PG&E BEV-2-S, BEV-1, and BEV-2-P) and scenarios (normal or worst case).
    Total cost = energy cost + subscription charges + overage fees.

    Notes:
    Worst case scenario means running at all chargers running simultaneously, which may cause high overage fee.

    Parameters:
    - num_charging_sessions (int): The number of EV charging sessions per month.
    - num_kwh_per_session (int): The number of kWh consumed per charging session.
    - rate_session_dist (dict): Distribution of sessions across peak, off-peak, and super off-peak periods, e.g., {"peak": 0.2, "off_peak": 0.3, "super_off_peak": 0.5}.
    - predefine_max_num_simultaneous_charging (int): Predefined maximum number of cars charging simultaneously.
    - actual_max_num_simultaneous_charging (int): Actual maximum number of cars charging simultaneously.
    - subscription_type (str): The type of subscription plan, can be "BEV-2-S", "BEV-1", or "BEV-2-P".
    - worst_case (bool): If True, calculates costs assuming all chargers are used simultaneously; if False, calculates costs based on the provided actual maximum simultaneous charging.

    Returns:
    - breakdown (dict): A dictionary containing the input parameters, cost breakdown, and total cost.
    """

    # Calculate total kWh
    total_kwh = num_charging_sessions * num_kwh_per_session

    # Calculate total kWh for each time-of-use period
    total_kwh_distribution = {
        "peak": rate_session_dist['peak'] * total_kwh,
        "off_peak": rate_session_dist['off_peak'] * total_kwh,
        "super_off_peak": rate_session_dist['super_off_peak'] * total_kwh
    }

    if subscription_type in rates:
        subscription_charge_per_block = rates[subscription_type]["subscription_charge_per_block"]
        block_size = rates[subscription_type]["block_size"]
        energy_charge = rates[subscription_type]["energy_charge"]
        overage_fee_per_kw = rates[subscription_type]["overage_fee_per_kw"]

        # Calculate the number of blocks needed based on maximum simultaneous charging
        num_blocks = predefine_max_num_simultaneous_charging * (150 // block_size)

        # Calculate the subscribed maximum demand
        subscribed_max_demand = num_blocks * block_size

        if worst_case:
            # Calculate actual maximum demand assuming all chargers are in use simultaneously
            actual_max_demand = num_150kw_chargers * 150  # in kW
        else:
            # Calculate actual maximum demand based on provided input
            actual_max_demand = actual_max_num_simultaneous_charging * 150  # in kW

        # Calculate energy cost
        energy_cost = (total_kwh_distribution["peak"] * energy_charge["peak"]) + \
                      (total_kwh_distribution["off_peak"] * energy_charge["off_peak"]) + \
                      (total_kwh_distribution["super_off_peak"] * energy_charge["super_off_peak"])

        # Calculate subscription cost
        subscription_charge = num_blocks * subscription_charge_per_block

        # Calculate overage fee if actual demand exceeds subscribed demand
        overage_fee = 0
        if actual_max_demand > subscribed_max_demand:
            excess_demand = actual_max_demand - subscribed_max_demand
            overage_fee = excess_demand * overage_fee_per_kw

        # Total cost
        total_cost = energy_cost + subscription_charge + overage_fee

        breakdown = {
            "num_charging_sessions": num_charging_sessions,
            "num_kwh_per_session": num_kwh_per_session,
            "rate_session_dist": rate_session_dist,
            "predefine_max_num_simultaneous_charging": predefine_max_num_simultaneous_charging,
            "actual_max_num_simultaneous_charging": actual_max_num_simultaneous_charging,
            "subscription_type": subscription_type,
            "worst_case": worst_case,
            "energy_cost": energy_cost,
            "subscription_charge": subscription_charge,
            "overage_fee": overage_fee,
            "total_cost": total_cost
        }

        return breakdown

    else:
        raise ValueError("Unsupported subscription type")







# Copy the three provided functions into this file
# Add your functions for calculating the costs here

# Function to determine which utility function to use based on location
def calculate_cost(location, params):
    if location == "Modesto":
        rate_schedule = modesto_rates
        breakdown = calculate_modesto_costs(**params)
    elif location == "Merced":
        rate_schedule = merced_rates
        breakdown = calculate_merced_costs(**params)
    elif location == "PG&E":
        rate_schedule = rates
        breakdown = calculate_pge_costs(**params)
    else:
        raise ValueError("Unsupported location")
    return rate_schedule, breakdown

# Streamlit UI
st.title("EV Charging Cost Calculator")

# Select location
location = st.selectbox("Select Location", ["Modesto", "Merced", "PG&E"])

# Define input parameters
num_charging_sessions = st.number_input("Number of EV Charging Sessions", min_value=100, max_value=10000, value=1000)
num_kwh_per_session = st.number_input("Number of kWh Purchased per Session", min_value=1, max_value=500, value=100)
actual_max_num_simultaneous_charging = st.number_input("Maximum Number of Cars Charging at Once", min_value=1, max_value=50, value=10)

params = {
    "num_charging_sessions": num_charging_sessions,
    "num_kwh_per_session": num_kwh_per_session,
    "actual_max_num_simultaneous_charging": actual_max_num_simultaneous_charging
}

if location == "PG&E":
    rate_session_dist = {
        "peak": st.slider("Peak Sessions (%)", min_value=0, max_value=100, value=20) / 100,
        "off_peak": st.slider("Off Peak Sessions (%)", min_value=0, max_value=100, value=50) / 100,
        "super_off_peak": st.slider("Super Off Peak Sessions (%)", min_value=0, max_value=100, value=30) / 100
    }
    predefine_max_num_simultaneous_charging = st.number_input("Predefined Maximum Number of Cars Charging Simultaneously", min_value=1, max_value=50, value=10)
    subscription_type = st.selectbox("Subscription Type", ["BEV-2-S", "BEV-1", "BEV-2-P"])
    params.update({
        "rate_session_dist": rate_session_dist,
        "predefine_max_num_simultaneous_charging": predefine_max_num_simultaneous_charging,
        "subscription_type": subscription_type
    })
    notes = """ Worst case scenario means running at all chargers running simultaneously, which may cause high overage fee.
    Parameters:
    - num_charging_sessions (int): The number of EV charging sessions per month.
    - num_kwh_per_session (int): The number of kWh consumed per charging session.
    - rate_session_dist (dict): Distribution of sessions across peak, off-peak, and super off-peak periods, e.g., {"peak": 0.2, "off_peak": 0.3, "super_off_peak": 0.5}.
    - predefine_max_num_simultaneous_charging (int): Predefined maximum number of cars charging simultaneously.
    - actual_max_num_simultaneous_charging (int): Actual maximum number of cars charging simultaneously.
    - subscription_type (str): The type of subscription plan, can be "BEV-2-S", "BEV-1", or "BEV-2-P".
    - worst_case (bool): If True, calculates costs assuming all chargers are used simultaneously; if False, calculates costs based on the provided actual maximum simultaneous charging.
    
    Returns:
    - breakdown (dict): A dictionary containing the input parameters, cost breakdown, and total cost.
    """
    
elif location == "Modesto":
    season = st.selectbox("Season", ["summer", "winter"])
    rate_session_dist = {
        "on_peak": st.slider("On Peak Sessions (%)", min_value=0, max_value=100, value=30) / 100,
        "partial_peak": st.slider("Partial Peak Sessions (%)", min_value=0, max_value=100, value=30) / 100,
        "off_peak": st.slider("Off Peak Sessions (%)", min_value=0, max_value=100, value=40) / 100
    }
    params.update({
        "rate_session_dist": rate_session_dist,
        "season": season
    })
    notes =   """ Calculate the total monthly electricity cost for EV charging stations in Modesto based on the season and scenarios.

  Parameters:
  - num_charging_sessions (int): The number of EV charging sessions per month.
  - num_kwh_per_session (int): The number of kWh consumed per charging session.
  - rate_session_dist (dict): Distribution of sessions across on-peak, partial-peak (for summer), and off-peak periods.
  - actual_max_num_simultaneous_charging (int): Actual maximum number of cars charging simultaneously.
  - season (str): The season, either "summer" or "winter".
  - worst_case (bool): If True, calculates costs assuming all chargers are used simultaneously; if False, calculates costs based on the provided actual maximum simultaneous charging.

  Returns:
  - total_cost (float): The total monthly cost of electricity for the given parameters.
  """
elif location == "Merced":
    season = st.selectbox("Season", ["summer", "winter"])
    rate_session_dist = {
        "on_peak": st.slider("On Peak Sessions (%)", min_value=0, max_value=100, value=100) / 100
    }
    mandated_charge_percent = st.slider("Mandated Charge Percent", min_value=3.35, max_value=5.35, value=5.35)
    params.update({
        "rate_session_dist": rate_session_dist,
        "season": season,
        "mandated_charge_percent": mandated_charge_percent
    })
    notes =   """ Calculate the total monthly electricity cost for EV charging stations in Merced based on the season and scenarios.

  Parameters:
  - num_charging_sessions (int): The number of EV charging sessions per month.
  - num_kwh_per_session (int): The number of kWh consumed per charging session.
  - rate_session_dist (dict): Distribution of sessions across on-peak periods.
  - actual_max_num_simultaneous_charging (int): Actual maximum number of cars charging simultaneously.
  - season (str): The season, either "summer" or "winter".
  - mandated_charge_percent (float): Mandated charge percentage.
  - worst_case (bool): If True, calculates costs assuming all chargers are used simultaneously; if False, calculates costs based on the provided actual maximum simultaneous charging.

  Returns:
  - total_cost (float): The total monthly cost of electricity for the given parameters.
  """

# Calculate the costs
if st.button("Calculate Cost"):
    rate_schedule, result = calculate_cost(location, params)

    st.subheader("Total Cost")
    st.write(f"Total Cost: ${result['total_cost']:.2f}")

    st.subheader("Rate Schedule")
    st.write(rate_schedule)
    
    st.subheader("Cost Breakdown")
    st.write(result)

    
    st.subheader("Notes")
    st.write(notes)
