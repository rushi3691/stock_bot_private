import matplotlib.pyplot as plt
import yfinance as yf
import datetime



def graph(company_code, period):
    yf.pdr_override()
    
    company = yf.Ticker(company_code)
    period_check = period
    
    if period_check == '1m':
        company_historical = company.history(period = '1mo', interval = '1d')
    elif period_check == '1y':
        company_historical = company.history(period = '1y', interval = '1wk')
    elif period_check == '5y':
        company_historical = company.history(period = '5y', interval = '1mo')
   

    openday = company_historical['Open']


    prices = list()             # generating list of opening prices
    for i in openday:
        if str(i) != 'nan':
            prices.append(i)

    x = list()                      # generating list of x-coordinates
    for _ in range(len(prices)):        
        x.append(_)
       
    # Importing current date
    current_time = datetime.datetime.now()
    year = current_time.year
    prev_year = int(year) - 1
    month = current_time.month
    prev_month = int(month) - 1
    day = current_time.day
    month_names = {'0':'Dec','1': 'Jan','2': 'Feb','3': 'Mar', '4': 'Apr', '5': 'May','6': 'June', '7': 'July', '8': 'Aug','9': 'Sept','10': 'Oct', '11': 'Nov', '12': 'Dec'}


    my_xticks = list()                      # Generates list for marking dates on x-axis
    for a in range(len(prices)):
        if period_check == 1:
            if a == 0:
                my_xticks.append(str(day) + ' ' + month_names[str(prev_month)])
            elif a == len(prices) - 1:
                my_xticks.append(str(day) + ' ' + month_names[str(month)])
            else:
                my_xticks.append('')

        elif period_check == 2:
            if a == 0:
                my_xticks.append(str(day) + ' ' + month_names[str(month)] + ' ' + str(prev_year))
            elif a == len(prices) - 1:
                my_xticks.append(str(day) + ' ' + month_names[str(month)] + ' ' + str(year))
            else:
                my_xticks.append('')

        elif period_check == 3:
            if a == 0:
                my_xticks.append(str(day) + ' ' + month_names[str(month)] + ' ' + str(int(year) - 5))
            elif a == len(prices) - 1:
                my_xticks.append(str(day) + ' ' + month_names[str(month)] + ' ' + str(year))
            else:
                my_xticks.append('')

                

    plt.xticks(x, my_xticks)
    y = prices   
    plt.plot(x,y)

    plt.xlabel(f'period: {period}')
    plt.ylabel("Price(in USD)")
    plt.title(f"Stock Price of: {company_code}")        # Needs completion

    # fig = plt.gcf()
    # fig.set_size_inches(8, 6)
    plt.savefig("./static/", dpi=100)
    # plt.savefig('stockgraph.png', dpi = 1000) 
    plt.close("all")      # Saves graph
    return 'stockgraph.png'

