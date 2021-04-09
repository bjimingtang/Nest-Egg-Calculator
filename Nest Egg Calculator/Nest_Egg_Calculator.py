
import sys
import random
import matplotlib.pyplot as plot

def read_to_list(file_name):
    """Open a file of data in percentages, convert to decimal, and put into a list. Return the list."""
    with open(file_name) as input_file:
        ##strip whitespace from each line
        lines = [float(line.strip()) for line in input_file];
        decimal = [round(line / 100, 5) for line in lines];
        return decimal;

def default_input(prompt, default=None):
    prompt = '{} [{}]: '.format(prompt, default);
    response = input(prompt);
    if not response and default:
        return default;
    else:
        return response;

def montecarlo(returns):
    """Run Monte Carlo and return investment value at end-of-plan and bankrupt count."""
    case_count = 0;
    bankrupt_count = 0;
    outcome = [];

    while case_count < int(num_cases):
        investments = int(start_value);
        start_year = random.randrange(0, len(returns));
        duration = int(random.triangular(int(minimum_retirement_years), int(most_likely_retirement_years), int(maximum_retirement_years)));
        end_year = start_year + duration;
        lifespan = [year for year in range(start_year, end_year)];
        bankrupt = False;

        #temporary list per case
        lifespan_returns = [];
        lifespan_inflation = [];
        for year in lifespan:
            lifespan_returns.append(returns[year % len(returns)]);
            lifespan_inflation.append(inflation_rate[year % len(inflation_rate)]);

        #loop through each year of retirement for each case
        for year, lifespan_return in enumerate(lifespan_returns):
            inflation = lifespan_inflation[year];

            #no inflation in first year
            if year == 0:
                withdrawal_adjusted = int(withdrawal);
            else:
                withdrawal_adjusted = int(withdrawal_adjusted * (1 + inflation));

            investments -= withdrawal_adjusted;
            investments = int(investments * (1 + lifespan_return));

            if investments <= 0:
                bankrupt = True;
                break;

        if bankrupt:
            outcome.append(0);
            bankrupt_count += 1;
        else:
            outcome.append(investments);
        
        case_count += 1;

    return outcome, bankrupt_count;

def bankrupt_probability(outcome, bankrupt_count):
    """Calculate the chance of bankruptcy, plus other stats of interest"""
    total_trials = len(outcome);
    odds_of_bankruptcy = round(100 * bankrupt_count / total_trials, 1);

    #print stats, with numbers formatted to include commas for readability
    print('\nInvestment type: {}\n'.format(invest_type));
    print('\nStarting value: ${:,}\n'.format(int(start_value)));
    print('\nAnnual withdrawal: ${:,}\n'.format(int(withdrawal)));
    print('\nYears in retirement (minimum-most likely-maximum): {}-{}-{}\n'.format(minimum_retirement_years, most_likely_retirement_years, maximum_retirement_years));
    print('\nNumber of trials: {:,}\n'.format(len(outcome)));
    print('\nOdds of running out of money: {}%\n'.format(odds_of_bankruptcy));
    print('\nAverage outcome: ${:,}\n'.format(int(sum(outcome)/total_trials)));
    print('\nMinimum outcome: ${:,}\n'.format(min(result for result in outcome)));
    print('\nMaximum outcome: ${:,}\n'.format(max(result for result in outcome)));

    return odds_of_bankruptcy;

def main():
    """Use Monte Carlo and bankruptcy functions to calculate, then draw the bar chart."""
    outcome, bankrupt_count = montecarlo(investment_type_args[invest_type]);
    bankruptcy_odds = bankrupt_probability(outcome, bankrupt_count);

    #plot first 3000 runs
    plot_data = outcome[:3000];

    plot.figure('Outcome by Case (showing first 3000 runs)', figsize=(16,5));
    index = [data + 1 for data in range(len(plot_data))];
    plot.bar(index, plot_data, color='black');
    plot.xlabel('Simulated Lives', fontsize=18);
    plot.ylabel('$ Remaining', fontsize=18);
    #want to display plain text, not scientific notation
    plot.ticklabel_format(style='plain', axis='y');
    ax = plot.gca();
    #add commas to the numeric text to make it more readable
    ax.get_yaxis().set_major_formatter(plot.FuncFormatter(lambda x, loc: "{:,}".format(int(x))));
    plot.title('Probability of running out of money = {}%'.format(bankruptcy_odds), fontsize=20, color='red');
    plot.show();

#data loading
print('\nNote: Input data should be in percent, not decimal!\n');
try:
    bonds = read_to_list('10-yr_tBond_returns_1926-2013_pct.txt');
    stocks = read_to_list('SP500_returns_1926-2013_pct.txt');
    blend_40_50_10 = read_to_list('S-B-C_blend_1926-2013_pct.txt');
    blend_50_50 = read_to_list('S-B_blend_1926-2013_pct.txt');
    inflation_rate = read_to_list('annual_infl_rate_1926-2013_pct.txt');
except IOError as err:
    print("{}. \nTerminating program.".format(err), file=sys.stderr);
    sys.exit(1);

#user input dictionary
investment_type_args = {'bonds': bonds, 
                        'stocks': stocks,
                        'sbc_blend': blend_40_50_10,
                        'sb_blend': blend_50_50};

#print input definitions for user
print("\nbonds=10-yr Treasury Bond\n");
print("\nstocks=SP500\n");
print("\nsbc_blend = 40% SP500/50% Treasury Bond/10% cash\n");
print("\nsb_blend = 50% SP500/50% Treasury Bond\n");

print("\nPress ENTER to take the default value shown in [brackets].\n");

#get user input
invest_type = default_input('Enter investment type: (bonds, stocks, sbc_blend, sb_blend): \n', 'bonds').lower();
#validate the investment type
while invest_type not in investment_type_args:
    invest_type = input("Invalid investment. Enter a valid investment type as listed in the prompt: \n");

start_value = default_input("Input the starting value of your investments: \n", '2000000');
#validate the starting value
while not start_value.isdigit():
    start_value = input("Invalid input! Enter an integer: \n");

withdrawal = default_input("Input annual pre-tax withdrawal (today's $): \n", '80000');
#validate the withdrawal value
while not withdrawal.isdigit():
    withdrawal = input("Invalid input! Enter an integer: \n");

minimum_retirement_years = default_input("Input minimum retirement years: \n", '18');
#validate the minimum retirement years
while not minimum_retirement_years.isdigit():
    minimum_retirement_years = input("Invalid input! Enter an integer: \n");

most_likely_retirement_years = default_input("Input most-likely retirement years: \n", '25');
#validate the most-likely retirement years
while not most_likely_retirement_years.isdigit():
    most_likely_retirement_years = input("Invalid input! Enter an integer: \n");

maximum_retirement_years = default_input("Input maximum retirement years: \n", '40');
#validate the maximum retirement years
while not maximum_retirement_years.isdigit():
    maximum_retirement_years = input("Invalid input! Enter an integer: \n");

num_cases = default_input("Input number of cases to run: \n", '50000');
#validate the number of cases
while not num_cases.isdigit():
    num_cases = input("Invalid input! Enter an integer: \n");

#additional validation of year numbers
if not int(minimum_retirement_years) < int(most_likely_retirement_years) < int(maximum_retirement_years):
    print("\nMinimum should be smaller than most likely and most likely should be smaller than maximum (retirement years)!\n", file-sys.stderr);
    sys.exit(1);
if int(maximum_retirement_years) > 99:
    print("\nMaximum retirement years shouldn't be more than 99!\n", file=sys.stderr);
    sys.exit(1);

#run program
if __name__ == '__main__':
    main();