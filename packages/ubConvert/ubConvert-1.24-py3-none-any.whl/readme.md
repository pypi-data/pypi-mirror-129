
    ubConvert Unit Conversion Classes -

    - Temperatures()
    - Speed_Distance()
    - Weights()
    - Volumes()
    - Times()

    The functions for most classes can be called in two ways.
    First example, to convert Kelvin to Fahrenheit from class Temperatures():

        kelvin = 278.967
        kelvin_to_fahrenheit(kelvin) = 42.74059999999997

    The second way is with a number representing the rounding factor, where:
        - 0 = integer, 1 = one decimal place, 2 = two decimal places, etc.,

        kelvin = 278.967
        kelvin_to_fahrenheit(kelvin, 2) = 42.74,
        kelvin_to_fahrenheit(kelvin, 1) = 42.7,
		kelvin_to_fahrenheit(kelvin, 0) = 43

    For converting and formatting Light-Years and Astronomical Units to kilometers
    or miles, things are a little different. The first way returns an integer:

        lt_years = 2
        light_years_to_miles(lt_years) = 11758000000000

    The second instance returns a number with requested decimal places in
    scientific notation:

        lt_years = 2
        light_years_to_miles(lt_years, 4) = 1.1758e+13

    Because the answers are such large integers, the third way returns the number
    in comma separated format for easier reading (second arg = 0, third arg = 1):

        lt_years = 2
        light_years_to_miles(lt_years, 0, 1) = 11,758,000,000,000

    ..................................................................
    Example:

        import ubConvert as ub

        weights = ub.Weights()
        oz = weights.grams_to_ounces(28)
        oz = 1

    ..................................................................

    Functions: NOTE- use all lower case when calling functions, right?

    - Temperatures() function list           	 	- Weights() function list

        Kelvin_to_Fahrenheit                      	    Grams_to_Ounces
        Kelvin_to_Celsius                         	    Ounces_to_Grams
        Fahrenheit_to_Kelvin                     	    Kilograms_to_Pounds
        Fahrenheit_to_Celsius                     	    Pounds_to_Kilograms
        Celsius_to_Fahrenheit                    	    Kilograms_to_Tons
        Celsius_to_Kelvin                        	    Tons_to_Kilograms
        Rankine_to_Fahrenheit                     	    Tons_to_Metric_Tonnes
        Fahrenheit_to_Rankine                     	    Metric_Tonnes_to_Tons

    - Speed_Distance() function list         		- Volumes() function list
							     
        MPH_to_KPH                                 	    Liters_to_Gallons
        KPH_to_MPH                                	    Gallons_to_Liters
        MPH_to_Meters_per_Second                            Ounces_to_Milliliters
        Meters_per_Second_to_MPH                   	    Milliliters_to_Ounces
        Meters_per_Second_to_KPH                  	    Cubic_Centimeter_to_Cubic_Inch
        KPH_to_Meters_per_Second                  	    Cubic_Inch_to_Cubic_Centimeter
        Miles_to_Kilometers
        Kilometers_to_Miles                   		- Times() function list
        Light_Years_to_Kilometers
        Kilometers_to_Light_Years                  	    Date_to_Timestamp
        Light_Years_to_Miles                       	    Timestamp_to_Date
        Miles_to_Light_Years
        Yards_to_Meters
        Meters_to_Yards
        Inch_to_Centimeter
        Centimeter_to_Inch
        Astronomical_Unit_to_Miles
        Miles_to_Astronomical_Unit
        Astronomical_Unit_to_Kilometers
        Kilometers_to_Astronomical_Unit
